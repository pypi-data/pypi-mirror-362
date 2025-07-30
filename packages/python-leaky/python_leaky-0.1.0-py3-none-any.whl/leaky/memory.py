import os
import resource
from sys import platform

import psutil
from pydantic.dataclasses import dataclass

from leaky.base import LeakyCount
from leaky.reports import MemoryUsageOutput


@dataclass
class MemoryUsage:
    """
    Represents memory usage information at a particular point in time.
    """

    current_rss_bytes: int
    """
    The current resident set size (RSS) in bytes.
    """

    peak_rss_bytes: int | None
    """
    The peak resident set size (RSS) in bytes. This is `None` if not supported on the
    current platform.
    """

    system_percent_used: float
    """
    The percent of total physical system memory used.
    """

    iteration_number: int
    """
    The iteration number that this memory usage record was generated.
    """


def get_memory_usage_output(previous: MemoryUsage | None, new: MemoryUsage) -> MemoryUsageOutput:
    """
    Gets a `Output` object representing the memory usage. This includes the difference
    between the current and previous usage if the previous usage is provided.
    """
    return MemoryUsageOutput(
        current_rss_bytes=new.current_rss_bytes,
        peak_rss_bytes=new.peak_rss_bytes,
        current_rss_diff=new.current_rss_bytes - previous.current_rss_bytes if previous else None,
        system_percent_used=new.system_percent_used,
        peak_rss_diff=new.peak_rss_bytes - previous.peak_rss_bytes
        if previous and previous.peak_rss_bytes and new.peak_rss_bytes
        else None,
        diff_from_iteration=previous.iteration_number if previous else None,
    )


def get_memory_usage(iteration: LeakyCount) -> MemoryUsage:
    """
    Gets memory usage information.
    """
    pid = os.getpid()
    p = psutil.Process(pid)
    memory_info = p.memory_info()
    if "linux" in platform:
        # On Linux ru_maxrss is in kilobytes.
        peak_rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024
    elif "darwin" in platform:
        # On Mac ru_maxrss is in bytes.
        peak_rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    elif "win32" in platform:
        # On Windows, peak_wset should be the same as the max RSS on Linux and Mac.
        # This is based on https://psutil.readthedocs.io/en/latest/#psutil.Process.memory_info
        # and the Windows PROCESS_MEMORY_COUNTERS_EX structure. The docs for this
        # say it is "the peak working set size, in bytes".
        peak_rss = memory_info.peak_wset
    else:
        peak_rss = None
    rss = memory_info.rss
    return MemoryUsage(
        current_rss_bytes=rss,
        peak_rss_bytes=peak_rss,
        system_percent_used=p.memory_percent(memtype="rss"),
        iteration_number=int(iteration),
    )
