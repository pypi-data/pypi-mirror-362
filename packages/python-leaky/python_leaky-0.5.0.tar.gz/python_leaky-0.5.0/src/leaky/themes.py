from rich.style import Style
from rich.theme import Theme

MEMORY_ABSOLUTE = "memory_absolute"
MEMORY_INCREASE = "memory_increase"
MEMORY_DECREASE = "memory_decrease"
COUNT = "count"
OBJECT_DETAILS_TITLE = "object_graph_title"
SIZE_TITLE = "size_title"
REFERRERS_TITLE = "referrers_title"
STRING_REPR_TITLE = "string_repr_title"
REFERRER_NAME = "referrer_name"
REFERRER_SUFFIX_LEAF = "referrer_name_leaf"
REFERRER_SUFFIX_CYCLE = "referrer_name_cycle"
OBJECT_ID = "object_id"
TITLE = "title"
HEADING_BORDER = "heading_border"
TABLE_TITLE = "table_title"
TABLE_HEADER = "table_header"
TABLE_BORDER = "table_border"
END_OF_SECTION_TEXT = "end_of_section_text"

DEFAULT_RICH_THEME = Theme(
    {
        MEMORY_ABSOLUTE: Style(color="cyan"),
        MEMORY_INCREASE: Style(color="red"),
        MEMORY_DECREASE: Style(color="green"),
        COUNT: Style(color="magenta"),
        OBJECT_DETAILS_TITLE: Style(),
        SIZE_TITLE: Style(color="yellow"),
        REFERRERS_TITLE: Style(color="yellow"),
        STRING_REPR_TITLE: Style(color="yellow"),
        REFERRER_NAME: Style(),
        OBJECT_ID: Style(color="bright_black"),
        TITLE: Style(bold=True),
        HEADING_BORDER: Style(color="yellow"),
        TABLE_TITLE: Style(color="yellow"),
        TABLE_HEADER: Style(),
        TABLE_BORDER: Style(color="yellow"),
        END_OF_SECTION_TEXT: Style(color="yellow"),
        REFERRER_SUFFIX_LEAF: Style(color="blue", italic=True),
        REFERRER_SUFFIX_CYCLE: Style(color="bright_black", italic=True),
    }
)
"""
The default theme for rich output.
"""
