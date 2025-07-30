import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from typing import Any, Generator, Sequence, Type

import objsize
import referrers
from rich.panel import Panel
from rich.text import Text

from leaky import utils
from leaky.base import ApproximateSize, LeakyCount
from leaky.memory import (
    MemoryUsage,
    get_memory_usage,
    get_memory_usage_output,
)
from leaky.options import Options
from leaky.output import NewLine, OutputWriter, RichOutput
from leaky.reports import (
    LeakSummary,
    ObjectDetails,
    ReportIteration,
    ReportWriter,
    TypeSummary,
)
from leaky.themes import (
    END_OF_SECTION_TEXT,
    HEADING_BORDER,
)
from leaky.utils import convert_graph_nodes, get_full_type_name


class _LeakyObjectId(int):
    """
    An object ID.
    """


class _LeakyObjectIds(set[int]):
    """
    A list of object IDs.
    """


class LeakyUsageDiff:
    """
    Represents the difference between two usage records.
    """

    def __init__(self, objects: list[Any]) -> None:
        self._objects = objects

    def get_leak_summary(self, iteration: LeakyCount, options: Options) -> LeakSummary:
        """
        Gets a summary of potential leaks.
        """
        type_counts = Counter(type(o) for o in self._objects)
        type_sizes: dict[Type[Any], ApproximateSize] = defaultdict(ApproximateSize)
        for obj in self._objects:
            obj_type = type(obj)
            type_sizes[obj_type] += _safe_shallow_size(obj)
        type_summaries = []
        for obj_type, count in type_counts.most_common(options.max_types_in_leak_summary):
            size = type_sizes[obj_type]
            type_summaries.append(
                TypeSummary(
                    object_type=get_full_type_name(obj_type),
                    count=count,
                    shallow_size_bytes=size,
                )
            )
        return LeakSummary(iteration=int(iteration), type_summaries=type_summaries)

    def generate_object_details(
        self, excluded_from_referrers: list[int], options: Options
    ) -> Generator[ObjectDetails, None, None]:
        # Figure out how many objects to return per type based on options.max_referrers.
        # If we have more types than options.max_referrers, then we return one of each
        # of the most common types.
        type_counts = Counter(type(o) for o in self._objects)
        most_common_types = dict(type_counts.most_common(options.max_object_summaries))
        objs_per_type = options.max_object_summaries // len(most_common_types)

        # Get an iterator rather than using a for loop, so we can exclude it from the
        # referrers.
        iterator = iter(self._objects)
        current_counts_per_type: Counter[type] = Counter()
        str_func = options.str_func if options.str_func else self.safe_str
        try:
            while True:
                # Wrap the object in a list so we can exclude it
                obj_list = [next(iterator)]
                obj_type = type(obj_list[0])
                current_counts_per_type[obj_type] += 1
                if (
                    obj_type not in most_common_types
                    or current_counts_per_type[obj_type] > objs_per_type
                ):
                    continue
                if options.check_referrers:
                    referrer_graph = referrers.get_referrer_graph(
                        obj_list[0],
                        exclude_object_ids=[
                            id(iterator),
                            id(self._objects),
                            id(obj_list),
                        ]
                        + excluded_from_referrers,
                        max_depth=options.referrers_max_depth,
                        max_untracked_search_depth=options.referrers_max_untracked_search_depth,
                        timeout=options.referrers_search_timeout,
                        single_object_referrer_limit=options.single_object_referrer_limit,
                        module_prefixes=options.referrers_module_prefixes,
                    )
                else:
                    referrer_graph = None
                yield ObjectDetails(
                    deep_size_bytes=_safe_deep_size(obj_list[0]),
                    object_type_name=get_full_type_name(type(obj_list[0])),
                    object_id=id(obj_list[0]),
                    object_str=str_func(obj_list[0], options.str_max_length),
                    referrer_graph=convert_graph_nodes(referrer_graph.to_networkx())
                    if referrer_graph
                    else None,
                )
        except StopIteration:
            pass

    def __len__(self) -> int:
        return len(self._objects)

    def safe_str(self, obj: Any, truncate_at: int) -> str:
        try:
            str_repr = str(obj)
            if len(str_repr) > truncate_at:
                str_repr = str_repr[:truncate_at] + f" … ({len(str_repr) - truncate_at} more chars)"
            return str_repr
        except Exception as e:
            # Some things don't like their string representation being obtained.
            return f"<Error when getting string representation: {str(e)}>"


class LeakyUsageSnapshot:
    """
    A snapshot of memory usage at a particular point in time.
    """

    def __init__(self, objects: list[Any]) -> None:
        # Only store the IDs here so that we don't contribute to any leaks.
        self._object_ids = self._get_object_ids(objects)

    def get_diff(self, other_objects: list[Any]) -> LeakyUsageDiff:
        """
        Returns the difference between this record and another record.
        """
        other_ids = {id(obj): obj for obj in other_objects}
        diff_objs = [obj for obj_id, obj in other_ids.items() if obj_id not in self._object_ids]
        return LeakyUsageDiff(diff_objs)

    def _get_object_ids(self, objects: list[Any]) -> _LeakyObjectIds:
        return _LeakyObjectIds(_LeakyObjectId(id(obj)) for obj in objects)


class LeakySnapshotManager:
    """
    Manages one or more memory snapshots and allows a report to be generated based on
    these.
    """

    def __init__(self, report_id: str) -> None:
        self._report_id = report_id
        self._most_recent_snapshot: LeakyUsageSnapshot | None = None
        self._most_recent_snapshot_time: datetime | None = None
        self._most_recent_reported_usage: MemoryUsage | None = None

    def generate_new_snapshot(self, all_objects: list[Any], options: Options) -> None:
        self._most_recent_snapshot = LeakyUsageSnapshot(
            objects=_filter_default(
                objects=all_objects,
                options=options,
            ),
        )
        self._most_recent_snapshot_time = datetime.now(timezone.utc)

    def clear_snapshots(self) -> None:
        self._most_recent_snapshot = None
        self._most_recent_snapshot_time = None

    @property
    def report_id(self) -> str:
        return self._report_id

    @property
    def most_recent_snapshot(self) -> LeakyUsageSnapshot | None:
        return self._most_recent_snapshot

    @property
    def most_recent_snapshot_time(self) -> datetime | None:
        return self._most_recent_snapshot_time

    @property
    def most_recent_reported_usage(self) -> MemoryUsage | None:
        return self._most_recent_reported_usage

    @most_recent_reported_usage.setter
    def most_recent_reported_usage(self, value: MemoryUsage) -> None:
        self._most_recent_reported_usage = value


def generate_report(
    snapshot_manager: LeakySnapshotManager,
    all_objects: list[Any],
    writer: OutputWriter,
    report_writer: ReportWriter,
    options: Options,
    iteration: LeakyCount,
    include_object_ids: _LeakyObjectIds,
    excluded_from_referrers: list[int],
) -> None:
    _generate_report(
        snapshot_manager,
        objects=_filter_objects(
            objects=all_objects,
            included_types=options.included_types,
            excluded_types=options.excluded_types,
            include_object_ids=include_object_ids,
            # These objects may have been created since the previous iteration
            exclude_object_ids=_get_ids(
                [
                    snapshot_manager.most_recent_snapshot,
                    snapshot_manager.most_recent_snapshot.__dict__
                    if snapshot_manager.most_recent_snapshot
                    else None,
                    snapshot_manager.most_recent_snapshot_time,
                ]
            ),
        ),
        writer=writer,
        report_writer=report_writer,
        options=options,
        iteration=iteration,
        excluded_from_referrers=[id(all_objects)] + excluded_from_referrers,
    )


def _generate_report(
    snapshot_manager: LeakySnapshotManager,
    objects: list[Any],
    writer: OutputWriter,
    report_writer: ReportWriter,
    options: Options,
    iteration: LeakyCount,
    excluded_from_referrers: list[int],
) -> None:
    report_time = datetime.now(timezone.utc)
    writer.write(NewLine())
    writer.write(NewLine())
    memory_usage = get_memory_usage(iteration=iteration)
    usage_output = get_memory_usage_output(
        previous=snapshot_manager.most_recent_reported_usage, new=memory_usage
    )
    text = Text.from_markup(str(usage_output.to_renderables()[0]), justify="center")
    _write_start_panel(iteration, text, writer)
    snapshot_manager.most_recent_reported_usage = memory_usage
    writer.write(NewLine())
    summary, referrers_list = _perform_leak_report(
        snapshot_manager,
        objects,
        writer,
        options=options,
        iteration=iteration,
        excluded_from_referrers=excluded_from_referrers,
    )
    writer.write(
        RichOutput(
            f"[{END_OF_SECTION_TEXT}]End of Leaky Memory Report (iteration {iteration})["
            f"/{END_OF_SECTION_TEXT}]"
        )
    )
    report_iteration = ReportIteration(
        report_id=snapshot_manager.report_id,
        iteration_number=iteration,
        start_time=snapshot_manager.most_recent_snapshot_time
        if snapshot_manager.most_recent_snapshot_time
        else report_time,
        end_time=report_time,
        memory_usage=usage_output,
        leak_summary=summary,
        referrers=referrers_list,
    )
    report_writer.write_iteration(report_iteration)


def _perform_leak_report(
    snapshot_manager: LeakySnapshotManager,
    objects: list[Any],
    writer: OutputWriter,
    options: Options,
    iteration: LeakyCount,
    excluded_from_referrers: list[int],
) -> tuple[LeakSummary, list[ObjectDetails]]:
    if snapshot_manager.most_recent_snapshot is None:
        writer.write(
            RichOutput(
                "No detailed report is available yet.\n"
                "Detailed reports will be available from the next iteration."
            )
        )
        writer.write(NewLine())
        return LeakSummary(iteration=iteration, type_summaries=[]), []

    diff = snapshot_manager.most_recent_snapshot.get_diff(objects)
    if len(diff) == 0:
        writer.write(RichOutput("No leaks found during this iteration."))
        writer.write(NewLine())
        return LeakSummary(iteration=iteration, type_summaries=[]), []

    summary = diff.get_leak_summary(iteration=iteration, options=options)
    writer.write(summary)
    writer.write(NewLine())

    referrers_list = []
    for object_details in diff.generate_object_details(
        excluded_from_referrers=[id(objects)] + excluded_from_referrers, options=options
    ):
        writer.write(object_details)
        writer.write(NewLine())
        referrers_list.append(object_details)
    else:
        writer.write(NewLine())

    return summary, referrers_list


def _write_start_panel(
    iteration: LeakyCount, memory_usage_text: Text, writer: OutputWriter
) -> None:
    writer.write(
        RichOutput(
            Panel(
                memory_usage_text,
                expand=False,
                padding=1,
                border_style=HEADING_BORDER,
                title=f"[bold]Leaky Memory Report[/bold] (iteration {iteration})",
                title_align="center",
            )
        )
    )


def _get_ids(objs: Sequence[Any | None]) -> _LeakyObjectIds:
    """
    Gets the IDs of the objects in the list if they are not `None`.
    """
    return _LeakyObjectIds(_LeakyObjectId(id(obj)) for obj in objs if obj is not None)


_EXCLUDED_TYPES = {
    LeakySnapshotManager,
    LeakyUsageSnapshot,
    LeakyUsageDiff,
    LeakyCount,
    _LeakyObjectId,
    _LeakyObjectIds,
}


def _is_included_type(
    obj: Any,
    included_types: set[Type[Any]],
    excluded_types: set[Type[Any]],
    include_object_ids: _LeakyObjectIds,
    exclude_object_ids: _LeakyObjectIds,
) -> bool:
    if (
        id(obj) == id(included_types)
        or id(obj) == id(excluded_types)
        or id(obj) == id(include_object_ids)
        or id(obj) == id(exclude_object_ids)
        or id(obj) in exclude_object_ids
    ):
        return False
    if include_object_ids and id(obj) not in include_object_ids:
        return False
    if included_types:
        return type(obj) in included_types
    else:
        return type(obj) not in _EXCLUDED_TYPES and type(obj) not in excluded_types


def _filter_default(
    objects: list[Any],
    options: Options,
) -> list[Any]:
    return _filter_objects(
        objects=objects,
        included_types=options.included_types,
        excluded_types=options.excluded_types,
        include_object_ids=_LeakyObjectIds(),
        exclude_object_ids=_LeakyObjectIds(),
    )


def _filter_objects(
    objects: list[Any],
    included_types: set[Type[Any]],
    excluded_types: set[Type[Any]],
    include_object_ids: _LeakyObjectIds,
    exclude_object_ids: _LeakyObjectIds,
) -> list[Any]:
    # Also exclude the IDs of the objects in the include_object_ids and exclude_object_ids lists
    exclude_object_ids = _LeakyObjectIds(
        exclude_object_ids
        | {id(include_object_id) for include_object_id in include_object_ids}
        | {id(exclude_object_id) for exclude_object_id in exclude_object_ids}
    )
    return [
        obj
        for obj in objects
        if _is_included_type(
            obj=obj,
            included_types=included_types,
            excluded_types=excluded_types,
            include_object_ids=include_object_ids,
            exclude_object_ids=exclude_object_ids,
        )
    ]


def _gc_and_get_objects(max_untracked_search_depth: int) -> list[Any]:
    # The utils.get_objects function takes care of garbage collection
    return utils.get_objects(max_untracked_search_depth=max_untracked_search_depth)


def _safe_deep_size(obj: Any) -> ApproximateSize:
    """
    Gets the approximate deep size of an object. If an error is encountered getting
    the deep size, then an `ApproximateSize` where the upper bound is unknown is returned.
    """
    try:
        return ApproximateSize(
            approx_size=objsize.get_deep_size(obj),
        )
    except Exception:
        return ApproximateSize(approx_size=0, upper_bound_known=False)


def _safe_shallow_size(obj: Any) -> ApproximateSize:
    """
    Gets the approximate shallow size of an object. If an error is encountered getting
    the deep size, then an `ApproximateSize` where the upper bound is unknown is returned.
    """
    try:
        return ApproximateSize(
            approx_size=sys.getsizeof(obj),
        )
    except Exception:
        return ApproximateSize(approx_size=0, upper_bound_known=False)
