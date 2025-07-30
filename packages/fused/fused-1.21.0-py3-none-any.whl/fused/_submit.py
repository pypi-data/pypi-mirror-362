import concurrent.futures
import json
import time
import warnings
from collections import defaultdict
from datetime import datetime, timedelta
from math import floor
from types import FunctionType
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    List,
    Literal,
    Optional,
    Tuple,
    Union,
    overload,
)

from requests.exceptions import ReadTimeout

from fused._optional_deps import HAS_PANDAS, PD_DATAFRAME
from fused._options import options as OPTIONS
from fused._run import ResultType
from fused._run import run as fused_run
from fused._udf import udf as fused_udf
from fused.models.udf import Udf
from fused.types import UdfRuntimeError
from fused.warnings import (
    FusedDeprecationWarning,
)

if TYPE_CHECKING:
    import pandas as pd


Status = Literal["cancelled", "running", "timeout", "error", "success", "pending"]
STATUS_NOT_FINISHED = ("running", "pending")
STATUS_FAILED = ("error", "timeout")


def _coerce_hashable(df: "pd.DataFrame"):
    """Make the values in the DataFrame hashable.
    E.g. Python `list` cannot be hashed."""

    for index in df.index:
        for column in df.columns:
            existing_value = df.loc[index, column]

            if isinstance(existing_value, list):
                # list we know a way to make it a hashable type
                existing_value = tuple(existing_value)

            try:
                # Some other types like `dict` we don't have a strategy
                # for, so instead try coercing to json.
                hash(existing_value)
            except TypeError:
                existing_value = json.dumps(existing_value)

            df.at[index, column] = existing_value

    return df


class Future:
    # or `Job`, `JobResult`, `Task`, ...

    def __init__(self, future, index, args):
        self._future: concurrent.futures.Future = future
        self._index = index
        self._args = args
        self._started_at = None
        self._ended_at = None

    def time(self) -> Optional[timedelta]:
        """How long this future took to complete, or None
        if the future is not complete."""
        if self._started_at is None or self._ended_at is None:
            return None
        return self._ended_at - self._started_at

    def done(self) -> bool:
        return self._future.done()

    def result(self):
        response = self._future.result()
        if isinstance(response, Exception):
            raise response
        if response.error_message is not None:
            raise self.exception()
        return response.data

    def exception(self) -> Optional[Exception]:
        try:
            response = self._future.result()
        except concurrent.futures.CancelledError as e:
            return e
        if isinstance(response, Exception):
            return response
        if response.error_message is not None:
            return UdfRuntimeError(
                f"[Run #{self._index} {self._args}] {response.error_message}",
                child_exception_class=response.exception_class,
            )
        return self._future.exception()

    def logs(self) -> str:
        response = self._future.result()
        if isinstance(response, Exception):
            return str(response)
        out = ""
        if response.stdout:
            out += "stdout\n------\n" + response.stdout
        if response.stderr:
            out += "\nstderr\n------\n" + response.stderr
        return out

    def status(self) -> Status:
        if self._future.cancelled():
            return "cancelled"
        elif self._future.running():
            return "running"
        elif self._future.done():
            exc = self.exception()
            if exc:
                if isinstance(
                    exc, ReadTimeout
                ) or "504 Server Error: Gateway Timeout" in str(exc):
                    return "timeout"
                return "error"
            return "success"  # or "finished"?
        else:
            return "pending"

    def __repr__(self) -> str:
        return f"<fused.Future [status: {('done - ' if self.done() else '') + self.status()}]>"


class JobPool:
    # or `Futures`, `PoolRunner`, etc

    """
    Pool of UDF runs. Don't use this class directly, use `fused.submit` instead.
    """

    def __init__(
        self,
        udf,
        arg_list,
        kwargs=None,
        engine="remote",
        max_workers=None,
        max_retry=2,
        before_run=None,
        wait_sleep=0.01,
        before_submit=0.01,
    ):
        self.udf = udf
        self.arg_list = arg_list
        self.n_jobs = len(self.arg_list)
        self._kwargs = kwargs or {}
        self._engine = engine
        self._pool = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)
        self._max_retry = max_retry
        self._before_run = before_run
        self._wait_sleep = wait_sleep
        self._before_submit = before_submit
        self._restarted_at = None
        self._started_at = None
        self._cancel_retry = False

    def _create_future(self, index, args) -> Future:
        future = Future(None, index, args)

        def _run(args):
            # currently we have to add a small delay between starting the UDF runs
            # to avoid overloading the server
            if self._before_run is not None:
                time.sleep(self._before_run)

            try:
                future._started_at = datetime.now()

                return fused_run(
                    self.udf,
                    engine=self._engine,
                    _return_response=True,
                    max_retry=self._max_retry,
                    _cancel_callback=lambda: self._cancel_retry,
                    **args,
                    **self._kwargs,
                )
            except Exception as exc:
                # ReadTime or HTTPError can happen on time-out or other server error
                return exc
            finally:
                future._ended_at = datetime.now()

        if self._before_submit:
            time.sleep(self._before_submit)

        future._future = self._pool.submit(_run, args)

        return future

    def _start_jobs(self):
        self._started_at = datetime.now()
        self._futures = [
            self._create_future(index, args) for index, args in enumerate(self.arg_list)
        ]

    def _get_status(self) -> List[bool]:
        return [f.done() for f in self._futures]

    def _status_counts(self) -> Dict[Status, int]:
        counts = defaultdict(int)
        for f in self._futures:
            counts[f.status()] += 1

        # TODO: always sort counts keys by status order
        return counts

    def _status_message(self) -> str:
        counts = self._status_counts()

        message_parts = []
        for status in ("running", "timeout", "error", "success", "pending"):
            c = counts[status]
            if c:
                message_parts.append(f"{c} {status}")

        if len(message_parts) == 0:
            return "empty"

        return ", ".join(message_parts)

    def _get_progress(self) -> Tuple[int, str]:
        # floor as to not show 100 if not every one is actually done
        percentage = floor(sum(self._get_status()) / self.n_jobs * 100)
        return percentage, f"{sum(self._get_status())}/{self.n_jobs}"

    def retry(self):
        """Rerun any tasks in error or timeout states. Tasks are rerun in the same pool."""
        old_futures = self._futures

        def _create_new_future(index, args):
            if old_futures[index].status() in ("error", "timeout"):
                return self._create_future(index, args)
            return old_futures[index]

        self._restarted_at = datetime.now()
        self._futures = [
            _create_new_future(index, args) for index, args in enumerate(self.arg_list)
        ]

    def cancel(self, wait: bool = False):
        """Cancel any pending (not running) tasks.

        Note it will not be possible to retry on the same JobPool later."""
        # Signal running tasks to stop retrying
        self._cancel_retry = True

        self._pool.shutdown(wait=wait, cancel_futures=True)
        counts = self._status_counts()
        if not wait:
            message = f"{counts['cancelled']} task(s) cancelled successfully"
            if counts["running"]:
                message += f", {counts['running']} task(s) already in progress and can not be cancelled."
            print(message)

    def total_time(self, since_retry: bool = False) -> timedelta:
        """Returns how long the entire job took.

        If only partial results are available, returns based on the last task to have been completed.
        """
        started_at = (
            self._restarted_at
            if since_retry and self._restarted_at is not None
            else self._started_at
        )
        if started_at is None:
            raise ValueError("JobPool has not been started")
        all_result_at = [f._ended_at for f in self._futures if f._ended_at is not None]
        if not len(all_result_at):
            raise ValueError("No result is available yet")
        last_result_at = max(all_result_at)
        return last_result_at - self._started_at

    def times(self) -> list[Optional[timedelta]]:
        """Time taken for each task.

        Incomplete tasks will be reported as None."""
        return [f.time() for f in self._futures]

    def done(self) -> bool:
        """True if all tasks have finished, regardless of success or failure."""
        return all(fut.done() for fut in self._futures)

    def all_succeeded(self) -> bool:
        """True if all tasks finished with success"""
        return all(f.status() == "success" for f in self._futures)

    def any_failed(self) -> bool:
        """True if any task finished with an error"""
        return any(f.status() in ("error", "timeout") for f in self._futures)

    def any_succeeded(self) -> bool:
        """True if any task finished with success"""
        return any(f.status() == "success" for f in self._futures)

    def arg_df(self):
        """The arguments passed to runs as a DataFrame"""
        if not HAS_PANDAS:
            raise ImportError("pandas is required to use this method")

        import pandas as pd

        return pd.DataFrame(self.arg_list)

    def status(self):
        """Return a Series indexed by status of task counts"""
        return self.df().value_counts("status")

    def wait(self):
        """Wait until all jobs are finished

        Use fused.options.show.enable_tqdm to enable/disable tqdm.
        Use pool._wait_sleep to set if sleep should occur while waiting.
        """

        def _noop(*args, **kwargs):
            pass

        after = _noop
        update = _noop
        if OPTIONS.show.enable_tqdm:
            from tqdm.auto import tqdm

            t = tqdm(total=self.n_jobs, bar_format="{l_bar}{bar} | {n_fmt}/{total_fmt}")

            def _tqdm_after():
                t.update(self.n_jobs - t.n)
                t.close()

            after = _tqdm_after
            update = lambda n_done: t.update(n_done - t.n)

        while not self.done():
            n_done = sum(self._get_status())
            update(n_done)
            if self._wait_sleep is not None:
                time.sleep(self._wait_sleep)

        after()

    def tail(self, stop_on_exception=False):
        """Wait until all jobs are finished, printing statuses as they become available.

        This is useful for interactively watching for the state of the pool.

        Use pool._wait_sleep to set if sleep should occur while waiting.
        """
        seen = set(self.results_now(return_exceptions=not stop_on_exception).keys())
        if len(seen):
            print(self._status_message())

            if len(seen) == len(self._futures):
                # Nothing left to tail
                return

        while len(seen) != len(self._futures):
            done = self.results_now(return_exceptions=not stop_on_exception)
            for new_key in done.keys():
                if new_key not in seen:
                    seen.add(new_key)
                    # TODO: Logger support, rather than print statement?
                    print(
                        f"[{datetime.now()}] Run #{new_key} {self._futures[new_key]._args} {self._futures[new_key].status()} ({self._status_message()})"
                    )

            if self._wait_sleep is not None:
                time.sleep(self._wait_sleep)

        print(f"End of tail\n{self._status_message()}")

    def results(self, return_exceptions=False) -> List[Any]:
        """Retrieve all results of the job.

        Results are ordered by the order of the args list."""
        results = []
        for fut in self._futures:
            try:
                results.append(fut.result())
            except Exception:
                if return_exceptions:
                    results.append(fut.exception())
                else:
                    raise
        return results

    def results_now(self, return_exceptions=False) -> Dict[int, Any]:
        """Retrieve the results that are currently done.

        Results are indexed by position in the args list."""
        results = {}
        for index, fut in enumerate(self._futures):
            if fut.done():
                try:
                    results[index] = fut.result()
                except Exception:
                    if return_exceptions:
                        results[index] = fut.exception()
                    else:
                        raise
        return results

    def df(
        self,
        status_column: Optional[str] = "status",
        result_column: Optional[str] = "result",
        time_column: Optional[str] = "time",
        logs_column: Optional[str] = "logs",
        exception_column: Optional[str] = None,
        include_exceptions: bool = True,
    ):
        """
        Get a DataFrame of results as they are currently.
        The DataFrame will have columns for each argument passed, and columns for:
        `status`, `result`, `time`, `logs` and optionally `exception`.
        """
        if not HAS_PANDAS:
            raise ImportError("pandas is required to use this method")

        import pandas as pd

        results_df = pd.DataFrame(self.arg_list)
        status_list = [f.status() for f in self._futures]
        if status_column:
            results_df[status_column] = status_list

        if time_column:
            time_list = [None] * len(self._futures)
            for i, fut in enumerate(self._futures):
                t = fut.time()
                if t is not None:
                    time_list[i] = t.total_seconds()

            results_df[time_column] = pd.Series(time_list, dtype=float)

        if result_column:
            result_list = [None] * len(self._futures)
            for i, fut in enumerate(self._futures):
                if status_list[i] not in STATUS_NOT_FINISHED:
                    try:
                        res = fut.result()
                    except Exception:
                        res = fut.exception() if include_exceptions else None

                    result_list[i] = res

            results_df[result_column] = result_list

        if logs_column:
            logs_list = [None] * len(self._futures)
            for i, fut in enumerate(self._futures):
                if status_list[i] not in STATUS_NOT_FINISHED:
                    logs_list[i] = fut.logs()

            results_df[logs_column] = logs_list

        if exception_column:
            results_df[exception_column] = [fut.exception() for fut in self._futures]

        return results_df

    def get_status_df(self):
        warnings.warn(
            "the 'get_status_df()' method is deprecated, use '.df()' instead.",
            FusedDeprecationWarning,
        )
        return self.df()

    def get_results_df(self, ignore_exceptions=False):
        warnings.warn(
            "the 'get_results_df()' method is deprecated, use '.df()' instead.",
            FusedDeprecationWarning,
        )
        self.wait()
        return self.df(include_exceptions=not ignore_exceptions)

    def errors(self) -> Dict[int, Exception]:
        """Retrieve the results that are currently done and are errors.

        Results are indexed by position in the args list."""
        errors = {}
        for index, fut in enumerate(self._futures):
            if fut.status() in STATUS_FAILED:
                errors[index] = fut.exception()
        return errors

    def first_error(self) -> Optional[Exception]:
        """Retrieve the first (by order of arguments) error result, or None."""
        for fut in self._futures:
            if fut.status() in STATUS_FAILED:
                return fut.exception()

        return None

    def logs(self) -> list[str]:
        """Logs for each task.

        Incomplete tasks will be reported as None."""
        return [
            (f.logs() if f.status() not in STATUS_NOT_FINISHED else None)
            for f in self._futures
        ]

    def first_log(self) -> Optional[str]:
        """Retrieve the first (by order of arguments) logs, or None."""
        for f in self._futures:
            if f.status() not in STATUS_NOT_FINISHED:
                return f.logs()

    def success(self) -> Dict[int, Any]:
        """Retrieve the results that are currently done and are successful.

        Results are indexed by position in the args list."""
        success = {}
        for index, fut in enumerate(self._futures):
            if fut.status() in ("success",):
                success[index] = fut.result()
        return success

    def pending(self) -> Dict[int, Any]:
        """Retrieve the arguments that are currently pending and not yet submitted."""
        pending = {}
        for index, fut in enumerate(self._futures):
            if fut.status() in ("pending",):
                pending[index] = fut._args
        return pending

    def running(self) -> Dict[int, Any]:
        """Retrieve the results that are currently running."""
        running = {}
        for index, fut in enumerate(self._futures):
            if fut.status() in ("running",):
                running[index] = fut._args
        return running

    def cancelled(self) -> Dict[int, Any]:
        """Retrieve the arguments that were cancelled and not run."""
        cancelled = {}
        for index, fut in enumerate(self._futures):
            if fut.status() in ("cancelled",):
                cancelled[index] = fut._args
        return cancelled

    def collect(self, ignore_exceptions=False, flatten=True):
        """Collect all results into a DataFrame"""
        if not HAS_PANDAS:
            raise ImportError("pandas is required to use this method")

        import pandas as pd

        results = self.results(return_exceptions=ignore_exceptions)
        mask = [not isinstance(r, Exception) for r in results]
        results = dict(
            res
            for res in zip(range(self.n_jobs), results)
            if not isinstance(res[1], Exception)
        )

        results_pandas = all(isinstance(res, pd.DataFrame) for res in results.values())
        if results_pandas and len(results) and flatten:
            # TODO: flatten can un-occur depending on results, this seems wrong
            results_df = pd.concat(results)
        else:
            results_df = pd.DataFrame({"result": pd.Series(results)})
            results_df.index = pd.MultiIndex.from_product([results_df.index])

        args_df = pd.DataFrame(self.arg_list)
        args_df = args_df[mask]

        _coerce_hashable(args_df)

        # combine concatenated results with arguments as prepended index levels
        assert len(results_df.index.levels[0]) == len(args_df)
        args_index = pd.MultiIndex.from_frame(args_df)
        args_codes = [c.take(results_df.index.codes[0]) for c in args_index.codes]
        new_idx = pd.MultiIndex(
            levels=list(args_index.levels) + results_df.index.levels[1:],
            codes=args_codes + results_df.index.codes[1:],
            names=list(args_df.columns) + results_df.index.names[1:],
        )
        if new_idx.nlevels == 1:
            new_idx = new_idx.get_level_values(0)
        results_df.index = new_idx
        return results_df

    def __getitem__(self, idx: int) -> Future:
        return self._futures[idx]

    def __len__(self) -> int:
        return self.n_jobs

    def __repr__(self) -> str:
        return f"<JobPool with {self.n_jobs} jobs [{self._status_message()}]>"

    def _repr_html_(self) -> str:
        # TODO we could provide a more informative repr in notebooks (e.g. showing
        # a table of the individual jobs and their status?)
        counts = self._status_counts()
        status_table_data = [
            f"<tr><td>{status}</td><td>{count}</td></tr>"
            for status, count in counts.items()
        ]
        return f"<table><tr><th>Status</th><th>Count</th></tr>{''.join(status_table_data)}</table>"


def _validate_arg_list(arg_list, udf):
    if HAS_PANDAS and isinstance(arg_list, PD_DATAFRAME):
        return arg_list.to_dict(orient="records")

    if not len(arg_list):
        raise ValueError("arg_list must be a non-empty list")
    if not isinstance(arg_list[0], dict):
        if not isinstance(udf, Udf):
            raise ValueError(
                "arg_list must be a list of dictionaries. A simple list to pass "
                "as first positional argument is only supported for UDF objects."
            )
        if udf._parameter_list is None:
            # TODO: Run _parameter_list detection here
            raise NotImplementedError(
                "arg_list must be a list of dictionaries. Could not detect the first "
                "positional argument name."
            )
        if len(udf._parameter_list) == 0:
            raise ValueError(
                "arg_list must be a list of dictionaries. UDF does not accept any arguments."
            )
        name = udf._parameter_list[0]
        arg_list = [{name: arg} for arg in arg_list]

    return arg_list


@overload
def submit(
    udf,
    arg_list,
    /,
    *,
    engine: Optional[Literal["remote", "local"]] = "remote",
    max_workers: Optional[int] = None,
    max_retry: int = 2,
    debug_mode: Literal[False] = False,
    collect: Literal[True] = True,
    **kwargs,
) -> "pd.DataFrame": ...


@overload
def submit(
    udf,
    arg_list,
    /,
    *,
    engine: Optional[Literal["remote", "local"]] = "remote",
    max_workers: Optional[int] = None,
    max_retry: int = 2,
    debug_mode: Literal[False] = False,
    collect: Literal[False] = False,
    **kwargs,
) -> JobPool: ...


@overload
def submit(
    udf,
    arg_list,
    /,
    *,
    engine: Optional[Literal["remote", "local"]] = "remote",
    max_workers: Optional[int] = None,
    max_retry: int = 2,
    debug_mode: Literal[True] = True,
    collect: Literal[True] = True,
    **kwargs,
) -> ResultType: ...


def submit(
    udf,
    arg_list,
    /,
    *,
    engine: Optional[Literal["remote", "local"]] = "remote",
    max_workers: Optional[int] = None,
    max_retry: int = 2,
    debug_mode: bool = False,
    collect: bool = True,
    cache_max_age: Optional[str] = None,
    cache: bool = True,
    ignore_exceptions: bool = False,
    flatten: bool = True,
    _before_run: Optional[float] = None,
    _before_submit: Optional[float] = 0.01,
    **kwargs,
) -> Union[JobPool, ResultType, "pd.DataFrame"]:
    """
    Executes a user-defined function (UDF) multiple times for a list of input
    parameters, and return immediately a "lazy" JobPool object allowing
    to inspect the jobs and wait on the results.

    See `fused.run` for more details on the UDF execution.

    Args:
        udf: the UDF to execute.
            See `fused.run` for more details on how to specify the UDF.
        arg_list: a list of input parameters for the UDF. Can be specified as:
            - a list of values for parametrizing over a single parameter, i.e.
              the first parameter of the UDF
            - a list of dictionaries for parametrizing over multiple parameters
            - A DataFrame for parametrizing over multiple parameters where each
              row is a set of parameters

        engine: The execution engine to use. Defaults to 'remote'.
        max_workers: The maximum number of workers to use. Defaults to 32.
        max_retry: The maximum number of retries for failed jobs. Defaults to 2.
        debug_mode: If True, executes only the first item in arg_list directly using
            `fused.run()`, useful for debugging UDF execution. Default is False.
        collect: If True, waits for all jobs to complete and returns the collected DataFrame
            containing the results. If False, returns a JobPool object, which is non-blocking
            and allows you to inspect the individual results and logs.
            Default is True.
        cache_max_age: The maximum age when returning a result from the cache.
            Supported units are seconds (s), minutes (m), hours (h), and days (d)
            (e.g. “48h”, “10s”, etc.).
            Default is `None` so a UDF run with `fused.run()` will follow
            `cache_max_age` defined in `@fused.udf()` unless this value is changed.
        cache: Set to False as a shortcut for `cache_max_age='0s'` to disable caching.
        ignore_exceptions: Set to True to ignore exceptions when collecting results.
            Runs that result in exceptions will be silently ignored. Defaults to False.
        flatten: Set to True to receive a DataFrame of results, without nesting of a
            `results` column, when collecting results. When False, results will be nested
            in a `results` column. If the UDF does not return a DataFrame (e.g. a string
            instead,) results will be nested in a `results` column regardless of this setting.
            Defaults to True.
        **kwargs: Additional (constant) keyword arguments to pass to the UDF.

    Returns:
        JobPool

    Examples:
        Run a UDF multiple times for the values 0 to 9 passed to as the first
        positional argument of the UDF:
        ```py
        df = fused.submit("username@fused.io/my_udf_name", range(10))
        ```

        Being explicit about the parameter name:
        ```py
        df = fused.submit(udf, [dict(n=i) for i in range(10)])
        ```

        Get the pool of ongoing tasks:
        ```py
        pool = fused.submit(udf, [dict(n=i) for i in range(10)], collect=False)
        ```

    """
    if isinstance(udf, FunctionType):
        if udf.__name__ == "<lambda>":
            # This will not work correctly in fused.udf. If we find a way to parse just the AST
            # of the lambda (without any surrounding function call, assignment, etc.) then we can
            # support lambda here
            raise TypeError(
                """Lambda expressions cannot be passed into fused.submit(). Create a function with @fused.udf instead:
@fused.udf
def udf(x):
    return x

fused.submit(udf, arg_list)
"""
            )
        # TODO: Move this logic to fused.run?
        udf = fused_udf(udf)

    arg_list = _validate_arg_list(arg_list, udf)

    if cache_max_age is not None:
        kwargs["cache_max_age"] = cache_max_age
    if not cache:
        kwargs["cache"] = cache

    if debug_mode:
        if not collect:
            warnings.warn(
                "'debug_mode=True' and 'collect=False' are mutually exclusive (the "
                "result of the first run is always returned directly), and the collect "
                "keyword is ignored in this case."
            )
        return fused_run(udf, engine=engine, **arg_list[0], **kwargs)

    max_workers = min(max_workers or 32, 1024)

    job_pool = JobPool(
        udf,
        arg_list,
        kwargs,
        engine=engine,
        max_workers=max_workers,
        max_retry=max_retry,
        before_run=_before_run,
        before_submit=_before_submit,
    )
    job_pool._start_jobs()

    if collect:
        job_pool.wait()
        return job_pool.collect(ignore_exceptions=ignore_exceptions, flatten=flatten)
    else:
        return job_pool
