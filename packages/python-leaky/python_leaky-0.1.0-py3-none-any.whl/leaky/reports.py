import dataclasses
import json
import random
import string
import sys
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

import networkx as nx
from networkx.classes import DiGraph
from pydantic import TypeAdapter, field_serializer, field_validator
from pydantic.dataclasses import dataclass
from rich import box
from rich.console import NewLine as RichNewLine
from rich.console import RenderableType
from rich.panel import Panel
from rich.table import Table

from leaky import networkx_copy
from leaky.base import ApproximateSize
from leaky.options import Options
from leaky.output import Output
from leaky.themes import (
    COUNT,
    HEADING_BORDER,
    MEMORY_DECREASE,
    MEMORY_INCREASE,
    OBJECT_DETAILS_TITLE,
    OBJECT_ID,
    REFERRER_NAME,
    REFERRER_SUFFIX_CYCLE,
    REFERRER_SUFFIX_LEAF,
    SIZE_TITLE,
    STRING_REPR_TITLE,
    TABLE_BORDER,
    TABLE_HEADER,
    TABLE_TITLE,
    TITLE,
)
from leaky.utils import as_mib, as_mib_sf, format_bytes

_CURRENT_FILE_VERSION = 1
"""
The current file format version. Used when writing files.
"""

_REPORT_DIR_PREFIX = "leaky_report_"
"""
The prefix of the report directory name.
"""

_ITERATION_REPORT_PREFIX = "iteration_report_"
"""
The prefix of the iteration report file name.
"""

_SUMMARY_FILE_NAME = "summary.json"
"""
The name of the summary file.
"""


@dataclass
class ReportMetadata:
    """
    Metadata relating to a single leak report. This is generated at the start of execution.
    """

    report_id: str
    """
    A unique ID of the report.
    """
    entrypoint: str
    """
    The entrypoint of the report. This is the main function that was used to start the
    program that was analyzed.
    """
    arguments: List[str]
    """
    The arguments that were used to start the program that was analyzed.
    """
    start_time: datetime
    """
    The start time of the report.
    """


@dataclass
class ReportSummary:
    """
    A summary of a single leak report, generated at the end of execution.
    """

    metadata: ReportMetadata
    """
    Metadata about the report.
    """

    iteration_count: int
    """
    The number of iterations that were run. This can be used to, for example, get the most
    recent iteration of the report, since iteration numbers are sequential.
    """


@dataclass
class MemoryUsageOutput(Output):
    """
    An `Output` object representing the memory usage.
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

    current_rss_diff: int | None
    """
    The difference in RSS between the current and previous usage. This is `None` if
    previous usage is not provided.
    """

    peak_rss_diff: int | None
    """
    The difference in RSS between the peak and previous peak. This is `None` if
    previous usage is not provided.
    """

    diff_from_iteration: int | None
    """
    The iteration number that the difference was calculated from. This is `None` if
    previous usage is not provided.
    """

    def to_renderables(self) -> list[RenderableType]:
        log_message = f"[{TITLE}]Memory used[/{TITLE}]: {as_mib(self.current_rss_bytes)}"
        if self.current_rss_diff is not None:
            sign = "+" if self.current_rss_diff >= 0 else ""
            tag = MEMORY_INCREASE if self.current_rss_diff > 0 else MEMORY_DECREASE
            log_message += f" ([{tag}]{sign}[/{tag}]{as_mib_sf(self.current_rss_diff, tag=tag)})"
        log_message += f" / {self.system_percent_used:.2f}% sys"
        if self.peak_rss_bytes is not None:
            log_message += "\n"
            log_message += f"[{TITLE}]Peak memory[/{TITLE}]: {as_mib(self.peak_rss_bytes)}"
            if self.peak_rss_diff is not None:
                sign = "+" if self.peak_rss_diff >= 0 else ""
                tag = MEMORY_INCREASE if self.peak_rss_diff > 0 else MEMORY_DECREASE
                log_message += f" ([{tag}]{sign}[/{tag}]{as_mib_sf(self.peak_rss_diff, tag=tag)})"
        return [log_message]


@dataclass
class TypeSummary:
    """
    A summary of a specific type of object.
    """

    object_type: str
    """
    The name of the type of object that was found to be leaking.
    """
    count: int
    """
    The number of objects of this type that were found to be leaking.
    """
    shallow_size_bytes: ApproximateSize
    """
    The total shallow size of all objects of this type that were found to be leaking.

    If the total size could not be determined, then the `upper_bound_known` field of
    `deep_size_bytes` will be `False`.
    """


@dataclass
class LeakSummary(Output):
    """
    A summary of potential leaks.
    """

    iteration: int
    """
    The iteration that this summary is for
    """

    type_summaries: list[TypeSummary]
    """
    A list of summaries for each type of object that was found to be leaking.
    """

    def to_renderables(self) -> list[RenderableType]:
        table = Table(
            title=f"Possible New Leaks (iteration {self.iteration})",
            box=box.ROUNDED,
            header_style=TABLE_HEADER,
            title_style=TABLE_TITLE,
            border_style=TABLE_BORDER,
        )
        table.add_column("Object Type", justify="left", no_wrap=True)
        table.add_column("Count", justify="right")
        table.add_column("Shallow size (estimated)", justify="right")
        for summary in self.type_summaries:
            formatted_bytes = format_bytes(summary.shallow_size_bytes.approx_size)
            table.add_row(
                summary.object_type,
                f"[{COUNT}]{summary.count}[/{COUNT}]",
                f"{summary.shallow_size_bytes.prefix}{formatted_bytes}",
            )
        return [table]


@dataclass(config={"arbitrary_types_allowed": True})
class ObjectDetails(Output):
    """
    Represents details of a specific object, including its referrers.
    """

    object_type_name: str
    object_id: int
    object_str: str
    deep_size_bytes: ApproximateSize
    referrer_graph: DiGraph | None

    def to_renderables(self) -> list[RenderableType]:
        title = (
            f"[{OBJECT_DETAILS_TITLE}]Details for {self.object_type_name} (id="
            f"{self.object_id})[/{OBJECT_DETAILS_TITLE}]"
        )
        size_str = (
            f"[{OBJECT_DETAILS_TITLE}]{self.deep_size_bytes.prefix}[/{OBJECT_DETAILS_TITLE}]"
            f"{format_bytes(self.deep_size_bytes.approx_size, tag=OBJECT_DETAILS_TITLE)}"
        )
        size = f"[{SIZE_TITLE}]Deep size (estimated):[/{SIZE_TITLE}] {size_str}"
        if self.referrer_graph is None or len(self.referrer_graph) == 0:
            referrer_graph = "No referrers found"
        else:
            # We avoid using Rich's tree here for now, as it seems to have issues
            # with wrapping and cropping. See https://github.com/Textualize/rich/issues/3785.
            printable_graph = _convert_graph_nodes_to_printable(self.referrer_graph)
            network_text = networkx_copy.generate_network_text(printable_graph)  # type: ignore
            referrer_graph = "\n" + "\n".join(line for line in network_text)
        return [
            Panel(
                title,
                box=box.ASCII,
                expand=False,
                padding=0,
                border_style=HEADING_BORDER,
            ),
            RichNewLine(),
            size,
            RichNewLine(),
            referrer_graph,
            RichNewLine(),
            f"[{STRING_REPR_TITLE}]String representation:[/{STRING_REPR_TITLE}]",
            self.object_str,
        ]

    @field_serializer("referrer_graph", when_used="json")
    def serialize_referrer_graph(self, referrer_graph: DiGraph | None) -> dict[str, Any] | None:
        if referrer_graph is None:
            return None
        else:
            node_link_data = nx.node_link_data(referrer_graph)
            assert isinstance(node_link_data, dict)
            return node_link_data

    @field_validator("referrer_graph", mode="before")
    @classmethod
    def validate_referrer_graph(cls, value: Any) -> DiGraph | None:
        """
        Validator to convert a dictionary back into a ReferrerGraph instance.
        """
        if value is None or isinstance(value, DiGraph):
            return value
        elif isinstance(value, dict):
            nx_graph = nx.node_link_graph(value)
            return nx_graph
        else:
            raise ValueError("Input for referrer_graph must be a DiGraph instance or a dict")


@dataclass
class ReportIteration:
    """
    A single iteration of a leak report.
    """

    report_id: str
    """
    The ID of the report that this iteration belongs to.
    """
    iteration_number: int
    """
    The iteration number of the report.
    """
    start_time: datetime
    """
    The start time of the iteration.
    """
    end_time: datetime
    """
    The end time of the iteration.
    """
    memory_usage: MemoryUsageOutput
    """
    The memory usage of the iteration.
    """
    leak_summary: LeakSummary
    """
    A summary of the leaks found in this iteration.
    """
    referrers: list[ObjectDetails]
    """
    A list of referrers for each object that was found to be leaking.
    """


@dataclass
class FullReport:
    """
    A full report of a single leak.
    """

    summary: ReportSummary
    """
    A summary of the report.
    """
    iterations: list[ReportIteration]
    """
    A list of all iterations of the report. Each iteration contains information about the
    memory usage and potential leaks at that point in time.
    """


class ReportWriter(ABC):
    """
    A writer that writes report data to a sink. This is typically a file.
    """

    @abstractmethod
    def write_iteration(self, iteration: ReportIteration) -> None:
        pass

    @property
    @abstractmethod
    def report_id(self) -> str:
        pass


class ReportReader(ABC):
    """
    A reader that reads report data from a source. This is typically a file.
    """

    @abstractmethod
    def get_report_summaries(self) -> list[ReportSummary]:
        """
        Gets the summaries of all reports in the given directory. If no directory is
        provided, the default report root is used.

        If the directory does not exist, an empty list is returned.
        """
        pass

    @abstractmethod
    def get_full_report(self, report_id: str, num_iterations: int) -> FullReport:
        """
        Gets the full report for a given report ID. The number of iterations to return
        is specified by the `num_iterations` parameter. The most recent `num_iterations`
        are returned, ordered by iteration number.

        If the report does not exist, a `ValueError` is raised.
        """
        pass


class NoOpReportWriter(ReportWriter):
    """
    A writer that does nothing.
    """

    def __init__(self, report_summary: ReportMetadata) -> None:
        self._report_id = report_summary.report_id

    def write_iteration(self, iteration: ReportIteration) -> None:
        # Do nothing
        pass

    @property
    def report_id(self) -> str:
        return self._report_id


class FileReportWriter(ReportWriter):
    """
    A writer that writes report data to a file within the report directory. Each
    iteration is written to a separate file suffixed with the iteration number.

    The writer is initialized with the path to the report directory and the report
    summary, which is written to a file named `summary.json`.
    """

    def __init__(self, report_directory: Path, report_summary: ReportMetadata) -> None:
        self._report_directory = report_directory
        self._report_summary = report_summary
        summary_file = self._report_directory / _SUMMARY_FILE_NAME
        with open(summary_file, "wb") as f:
            f.write(TypeAdapter(type(self._report_summary)).dump_json(self._report_summary))
        version_file = self._report_directory / "version"
        with open(version_file, "w") as f:
            f.write(str(_CURRENT_FILE_VERSION))

    def write_iteration(self, iteration: ReportIteration) -> None:
        iteration_file = (
            self._report_directory / f"{_ITERATION_REPORT_PREFIX}{iteration.iteration_number}.json"
        )
        with open(iteration_file, "wb") as f:
            f.write(TypeAdapter(type(iteration)).dump_json(iteration))

    @property
    def report_id(self) -> str:
        return self._report_summary.report_id


class FileReportReader(ReportReader):
    def __init__(self, report_directory: Path | None = None) -> None:
        self._report_root = _get_report_root(
            override=str(report_directory) if report_directory else None
        )

    def get_report_summaries(self) -> List[ReportSummary]:
        """
        Gets the summaries of all reports in the given directory. If no directory is
        provided, the default report root is used.

        If the directory does not exist, an empty list is returned.
        """
        if not self._report_root.exists():
            return []
        else:
            summary_list = []
            report_dirs = [
                d
                for d in self._report_root.iterdir()
                if d.is_dir() and d.name.startswith(_REPORT_DIR_PREFIX)
            ]
            for report_dir in report_dirs:
                summary_path = report_dir / _SUMMARY_FILE_NAME
                if summary_path.exists():
                    with open(summary_path, "r") as f:
                        data = json.load(f)
                        summary_start: ReportMetadata = TypeAdapter(ReportMetadata).validate_python(
                            data
                        )
                    iteration_files = list(report_dir.glob(f"{_ITERATION_REPORT_PREFIX}*.json"))
                    iteration_count = len(iteration_files)
                    summary = ReportSummary(
                        metadata=summary_start,
                        iteration_count=iteration_count,
                    )
                    summary_list.append(summary)
            return summary_list

    def get_full_report(self, report_id: str, num_iterations: int) -> FullReport:
        report_dir = self._report_root / f"{_REPORT_DIR_PREFIX}{report_id}"
        if not report_dir.exists():
            raise ValueError(f"Report with ID {report_id} not found.")

        summary_path = report_dir / _SUMMARY_FILE_NAME
        with open(summary_path, "r") as f:
            data = json.load(f)
            summary_start = TypeAdapter(ReportMetadata).validate_python(data)

        iteration_files = sorted(
            report_dir.glob(f"{_ITERATION_REPORT_PREFIX}*.json"),
            key=lambda p: int(p.stem.split(f"{_ITERATION_REPORT_PREFIX}")[1]),
            reverse=True,
        )

        iterations = []
        for iteration_file in iteration_files[:num_iterations]:
            with open(iteration_file, "r") as f:
                data = json.load(f)
                iteration = TypeAdapter(ReportIteration).validate_python(data)
                iterations.append(iteration)

        iterations.sort(key=lambda i: i.iteration_number)

        summary = ReportSummary(
            metadata=summary_start,
            iteration_count=len(iteration_files),
        )

        return FullReport(summary=summary, iterations=iterations)


def get_report_writer(options: Options) -> ReportWriter:
    """
    Gets an report writer for the given options.

    If the report directory is not specified, the default report root is used.
    The report root is a directory in the user's home directory called `.leaky/reports`.
    """
    start_time = datetime.now(timezone.utc)
    report_root = _get_report_root(
        override=str(options.report_directory) if options.report_directory else None
    )

    report_id = _generate_report_id(start_time)
    report_dir_name = f"{_REPORT_DIR_PREFIX}{report_id}"
    report_directory = report_root / report_dir_name
    while report_directory.exists():
        report_id = _generate_report_id(start_time)
        report_dir_name = f"{_REPORT_DIR_PREFIX}{report_id}"
        report_directory = report_root / report_dir_name
    report_directory.mkdir(parents=True, exist_ok=False)

    report_summary = ReportMetadata(
        report_id=report_id,
        entrypoint=_get_entrypoint(),
        arguments=_get_arguments(),
        start_time=start_time,
    )

    if options.save_reports:
        report_writer: ReportWriter = FileReportWriter(report_directory, report_summary)
    else:
        report_writer = NoOpReportWriter(report_summary)
    return report_writer


def get_report_reader(report_directory: Path | None = None) -> ReportReader:
    """
    Gets a report reader for the given report directory. If no directory is provided,
    the default report root is used.
    """
    return FileReportReader(report_directory=report_directory)


def _get_report_root(override: str | None) -> Path:
    """
    Gets the root directory for reports.
    """
    if override is None:
        report_root = _get_default_report_root()
    else:
        report_root = Path(override)
    return report_root


def _get_default_report_root() -> Path:
    """
    Gets the default report root.
    """
    return Path.home() / ".leaky" / "reports"


def _generate_report_id(start_time: datetime) -> str:
    """
    Generates a short, human-friendly, ID with a high probability of uniqueness
    (but the ID is not guaranteed to be unique, so needs to be checked).
    """
    chars = string.ascii_lowercase + string.digits
    first_part = "".join(random.choice(chars) for _ in range(4))
    second_part = "".join(random.choice(chars) for _ in range(4))
    return f"{first_part}-{second_part}"


def _get_entrypoint() -> str:
    """
    Gets the entrypoint of the report.
    """
    return sys.argv[0]


def _get_arguments() -> list[str]:
    """
    Gets the arguments of the report.
    """
    return sys.argv[1:]


# Note: this is not a pydantic data class
@dataclasses.dataclass(frozen=True)
class _PrintableReferrerNode:
    name: str
    """
    A meaningful name for the referrer. For example, if the referrer is a local variable,
    the name would be the variable name, suffixed with "(local)".
    """

    object_id: int
    """
    A unique ID for the referrer object. If the referrer is not an object then this is the
    ID of the object it refers to.
    """

    type: str
    """
    A string representing the type of referrer. For example, if the referrer is a local
    variable, this would be "local".
    """

    is_cycle: bool
    """
    Whether the referrer is part of a cycle in the graph. If this is `True`, the referrer
    will be the last node in a branch of the graph.
    """

    is_leaf: bool = False
    """
    Whether this node is a leaf node in the graph.
    """

    def __str__(self) -> str:
        if self.is_leaf and self.is_cycle:
            suffix = f"[{REFERRER_SUFFIX_CYCLE}](cycle)[/{REFERRER_SUFFIX_CYCLE}]"
        elif self.is_leaf and not self.is_cycle:
            suffix = f"[{REFERRER_SUFFIX_LEAF}](root)[/{REFERRER_SUFFIX_LEAF}]"
        else:
            suffix = ""
        return (
            f"[{REFERRER_NAME}]{self.name}[/{REFERRER_NAME}] "
            f"[{OBJECT_ID}](id={self.object_id})[/{OBJECT_ID}] "
            f"{suffix}"
        )


def _convert_graph_nodes_to_printable(referrer_graph: nx.DiGraph) -> nx.DiGraph:
    """
    Converts a networkx graph with string nodes and attributes, as produced by
    `utils.convert_graph_nodes` to a graph with `_PrintableReferrerNode`s.
    """
    new_graph = nx.DiGraph()
    printable_nodes: Dict[int, _PrintableReferrerNode] = {}
    for node in referrer_graph.nodes():
        if isinstance(node, int):
            attrs = referrer_graph.nodes[node]
            new_node = _PrintableReferrerNode(is_leaf=referrer_graph.out_degree(node) == 0, **attrs)
            new_graph.add_node(new_node)
            printable_nodes[node] = new_node
        else:
            raise ValueError(f"Unexpected type: {type(node)}")
    for u, v in referrer_graph.edges():
        if isinstance(u, int) and isinstance(v, int):
            new_graph.add_edge(printable_nodes[u], printable_nodes[v])
        else:
            raise ValueError(f"Unexpected type: {type(u)} or {type(v)}")
    return new_graph
