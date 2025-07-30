import gc
import time
from threading import Thread
from typing import Any

from leaky.base import LeakyCount
from leaky.interface import LeakMonitor
from leaky.options import Options
from leaky.output import OutputWriter
from leaky.reports import ReportWriter
from leaky.snapshots import (
    LeakySnapshotManager,
    _filter_default,
    _gc_and_get_objects,
    _LeakyObjectId,
    _LeakyObjectIds,
    generate_report,
)


class LeakMonitorImpl(LeakMonitor):
    """
    Context manager to monitor for memory leaks. The *second* time that the enclosed code
    is called, a summary of potential leaks will be printed to the console.
    """

    def __init__(
        self,
        writer: OutputWriter,
        report_writer: ReportWriter,
        warmup_calls: int,
        calls_per_report: int,
        options: Options,
    ) -> None:
        self._snapshot_manager = LeakySnapshotManager(report_writer.report_id)
        self._writer = writer
        self._warmup_calls = warmup_calls
        self._calls_per_report = calls_per_report
        self._options = options
        self._report_writer = report_writer
        self._call_count: LeakyCount = LeakyCount(0)
        self._report_iteration: LeakyCount = LeakyCount(0)
        self._calls_since_previous_report: LeakyCount = LeakyCount(0)
        self._object_ids_created_since_previous_report: _LeakyObjectIds = _LeakyObjectIds()
        self._object_ids_on_enter: _LeakyObjectIds | None = None

    def __enter__(self) -> None:
        """
        Enters the context manager.
        """
        self._call_count = LeakyCount(self._call_count + 1)
        if self._call_count > self._warmup_calls:
            self._calls_since_previous_report = LeakyCount(self._calls_since_previous_report + 1)
        all_objects = _gc_and_get_objects(
            max_untracked_search_depth=self._options.max_untracked_search_depth
        )
        # Only generate a snapshot after the warmup time, and if this is the first call
        # since the previous report.
        if self._call_count > self._warmup_calls and self._calls_since_previous_report == 1:
            # When this is used as a context manager, the previous usage is always None
            # when it is entered. When the context manager exits, the usage diff is calculated
            # as the diff between the entry and exit of the context manager.
            self._snapshot_manager.generate_new_snapshot(
                all_objects=all_objects, options=self._options
            )
        self._object_ids_on_enter = _LeakyObjectIds(
            _LeakyObjectId(id(obj))
            for obj in _filter_default(
                objects=all_objects,
                options=self._options,
            )
        )

    def __exit__(
        self, exc_type: type[BaseException] | None, exc_value: BaseException | None, traceback: Any
    ) -> None:
        """
        Exits the context manager.
        """
        # On the last warmup call, generate a report. The report will not contain any leaks,
        # but provides a baseline of memory usage.
        # Also generate a report if we have had at least _calls_per_report calls since the
        # previous report.
        all_objects = _gc_and_get_objects(
            max_untracked_search_depth=self._options.max_untracked_search_depth
        )
        assert self._object_ids_on_enter is not None
        # We only want to consider objects that were created within the function that is being
        # decorated. Update _object_ids_created_since_previous_report to include only these
        # objects.
        self._object_ids_created_since_previous_report.update(
            _LeakyObjectIds(
                _LeakyObjectId(id(obj))
                for obj in _filter_default(
                    objects=all_objects,
                    options=self._options,
                )
            )
            - self._object_ids_on_enter
        )
        if self._call_count == self._warmup_calls or (
            self._call_count > self._warmup_calls
            and self._calls_since_previous_report >= self._calls_per_report
        ):
            self._report_iteration = LeakyCount(self._report_iteration + 1)
            generate_report(
                snapshot_manager=self._snapshot_manager,
                all_objects=all_objects,
                writer=self._writer,
                report_writer=self._report_writer,
                options=self._options,
                iteration=self._report_iteration,
                include_object_ids=self._object_ids_created_since_previous_report,
                excluded_from_referrers=[
                    id(self._object_ids_created_since_previous_report),
                    id(self._object_ids_on_enter),
                ],
            )
            self._snapshot_manager.clear_snapshots()
            self._calls_since_previous_report = LeakyCount(0)
            self._object_ids_created_since_previous_report = _LeakyObjectIds()


class LeakMonitorThread(Thread):
    """
    Thread to monitor for memory leaks.
    """

    def __init__(
        self,
        max_object_lifetime: float,
        writer: OutputWriter,
        report_writer: ReportWriter,
        options: Options,
    ) -> None:
        super().__init__(daemon=True)
        # Use the max object lifetime as the startup delay. We might want to make this
        # independently configurable in the future.
        self._startup_delay = max_object_lifetime
        self._max_object_lifetime = max_object_lifetime
        self._snapshot_manager = LeakySnapshotManager(report_id=report_writer.report_id)
        self._writer = writer
        self._report_writer = report_writer
        self._options = options
        self._report_iteration: LeakyCount = LeakyCount(0)

    def run(self) -> None:
        time.sleep(self._startup_delay)
        while True:
            self._run_iteration()

    def _run_iteration(self) -> None:
        # The new iteration variable is created between the previous snapshot and
        # the report, so we need to be careful not to identify it as a leak.
        # That's why it's an instance of Iteration, rather than an int.
        self._report_iteration = LeakyCount(self._report_iteration + 1)
        generate_report(
            snapshot_manager=self._snapshot_manager,
            all_objects=_gc_and_get_objects(
                max_untracked_search_depth=self._options.max_untracked_search_depth
            ),
            writer=self._writer,
            report_writer=self._report_writer,
            options=self._options,
            iteration=self._report_iteration,
            include_object_ids=_LeakyObjectIds(),
            excluded_from_referrers=[],
        )
        self._snapshot_manager.generate_new_snapshot(
            all_objects=_gc_and_get_objects(
                max_untracked_search_depth=self._options.max_untracked_search_depth
            ),
            options=self._options,
        )
        # Sleep for the maximum object lifetime. This ensures that on the next
        # iteration we will have a snapshot that is at least as old as the max
        # object lifetime.
        time.sleep(self._max_object_lifetime)
        gc.collect()
