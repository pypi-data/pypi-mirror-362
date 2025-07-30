import os
import tempfile
import warnings
from pathlib import Path
from typing import Dict, List, Literal, Optional, Tuple, Union
from urllib.parse import urlparse

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StrictBool,
    StrictStr,
    field_serializer,
    field_validator,
    model_validator,
)

from ._global_api import reset_api
from .warnings import FusedIgnoredWarning, FusedImportWarning

DEV_DEFAULT_BASE_URL = "http://localhost:8783/v1"
PROD_DEFAULT_BASE_URL = "https://www.fused.io/server/v1"
STAGING_DEFAULT_BASE_URL = "https://www-staging.fused.io/server/v1"
UNSTABLE_DEFAULT_BASE_URL = "https://unstable.fused.io/server/v1"
DEV_PR_DEFAULT_BASE_URL = "https://{}.dev.fusedlabs.io/server/v1"


OPTIONS_PATH = Path("~/.fused/settings.toml").expanduser()
"""First choice for where to find settings"""
OPTIONS_JSON_PATH = Path("~/.fused/settings.json").expanduser()
"""Second choice for where to find settings"""

StorageStr = Literal["auto", "mount", "local", "object"]


class OptionsBaseModel(BaseModel):
    def __dir__(self) -> List[str]:
        # Provide method name lookup and completion. Only provide 'public'
        # methods.
        # This enables autocompletion
        # Pydantic methods to remove in __dir__
        PYDANTIC_METHODS = {
            "Config",
            "construct",
            "copy",
            "from_orm",
            "json",
            "parse_file",
            "parse_obj",
            "schema",
            "schema_json",
            "update_forward_refs",
            "validate",
            "model_validate",
            "model_dump_json",
        }

        normal_dir = {
            name
            for name in dir(type(self))
            if (not name.startswith("_") and name not in PYDANTIC_METHODS)
        }
        pydantic_fields = set(self.model_fields.keys())
        return sorted(normal_dir | pydantic_fields)

    def _repr_html_(self) -> str:
        # Circular import because the repr needs the options
        from fused._formatter.formatter_options import fused_options_repr

        return fused_options_repr(self)


class AuthOptions(OptionsBaseModel):
    authorize_url: str = "https://dev-tjcykxcetrz6bps6.us.auth0.com/authorize"
    """The authorize URL is used for the initial login flow. This is intended to be opened in
    the user's web browser for them to sign in."""

    oauth_token_url: str = "https://dev-tjcykxcetrz6bps6.us.auth0.com/oauth/token"
    """The token url is used for programmatic access to generate access and refresh tokens."""

    logout_url: str = "https://dev-tjcykxcetrz6bps6.us.auth0.com/oidc/logout"

    # The client id, client secret, and audience identifies a specific application and API
    client_id: str = "CXiwKZQmmyo0rqXZY7pzBgfsF7AL2A9l"
    client_secret: str = (
        "FVNz012KgNmqITYnCCOM8Q1Nt81W_DO4SeCRgVsftREKTWpzZU522nia5TdSNv8h"
    )
    audience: str = "fused-python-api"

    local_redirect_url: str = "http://localhost:3000"
    """This redirect uri is passed to the authorize URL as a url parameter. This localhost
    uri is used to intercept the "code" generated from the authorization"""

    scopes: List[str] = ["openid", "email", "name", "offline_access"]
    """The offline_access scope is necessary to be able to fetch refresh tokens
    The other scopes are useful to access identifying information in the retrieved JWT"""

    credentials_path: str = "~/.fused/credentials"
    """The path where the refresh token is saved on disk. Will be user-expanded to resolve ~."""


class ShowOptions(OptionsBaseModel):
    """Options for showing debug information"""

    open_browser: Optional[StrictBool] = None
    """Whether to open a local browser window for debug information"""
    show_widget: Optional[StrictBool] = None
    """Whether to show debug information in an IPython widget"""

    enable_tqdm: StrictBool = True
    """Whether to show tqdm-based progress information"""


def _cache_directory(object_cache_storage: bool) -> Path:
    return _get_cache_dir(object_cache_storage, "auto")


def _data_directory(object_cache_storage: bool) -> Path:
    return _get_data_dir(object_cache_storage, "auto")


def _get_data_dir(object_cache_storage: bool, storage: StorageStr = "auto") -> Path:
    base_path = _get_writable_dir(object_cache_storage, storage)
    # Keep consistency with job2 data_path where return can be /mount/tmp or /tmp
    # TODO: Maybe unify to single common dir - /mount/data and /tmp/data
    if "mount" in str(base_path):
        return base_path / "tmp"
    else:
        return base_path


def _get_cache_dir(object_cache_storage: bool, storage: StorageStr = "auto") -> Path:
    base_path = _get_writable_dir(object_cache_storage, storage)
    return base_path / "cached_data"


def _get_writable_dir(object_cache_storage: bool, storage: StorageStr = "auto") -> Path:
    mount_path = Path("/mount")
    temp_dir = Path(tempfile.gettempdir())

    if storage == "auto":
        if object_cache_storage:
            base_path = Path("/")
        # Cache in mounted drive if available & writable, else cache in /tmp
        elif is_path_writable(mount_path):
            base_path = mount_path
        else:
            base_path = temp_dir
    elif storage == "mount":
        base_path = mount_path
    elif storage == "local":
        base_path = temp_dir
    elif storage == "object":
        base_path = Path("/")
    else:
        raise ValueError(storage)

    return base_path


def is_path_writable(p: Path) -> bool:
    return p.exists() and os.access(p, os.W_OK)


class Options(OptionsBaseModel):
    base_url: str = PROD_DEFAULT_BASE_URL
    """Fused API endpoint"""

    auth: AuthOptions = Field(default_factory=AuthOptions)
    """Options for authentication."""

    show: ShowOptions = Field(default_factory=ShowOptions)
    """Options for object reprs and how data are shown for debugging."""

    max_workers: int = 16
    """Maximum number of threads, when multithreading requests"""

    request_timeout: Union[Tuple[float, float], float, None] = 120
    """Request timeout for the Fused service

    May be set to a tuple of connection timeout and read timeout"""

    request_max_retries: int = 5
    """Maximum number of retries for API requests"""

    request_retry_base_delay: float = 1.0
    """Base delay before retrying a API request in seconds"""

    realtime_client_id: Optional[StrictStr] = None
    """Client ID for realtime service."""

    max_recursion_factor: int = 5
    """Maximum recursion factor for UDFs. This is used to limit the number of
    recursive calls to UDFs. If a UDF exceeds this limit, an error will be raised."""

    save_user_settings: StrictBool = True
    """Save per-user settings such as credentials and environment IDs."""

    default_udf_run_engine: Optional[StrictStr] = None
    """Default engine to run UDFs, one of: "local" or "remote"."""

    default_validate_imports: StrictBool = False
    """Default for whether to validate imports in UDFs before `run_local`,
    `run_batch`."""

    prompt_to_login: StrictBool = False
    """Automatically prompt the user to login when importing Fused."""

    no_login: StrictBool = False
    """If set, Fused will not attempt to login automatically when needed."""

    pyodide_async_requests: StrictBool = False
    """If set, Fused is being called inside Pyodide and should use pyodide
    for async HTTP requests."""

    cache_directory: Path = None
    """The base directory for storing cached results. Note: if storage type is 'object', then this path is relative to
    fd_prefix."""

    data_directory: Path = None
    """The base directory for storing data results. Note: if storage type is 'object', then this path is relative to
    fd_prefix."""

    temp_directory: Path = Path(tempfile.gettempdir())
    """The base directory for storing temporary files."""

    never_import: StrictBool = False
    """Never import UDF code when loading UDFs."""

    gcs_secret: str = "gcs_fused"
    """Secret name for GCS credentials."""

    gcs_filename: str = "/tmp/.gcs.fused"
    """Filename for saving temporary GCS credentials to locally or in rt2 instance"""

    gcp_project_name: Optional[StrictStr] = None
    """Project name for GCS to use for GCS operations."""

    logging: StrictBool = Field(default=False, validate_default=True)
    """Control logging for Fused"""

    verbose_udf_runs: StrictBool = True
    """Whether to print logs from UDF runs by default"""

    default_run_headers: Optional[Dict[str, str]] = {"X-Fused-Cache-Disable": "true"}
    """(Advanced) Default headers to include with UDF run requests."""

    default_dtype_out_vector: StrictStr = "parquet"
    """Default transfer type for vector (tabular) data"""

    default_dtype_out_raster: StrictStr = "tiff"
    """Default transfer type for raster data"""

    fd_prefix: Optional[str] = None
    """If set, where fd:// scheme URLs will resolve to. By default will infer this from your user account."""

    verbose_cached_functions: StrictBool = True
    """Whether to print logs from cache decorated functions by default"""

    local_engine_cache: StrictBool = True
    """Enable UDF cache with local engine"""

    default_send_status_email: StrictBool = True
    """Whether to send a status email to the user when a job is complete."""

    cache_in_object_storage: StrictBool = False
    """Have data saved to object storage for cache_directory and data_directory based on fd_prefix"""

    @model_validator(mode="after")
    def _set_default_directories(self):
        if self.cache_directory is None:
            self.cache_directory = _cache_directory(self.cache_in_object_storage)
        if self.data_directory is None:
            self.data_directory = _data_directory(self.cache_in_object_storage)

        return self

    @field_validator("logging")
    @classmethod
    def _validate_logging(cls, v):
        from loguru import logger

        if v:
            logger.enable("fused")
        else:
            logger.disable("fused")

        return v

    @field_serializer("cache_directory")
    def _serialize_cache_directory(self, path: Path, _info) -> str:
        return str(path)

    @field_serializer("temp_directory")
    def _serialize_temp_directory(self, path: Path, _info) -> str:
        return str(path)

    @field_validator("base_url")
    @classmethod
    def _validate_base_url(cls, v):
        reset_api()
        return v

    @field_validator("auth")
    @classmethod
    def _validate_auth(cls, v):
        from fused._auth import AUTHORIZATION

        # reset to trigger re-authentication / loading from disk to ensure setting
        # the options.auth blow has effect
        AUTHORIZATION.reset()

        return v

    @field_validator("data_directory", mode="before")
    @classmethod
    def _validate_data_directory(cls, v, values):
        if not values.data["cache_in_object_storage"] and is_path_writable(Path(v)):
            return v
        else:
            return _data_directory(values.data["cache_in_object_storage"])

    @property
    def base_web_url(self):
        if self.base_url == STAGING_DEFAULT_BASE_URL:
            return "https://staging.fused.io"

        parts = urlparse(self.base_url)
        return "{scheme}://{netloc}".format(**parts._asdict())

    def save(self):
        """Save Fused options to `~/.fused/settings.toml`. They will be automatically
        reloaded the next time fused-py is imported.
        """
        try:
            import rtoml

            OPTIONS_PATH.parent.mkdir(parents=True, exist_ok=True)
            # None (null) will not be serialized correctly in toml, so exclude it.
            # Any option which can be None should be None by default. Some open options
            # don't do this; should be updated to not be Optional.
            rtoml.dump(
                self.model_dump(exclude_none=True, exclude_defaults=True), OPTIONS_PATH
            )
        except ImportError:
            warnings.warn(
                FusedImportWarning("rtoml is not installed so options are not saved")
            )

    def _to_toml(self) -> str:
        try:
            import rtoml

            return rtoml.dumps(
                self.model_dump(exclude_none=True, exclude_defaults=True)
            )
        except ImportError:
            warnings.warn(
                FusedImportWarning("rtoml is not installed so options are not saved")
            )

    model_config = ConfigDict(validate_assignment=True)


def _load_options():
    if OPTIONS_PATH.exists():
        try:
            import rtoml

            return Options.model_validate(rtoml.load(OPTIONS_PATH))
        except:  # noqa E722
            warnings.warn(
                FusedIgnoredWarning(
                    f"Settings file {OPTIONS_PATH} exists but could not be loaded."
                )
            )

    if OPTIONS_JSON_PATH.exists():
        try:
            import json

            with open(OPTIONS_JSON_PATH) as json_file:
                return Options.model_validate(json.load(json_file))
        except:  # noqa E722
            warnings.warn(
                FusedIgnoredWarning(
                    f"Settings file {OPTIONS_JSON_PATH} exists but could not be loaded."
                )
            )

    return Options()


options = _load_options()
"""List global configuration options.

This object contains a set of configuration options that control global behavior of the library. This object can be used to modify the options.

Examples:
    Change the `request_timeout` option from its default value to 120 seconds:
    ```py
    fused.options.request_timeout = 120
    ```
"""


def _dev_auth():
    auth = AuthOptions()
    auth.client_id = "K5XfH4xP6PQo6weGVvPYDUiLxGu7GMdb"
    auth.client_secret = (
        "sHh339I8c8bDEPXVMRHMi9rnSrwWtawBHW1588Rm9mqGTc8F5khtvpYOha6Bxk7P"
    )
    auth.audience = "fused-python-api"
    auth.oauth_token_url = "https://fused-dev.us.auth0.com/oauth/token"
    auth.authorize_url = "https://fused-dev.us.auth0.com/authorize"
    auth.credentials_path = "~/.fused/credentials-dev"
    return auth


def env(environment_name: Union[str, int]):
    """Set the environment."""
    if isinstance(environment_name, int) or environment_name.isnumeric():
        _env = DEV_PR_DEFAULT_BASE_URL.format(environment_name)
        options.auth = _dev_auth()
        setattr(options, "base_url", _env)
        return
    else:
        # reset auth options in case we are switching from a dev env
        options.auth = AuthOptions()

    if environment_name == "dev":
        _env = DEV_DEFAULT_BASE_URL
    elif environment_name == "stg" or environment_name == "staging":
        _env = STAGING_DEFAULT_BASE_URL
    elif environment_name == "prod":
        _env = PROD_DEFAULT_BASE_URL
    elif environment_name == "unstable":
        _env = UNSTABLE_DEFAULT_BASE_URL
    else:
        raise ValueError("Available options are `dev`, `stg`, `prod`, and `unstable`.")

    # setting this will cause the global API to be reset
    setattr(options, "base_url", _env)

    # Reset realtime_client_id since it should no longer be correct for a new env.
    setattr(options, "realtime_client_id", None)
