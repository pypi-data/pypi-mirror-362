"""
The public api of leaky. Functions in this module are imported into the main
`__init__.py` file, along with the interfaces defined in `interface.py`.
"""

import functools
from typing import Any, Callable, Dict

from leaky.interface import LeakMonitor
from leaky.monitors import LeakMonitorImpl, LeakMonitorThread
from leaky.options import Options
from leaky.output import get_output_writer
from leaky.reports import get_report_writer


def start(max_object_lifetime: float, **kwargs: Dict[str, Any]) -> None:
    """
    Starts monitoring for memory leaks. A summary of potential leaks will be printed to the
    console every `max_object_lifetime` seconds.

    :param max_object_lifetime: The maximum time in seconds that an object can live before
    it is considered a potential leak.
    :param kwargs: Additional options. See the `leaky.Options` class for more details.
    """
    options = _create_options(kwargs)
    leak_monitor_thread = LeakMonitorThread(
        max_object_lifetime=max_object_lifetime,
        writer=get_output_writer(options=options),
        report_writer=get_report_writer(options=options),
        options=options,
    )
    leak_monitor_thread.start()


def leak_monitor(
    warmup_calls: int = 1, calls_per_report: int = 1, **kwargs: Dict[str, Any]
) -> Callable[[Any], Any]:
    """
    Decorator to monitor for memory leaks.

    After the decorated function has been called `warmup_calls` times, a memory leak report
    is generated every `calls_per_report` calls to the decorated function. The report
    identifies potential memory leaks that have occurred since the previous report.

    The `calls_per_report` parameter can be changed if data created by the decorated function
    is permitted to live for a certain number of calls.

    The `warmup_calls` parameter can be changed if data is created on initial calls to the
    decorated function, but not changed after that.

    The behavior of the decorator can be controlled by passing keyword arguments to the
    decorator. See the `leaky.Options` class for more details.
    """

    def decorator_func(func: Any) -> Callable[[Any], Any]:
        monitor = create_leak_monitor(
            warmup_calls=warmup_calls, calls_per_report=calls_per_report, **kwargs
        )

        @functools.wraps(func)
        def wrapper(*inner_args: Any, **inner_kwargs: Any) -> Any:
            with monitor:
                return func(*inner_args, **inner_kwargs)

        return wrapper

    return decorator_func


def create_leak_monitor(
    warmup_calls: int = 1,
    calls_per_report: int = 1,
    **kwargs: Dict[str, Any],
) -> LeakMonitor:
    """
    Creates a monitor for memory leaks. The *second* time that the monitor instance is called
    as a context manager, a summary of potential leaks is written to the output.
    """
    options = _create_options(kwargs)
    return LeakMonitorImpl(
        writer=get_output_writer(options=options),
        report_writer=get_report_writer(options=options),
        warmup_calls=warmup_calls,
        calls_per_report=calls_per_report,
        options=options,
    )


def _create_options(kwargs: Dict[str, Any]) -> Options:
    return Options(**kwargs)
