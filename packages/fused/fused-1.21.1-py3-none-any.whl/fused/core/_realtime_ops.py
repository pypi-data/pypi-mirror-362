from __future__ import annotations

import json
import sys
import time
from typing import TYPE_CHECKING, Any

import aiohttp
import requests
import yarl

from fused._optional_deps import (
    GPD_GEODATAFRAME,
    HAS_GEOPANDAS,
    HAS_PANDAS,
    HAS_SHAPELY,
    PD_DATAFRAME,
    SHAPELY_GEOMETRY,
)
from fused._options import options as OPTIONS
from fused._request import raise_for_status, raise_for_status_async
from fused.models.udf._eval_result import UdfEvaluationResult
from fused.types import UdfRuntimeError

from ..models import AnyJobStepConfig
from ..models.udf import AnyBaseUdf
from ..models.udf._eval_result import is_response_cached
from ._impl._context_impl import context_get_auth_header, context_get_user_email
from ._impl._realtime_ops_impl import (
    get_recursion_factor,
    make_realtime_url,
    make_shared_realtime_url,
)
from ._serialization import (
    deserialize_html,
    deserialize_json,
    deserialize_npy,
    deserialize_parquet,
    deserialize_png,
    deserialize_tiff,
    deserialize_zip,
)

if TYPE_CHECKING:
    import pandas as pd
    import xarray as xr


def serialize_realtime_params(params: dict[str, Any]):
    result = {}
    for param_name, param_value in params.items():
        if (HAS_GEOPANDAS and isinstance(param_value, GPD_GEODATAFRAME)) or (
            HAS_PANDAS and isinstance(param_value, PD_DATAFRAME)
        ):
            result[param_name] = param_value.to_json()
        elif isinstance(param_value, (list, tuple, dict, bool)):
            result[param_name] = json.dumps(param_value)
        elif HAS_SHAPELY and isinstance(param_value, SHAPELY_GEOMETRY):
            import shapely

            result[param_name] = shapely.to_wkt(param_value)
        else:
            result[param_name] = param_value

    return result


def _realtime_raise_for_status(r: requests.Response):
    if r.status_code >= 400 and "x-fused-error" in r.headers:
        msg = str(r.headers["x-fused-error"])
        raise requests.HTTPError(msg, response=r)
    if r.status_code >= 400 and "x-fused-metadata" in r.headers:
        # x-fused-metadata holds LogHandler as JSON, which contains stdout/stderr.
        _fused_metadata = r.headers.get("x-fused-metadata")
        fused_metadata = json.loads(_fused_metadata) if _fused_metadata else {}

        # Extract stdout/stderr.
        stdout = fused_metadata.get("stdout")
        stderr = fused_metadata.get("stderr")

        # Extract exception details
        exception_class = fused_metadata.get("exception_class")
        has_exception = fused_metadata.get("has_exception", False)

        # Extract error line, if exists.
        error_lineno = fused_metadata.get("lineno")

        error_message = ""
        if "errormsg" in fused_metadata and fused_metadata["errormsg"]:
            error_message = f"The UDF returned the following error in line {fused_metadata.get('lineno')}:\n{fused_metadata['errormsg']}"
        elif "exception" in fused_metadata and fused_metadata["exception"]:
            error_message = fused_metadata["exception"]

        return UdfEvaluationResult(
            data=None,
            time_taken_seconds=0.0,  # TODO
            stdout=stdout,
            stderr=stderr,
            error_message=error_message,
            error_lineno=error_lineno,
            has_exception=has_exception,
            exception_class=exception_class,
        )

    raise_for_status(r)


async def _realtime_raise_for_status_async(r: aiohttp.ClientResponse):
    if r.status >= 400 and "x-fused-error" in r.headers:
        msg = str(r.headers["x-fused-error"])
        raise aiohttp.ClientResponseError(
            request_info=r.request_info,
            status=r.status,
            message=msg,
            headers=r.headers,
            history=r.history,
        )
    if r.status >= 400 and "x-fused-metadata" in r.headers:
        # x-fused-metadata holds LogHandler as JSON, which contains stdout/stderr.
        _fused_metadata = r.headers.get("x-fused-metadata")
        fused_metadata = json.loads(_fused_metadata) if _fused_metadata else {}

        # Extract stdout/stderr.
        stdout = fused_metadata.get("stdout")
        # stderr = fused_metadata.get("stderr")

        # Extract exception details
        exception_class = fused_metadata.get("exception_class")
        # has_exception = fused_metadata.get("has_exception", False)

        # Extract error line, if exists.
        # error_lineno = fused_metadata.get("lineno")

        error_message = ""
        if "errormsg" in fused_metadata and fused_metadata["errormsg"]:
            error_message = f"The UDF returned the following error in line {fused_metadata.get('lineno')}:\n{fused_metadata['errormsg']}"
        elif "exception" in fused_metadata and fused_metadata["exception"]:
            error_message = fused_metadata["exception"]

        if stdout:
            sys.stdout.write(stdout)
        raise UdfRuntimeError(error_message, child_exception_class=exception_class)

    await raise_for_status_async(r)


async def _realtime_follow_redirect_async(
    *, session: aiohttp.ClientSession, r: aiohttp.ClientResponse
):
    if r.status >= 300 and r.status < 400 and "location" in r.headers:
        # Per this link, aiohttp will mangle the redirect URL
        # https://stackoverflow.com/questions/77319421/aiohttp-showing-403-forbidden-error-but-requests-get-giving-200-ok-response
        url = yarl.URL(r.headers["location"], encoded=True)
        return await session.get(url)
    return r


def run_tile(
    email_or_team: str,
    id: str | None = None,
    *,
    x: int,
    y: int,
    z: int,
    cache_max_age: int | None = None,
    _dtype_out_vector: str | None = None,
    _dtype_out_raster: str | None = None,
    _client_id: str | None = None,
    **params,
) -> pd.DataFrame | xr.Dataset | None:
    """
    Executes a private tile-based UDF indexed under the specified email and ID. The calling user must have the necessary permissions to execute the UDF.

    This function constructs a URL to run a UDF on a specific tile defined by its x, y, and z coordinates, and
    sends a request to the server. It supports customization of the output data types for vector and raster data,
    as well as additional parameters for the UDF execution.

    Args:
        email (str): Email address of user account associated with the UDF.
        id (Optional[str]): Unique identifier for the UDF. If None, the user's email is used as the ID.
        x (int): The x coordinate of the tile.
        y (int): The y coordinate of the tile.
        z (int): The zoom level of the tile.
        cache_max_age (Optional[int]): The maximum age when returning a result from the cache.
        _dtype_out_vector (str): Desired data type for vector output. Defaults to a pre-defined type.
        _dtype_out_raster (str): Desired data type for raster output. Defaults to a pre-defined type.
        _client_id (Optional[str]): Client identifier for API usage. If None, a default or global client ID may be used.
        **params: Additional keyword arguments for the UDF execution.

    Returns:
        The response from the server after executing the UDF on the specified tile.
    """
    if id is None:
        id = email_or_team
        email_or_team = context_get_user_email()

    url = f"{make_realtime_url(_client_id)}/api/v1/run/udf/saved/{email_or_team}/{id}/tiles/{z}/{x}/{y}"
    return _run_and_process(
        url=url,
        cache_max_age=cache_max_age,
        _dtype_out_vector=_dtype_out_vector,
        _dtype_out_raster=_dtype_out_raster,
        **params,
    )


def run_shared_tile(
    token: str,
    *,
    x: int,
    y: int,
    z: int,
    cache_max_age: int | None = None,
    _dtype_out_vector: str | None = None,
    _dtype_out_raster: str | None = None,
    _client_id: str | None = None,
    **params,
) -> pd.DataFrame | xr.Dataset | None:
    """
    Executes a shared tile-based UDF.

    This function constructs a URL to run a UDF on a specific tile defined by its x, y, and z coordinates, and
    sends a request to the server. It supports customization of the output data types for vector and raster data,
    as well as additional parameters for the UDF execution.

    Args:
        token (str): A shared access token that authorizes the operation.
        id (Optional[str]): Unique identifier for the UDF. If None, the user's email is used as the ID.
        x (int): The x coordinate of the tile.
        y (int): The y coordinate of the tile.
        z (int): The zoom level of the tile.
        cache_max_age (Optional[int]): The maximum age when returning a result from the cache.
        _dtype_out_vector (str): Desired data type for vector output. Defaults to a pre-defined type.
        _dtype_out_raster (str): Desired data type for raster output. Defaults to a pre-defined type.
        _client_id (Optional[str]): Client identifier for API usage. If None, a default or global client ID may be used.
        **params: Additional keyword arguments for the UDF execution.

    Returns:
        The response from the server after executing the UDF on the specified tile.
    """
    url = f"{make_shared_realtime_url(token)}/run/tiles/{z}/{x}/{y}"
    return _run_and_process(
        url=url,
        cache_max_age=cache_max_age,
        _dtype_out_vector=_dtype_out_vector,
        _dtype_out_raster=_dtype_out_raster,
        _client_id=_client_id,
        _is_shared=True,
        **params,
    )


def _run_and_process(
    url: str,
    *,
    cache_max_age: int | None = None,
    _dtype_out_vector: str | None = None,
    _dtype_out_raster: str | None = None,
    _profile: bool = False,
    _is_shared: bool = False,
    **params,
):
    access_token_header = context_get_auth_header(missing_ok=_is_shared)
    recursion_factor = get_recursion_factor()

    req_params = {
        # TODO...
        **({"cache_max_age": int(cache_max_age)} if cache_max_age is not None else {}),
        "dtype_out_vector": _dtype_out_vector or OPTIONS.default_dtype_out_vector,
        "dtype_out_raster": _dtype_out_raster or OPTIONS.default_dtype_out_raster,
        "profile": _profile,
        **(serialize_realtime_params(params) if params is not None else {}),
    }

    time_start = time.perf_counter()
    r = requests.get(
        url=url,
        params=req_params,
        headers={
            **access_token_header,
            **(OPTIONS.default_run_headers or {}),
            "Fused-Recursion": f"{recursion_factor}",
        },
    )
    time_end = time.perf_counter()
    exc = _realtime_raise_for_status(r)
    if exc is not None:
        return exc

    time_taken_seconds = time_end - time_start
    return _process_response(
        r, step_config=None, time_taken_seconds=time_taken_seconds, profile=_profile
    )


def run_file(
    email_or_team: str,
    id: str | None = None,
    *,
    cache_max_age: int | None = None,
    _dtype_out_vector: str | None = None,
    _dtype_out_raster: str | None = None,
    _client_id: str | None = None,
    **params,
) -> pd.DataFrame | xr.Dataset | None:
    """
    Executes a private file-based UDF indexed under the specified email and ID. The calling user must have the necessary permissions to execute the UDF.

    This function constructs a URL to run a UDF associated with the given email and ID, allowing for output data type customization for both vector and raster outputs. It also supports additional parameters for the UDF execution.

    Args:
        email (str): Email address of user account associated with the UDF.
        id (Optional[str]): Unique identifier for the UDF. If None, the user's email is used as the ID.
        cache_max_age (Optional[int]): The maximum age when returning a result from the cache.
        _dtype_out_vector (str): Desired data type for vector output, defaults to a predefined type.
        _dtype_out_raster (str): Desired data type for raster output, defaults to a predefined type.
        _client_id (Optional[str]): Client identifier for API usage. If None, a default or global client ID may be used.
        **params: Additional keyword arguments for the UDF execution.

    Returns:
        The response from the server after executing the UDF.
    """
    if id is None:
        id = email_or_team
        email_or_team = context_get_user_email()

    url = f"{make_realtime_url(_client_id)}/api/v1/run/udf/saved/{email_or_team}/{id}"
    return _run_and_process(
        url=url,
        cache_max_age=cache_max_age,
        _dtype_out_vector=_dtype_out_vector,
        _dtype_out_raster=_dtype_out_raster,
        **params,
    )


def run_shared_file(
    token: str,
    *,
    cache_max_age: int | None = None,
    _dtype_out_vector: str | None = None,
    _dtype_out_raster: str | None = None,
    **params,
) -> pd.DataFrame | xr.Dataset | None:
    """
    Executes a shared file-based UDF.

    This function constructs a URL for running an operation on a file accessible via a shared token. It allows for customization of the output data types for vector and raster data and supports additional parameters for the operation's execution.

    Args:
        token (str): A shared access token that authorizes the operation.
        cache_max_age (Optional[int]): The maximum age when returning a result from the cache.
        _dtype_out_vector (str): Desired data type for vector output, defaults to a predefined type.
        _dtype_out_raster (str): Desired data type for raster output, defaults to a predefined type.
        **params: Additional keyword arguments for the operation execution.

    Returns:
        The response from the server after executing the operation on the file.

    Raises:
        Exception: Describes various exceptions that could occur during the function execution, including but not limited to invalid parameters, network errors, unauthorized access errors, or server-side errors.

    Note:
        This function is designed to access shared operations that require a token for authorization. It requires network access to communicate with the server hosting these operations and may incur data transmission costs or delays depending on the network's performance.
    """
    url = f"{make_shared_realtime_url(token)}/run/file"
    return _run_and_process(
        url=url,
        cache_max_age=cache_max_age,
        _dtype_out_vector=_dtype_out_vector,
        _dtype_out_raster=_dtype_out_raster,
        _is_shared=True,
        **params,
    )


async def run_tile_async(
    email_or_team: str,
    id: str | None = None,
    *,
    x: int,
    y: int,
    z: int,
    cache_max_age: int | None = None,
    _dtype_out_vector: str | None = None,
    _dtype_out_raster: str | None = None,
    _client_id: str | None = None,
    **params,
) -> pd.DataFrame | xr.Dataset | None:
    """
    Asynchronously executes a private tile-based UDF indexed under the specified email and ID. The calling user must have the necessary permissions to execute the UDF.

    This function constructs a URL to asynchronously run a UDF on a specific tile defined by its x, y, and z coordinates. It supports customization of the output data types for vector and raster data, and accommodates additional parameters for the UDF execution.

    Args:
        email (str): The user's email address, used to identify the user's saved UDFs. If the ID is not provided, this email will also be used as the ID.
        id (Optional[str]): Unique identifier for the UDF. If None, the user's email is used as the ID.
        x (int): The x coordinate of the tile.
        y (int): The y coordinate of the tile.
        z (int): The zoom level of the tile.
        cache_max_age (Optional[int]): The maximum age when returning a result from the cache.
        _dtype_out_vector (str): Desired data type for vector output. Defaults to a predefined type.
        _dtype_out_raster (str): Desired data type for raster output. Defaults to a predefined type.
        _client_id (Optional[str]): Client identifier for API usage. If None, a default or global client ID may be used.
        **params: Additional keyword arguments for the UDF execution.

    Returns:
        A coroutine that, when awaited, sends a request to the server to execute the UDF on the specified tile and returns the server's response. The format and content of the response depend on the UDF's implementation and the server's response format.
    """
    if id is None:
        id = email_or_team
        email_or_team = context_get_user_email()

    url = f"{make_realtime_url(_client_id)}/api/v1/run/udf/saved/{email_or_team}/{id}/tiles/{z}/{x}/{y}"
    return await _run_and_process_async(
        url=url,
        cache_max_age=cache_max_age,
        _dtype_out_vector=_dtype_out_vector,
        _dtype_out_raster=_dtype_out_raster,
        **params,
    )


async def run_shared_tile_async(
    token: str,
    *,
    x: int,
    y: int,
    z: int,
    cache_max_age: int | None = None,
    _dtype_out_vector: str | None = None,
    _dtype_out_raster: str | None = None,
    **params,
) -> pd.DataFrame | xr.Dataset | None:
    """
    Asynchronously executes a shared tile-based UDF using a specific access token.

    This function constructs a URL for running an operation on a tile, defined by its x, y, and z coordinates, accessible via a shared token. It allows for customization of the output data types for vector and raster data and supports additional parameters for the operation's execution.

    Args:
        token (str): A shared access token that authorizes the operation on the specified tile.
        x (int): The x coordinate of the tile.
        y (int): The y coordinate of the tile.
        z (int): The zoom level of the tile.
        cache_max_age (Optional[int]): The maximum age when returning a result from the cache.
        _dtype_out_vector (str): Desired data type for vector output, defaults to a predefined type.
        _dtype_out_raster (str): Desired data type for raster output, defaults to a predefined type.
        **params: Additional keyword arguments for the operation execution.

    Returns:
        A coroutine that, when awaited, sends a request to the server to execute the operation on the specified tile and returns the server's response. The format and content of the response depend on the operation's implementation and the server's response format.
    """
    url = f"{make_shared_realtime_url(token)}/run/tiles/{z}/{x}/{y}"
    return await _run_and_process_async(
        url=url,
        cache_max_age=cache_max_age,
        _dtype_out_vector=_dtype_out_vector,
        _dtype_out_raster=_dtype_out_raster,
        _is_shared=True,
        **params,
    )


async def _run_and_process_async(
    url: str,
    *,
    cache_max_age: int | None = None,
    _dtype_out_vector: str | None = None,
    _dtype_out_raster: str | None = None,
    _is_shared: bool = False,
    **params,
):
    access_token_header = context_get_auth_header(missing_ok=_is_shared)
    recursion_factor = get_recursion_factor()

    req_params = {
        # TODO...
        **({"cache_max_age": int(cache_max_age)} if cache_max_age is not None else {}),
        "dtype_out_vector": _dtype_out_vector or OPTIONS.default_dtype_out_vector,
        "dtype_out_raster": _dtype_out_raster or OPTIONS.default_dtype_out_raster,
        **(serialize_realtime_params(params) if params is not None else {}),
    }

    time_start = time.perf_counter()
    if OPTIONS.pyodide_async_requests:
        import pyodide.http

        url_with_params = yarl.URL(url, encoded=True).with_query(req_params)
        r = await pyodide.http.pyfetch(
            str(url_with_params),
            headers={
                **access_token_header,
                **(OPTIONS.default_run_headers or {}),
                "Fused-Recursion": f"{recursion_factor}",
            },
        )
        time_end = time.perf_counter()
        redirect = r.headers.get("x-fused-redirect", None)
        if redirect:
            url = yarl.URL(redirect, encoded=True)
            r = await pyodide.http.pyfetch(url)

        await _realtime_raise_for_status_async(r)

        time_taken_seconds = time_end - time_start
        result = await _process_response_async(
            r, step_config=None, time_taken_seconds=time_taken_seconds
        )

    else:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url=url,
                params=req_params,
                headers={
                    **access_token_header,
                    **(OPTIONS.default_run_headers or {}),
                    "Fused-Recursion": f"{recursion_factor}",
                },
                allow_redirects=False,
            ) as r:
                time_end = time.perf_counter()
                r = await _realtime_follow_redirect_async(session=session, r=r)
                await _realtime_raise_for_status_async(r)

                time_taken_seconds = time_end - time_start
                result = await _process_response_async(
                    r, step_config=None, time_taken_seconds=time_taken_seconds
                )

    return result.data


async def run_file_async(
    email_or_team: str,
    id: str | None = None,
    *,
    cache_max_age: int | None = None,
    _dtype_out_vector: str | None = None,
    _dtype_out_raster: str | None = None,
    _client_id: str | None = None,
    **params,
) -> pd.DataFrame | xr.Dataset | None:
    """
    Asynchronously executes a file-based UDF associated with the specific email and ID.

    This function constructs a URL to run a UDF on a server, allowing for output data type customization for vector and raster outputs and supporting additional parameters for the UDF execution. If no ID is provided, the user's email is used as the identifier.

    Args:
        email_or_team (str): The user's email address, used to identify the user's saved UDFs. If the ID is not provided, this email will also be used as the ID.
        id (Optional[str]): Unique identifier for the UDF. If None, the function fetches the user's email as the ID.
        cache_max_age (Optional[int]): The maximum age when returning a result from the cache.
        _dtype_out_vector (str): Desired data type for vector output, defaults to a predefined type.
        _dtype_out_raster (str): Desired data type for raster output, defaults to a predefined type.
        _client_id (Optional[str]): Client identifier for API usage. If None, a default or global client ID may be used.
        **params: Additional keyword arguments for the UDF execution.

    Returns:
        A coroutine that, when awaited, sends a request to the server to execute the UDF and returns the server's response. The format and content of the response depend on the UDF's implementation and the server's response format.
    """
    if id is None:
        id = email_or_team
        email_or_team = context_get_user_email()

    url = f"{make_realtime_url(_client_id)}/api/v1/run/udf/saved/{email_or_team}/{id}"
    return await _run_and_process_async(
        url=url,
        cache_max_age=cache_max_age,
        _dtype_out_vector=_dtype_out_vector,
        _dtype_out_raster=_dtype_out_raster,
        **params,
    )


async def run_shared_file_async(
    token: str,
    *,
    cache_max_age: int | None = None,
    _dtype_out_vector: str | None = None,
    _dtype_out_raster: str | None = None,
    **params,
) -> pd.DataFrame | xr.Dataset | None:
    """
    Asynchronously executes a shared file-based UDF using the specific access token.

    Constructs a URL to run an operation on a file accessible via a shared token, enabling customization of the output data types for vector and raster data. It accommodates additional parameters for the operation's execution.

    Args:
        token (str): A shared access token that authorizes the operation.
        cache_max_age (Optional[int]): The maximum age when returning a result from the cache.
        _dtype_out_vector (str): Desired data type for vector output, defaults to a predefined type.
        _dtype_out_raster (str): Desired data type for raster output, defaults to a predefined type.
        **params: Additional keyword arguments for the operation execution.

    Returns:
        A coroutine that, when awaited, sends a request to the server to execute the operation on the file and returns the server's response. The format and content of the response depend on the operation's implementation and the server's response format.
    """
    url = f"{make_shared_realtime_url(token)}/run/file"
    return await _run_and_process_async(
        url=url,
        cache_max_age=cache_max_age,
        _dtype_out_vector=_dtype_out_vector,
        _dtype_out_raster=_dtype_out_raster,
        _is_shared=True,
        **params,
    )


def _process_response(
    r: requests.Response,
    step_config: AnyJobStepConfig,
    time_taken_seconds: float,
    profile: bool = False,
) -> UdfEvaluationResult:
    result_content: bytes | None = None
    stdout: str | None = None
    stderr: str | None = None
    error_message: str | None = None
    error_lineno: int | None = None

    try:
        result_content = r.content
        # x-fused-metadata holds LogHandler as JSON, which contains stdout/stderr.
        _fused_metadata = r.headers.get("x-fused-metadata")
        fused_metadata = json.loads(_fused_metadata) if _fused_metadata else {}

        if profile:
            return fused_metadata.get("profile")

        # Extract stdout/stderr.
        stdout = fused_metadata.get("stdout")
        stderr = fused_metadata.get("stderr")

        # Extract exception details
        exception_class = fused_metadata.get("exception_class")
        has_exception = fused_metadata.get("has_exception", False)

        # Extract udf.
        udf: AnyBaseUdf | None = None
        if step_config is not None:
            udf = step_config.udf

        # Extract error line, if exists.
        error_lineno = fused_metadata.get("lineno")

        if r.status_code == 200:
            # If the UDF returned None.
            if len(result_content) == 0:
                data = None

            # Else, process response output.
            elif r.headers["content-type"] == "image/png":
                data = deserialize_png(result_content)

            elif r.headers["content-type"] == "image/tiff":
                # TODO: Automatically display tiff?
                data = deserialize_tiff(r.content)

            elif r.headers["content-type"] == "application/json":
                data = deserialize_json(result_content)

            elif r.headers["content-type"] == "text/html":
                data = deserialize_html(result_content)

            elif r.headers["content-type"] == "application/zip":
                data = deserialize_zip(result_content)

            elif r.headers["content-type"] == "application/x-numpy-data":
                data = deserialize_npy(result_content)
            else:
                # assume parquet
                data = deserialize_parquet(result_content)

            cache_status = is_response_cached(r)
            return UdfEvaluationResult(
                data=data,
                udf=udf,
                time_taken_seconds=time_taken_seconds,
                stdout=stdout,
                stderr=stderr,
                error_message=error_message,
                error_lineno=error_lineno,
                has_exception=has_exception,
                exception_class=exception_class,
                is_cached=cache_status.is_cached,
                cache_source=cache_status.cache_source,
            )
        else:
            if "errormsg" in fused_metadata and fused_metadata["errormsg"]:
                error_message = f"The UDF returned the following error in line {fused_metadata.get('lineno')}:\n{fused_metadata['errormsg']}"
            elif "exception" in fused_metadata and fused_metadata["exception"]:
                error_message = fused_metadata["exception"]
            else:
                # No error message was returned, e.g. due to deserialization error
                try:
                    # Look for a "detail" field in the response payload
                    details_obj = json.loads(r.text)
                    error_message = details_obj["detail"]
                except:  # noqa: E722
                    error_message = r.text

            return UdfEvaluationResult(
                data=None,
                udf=udf,
                time_taken_seconds=time_taken_seconds,
                stdout=stdout,
                stderr=stderr,
                error_message=error_message,
                error_lineno=error_lineno,
                has_exception=has_exception,
                exception_class=exception_class,
            )
    except:  # noqa: E722
        r.raise_for_status()
        raise


async def _process_response_async(
    r,
    step_config: AnyJobStepConfig,
    time_taken_seconds: float,
) -> UdfEvaluationResult:
    result_content: bytes | None = None
    stdout: str | None = None
    stderr: str | None = None
    error_message: str | None = None
    error_lineno: int | None = None

    try:
        if r.status != 200 and r.status != 422:
            raise ValueError(await r.read())

        result_content = (
            await r.read() if not OPTIONS.pyodide_async_requests else await r.bytes()
        )
        # x-fused-metadata holds LogHandler as JSON, which contains stdout/stderr.
        _fused_metadata = r.headers.get("x-fused-metadata")
        fused_metadata = json.loads(_fused_metadata) if _fused_metadata else {}

        # Extract stdout/stderr.
        stdout = fused_metadata.get("stdout")
        stderr = fused_metadata.get("stderr")

        # Extract exception details
        exception_class = fused_metadata.get("exception_class")
        has_exception = fused_metadata.get("has_exception", False)

        # Extract udf.
        udf: AnyBaseUdf | None = None
        if step_config is not None:
            udf = step_config.udf

        # Extract error line, if exists.
        error_lineno = fused_metadata.get("lineno")

        if r.status == 200:
            # If the UDF returned None.
            if len(result_content) == 0:
                data = None

            # Else, process response output.
            elif r.headers["content-type"] == "image/png":
                data = deserialize_png(result_content)

            elif r.headers["content-type"] == "image/tiff":
                # TODO: Automatically display tiff?
                data = deserialize_tiff(r.content)

            elif r.headers["content-type"] == "application/json":
                data = deserialize_json(result_content)

            elif r.headers["content-type"] == "text/html":
                data = deserialize_html(result_content)

            elif r.headers["content-type"] == "application/zip":
                data = deserialize_zip(result_content)

            else:
                # assume parquet
                data = deserialize_parquet(result_content)

            cache_status = is_response_cached(r)
            return UdfEvaluationResult(
                data=data,
                udf=udf,
                time_taken_seconds=time_taken_seconds,
                stdout=stdout,
                stderr=stderr,
                error_message=error_message,
                error_lineno=error_lineno,
                has_exception=has_exception,
                exception_class=exception_class,
                is_cached=cache_status.is_cached,
                cache_source=cache_status.cache_source,
            )
        else:
            if "errormsg" in fused_metadata and fused_metadata["errormsg"]:
                error_message = f"The UDF returned the following error in line {fused_metadata.get('lineno')}:\n{fused_metadata['errormsg']}"
            elif "exception" in fused_metadata and fused_metadata["exception"]:
                error_message = fused_metadata["exception"]
            else:
                # No error message was returned, e.g. due to deserialization error
                try:
                    # Look for a "detail" field in the response payload
                    details_obj = json.loads(result_content)
                    error_message = details_obj["detail"]
                except:  # noqa: E722
                    error_message = result_content.decode()

            return UdfEvaluationResult(
                data=None,
                udf=udf,
                time_taken_seconds=time_taken_seconds,
                stdout=stdout,
                stderr=stderr,
                error_message=error_message or "Unknown error occured",
                error_lineno=error_lineno,
                has_exception=has_exception,
                exception_class=exception_class,
            )
    except:  # noqa: E722
        r.raise_for_status()
        raise
