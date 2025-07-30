import gc
import inspect
from dataclasses import asdict
from typing import Any, Dict, Type

import networkx as nx
from referrers import ReferrerGraphNode

from leaky.themes import (
    MEMORY_ABSOLUTE,
)

_KIB = 1024
_MIB = _KIB**2
_GIB = _KIB**3


def as_mib(num_bytes: int, tag: str = MEMORY_ABSOLUTE) -> str:
    """
    Returns a string representation of the number of byte1s in MiB, rounded to one decimal
    place.
    """
    return f"[{tag}]{num_bytes / 1024 / 1024:.1f}[/{tag}] MiB"


def as_mib_sf(num_bytes: int, tag: str = MEMORY_ABSOLUTE) -> str:
    """
    Returns a string representation of the number of bytes in MiB, rounded to three significant
    figures.
    """
    return f"[{tag}]{num_bytes / 1024 / 1024:.3g}[/{tag}] MiB"


def format_bytes(num_bytes: int, tag: str = MEMORY_ABSOLUTE) -> str:
    """
    Converts a size in bytes to a human-readable string in B, KiB, MiB, or GiB.

    This function takes an integer representing the number of bytes and returns
    a formatted string with the most appropriate unit. The rounding is adjusted
    based on the unit to provide a clean and readable output.
    """
    if not isinstance(num_bytes, int) or num_bytes < 0:
        raise ValueError("Input must be a non-negative integer.")

    if num_bytes == 0:
        return "0 B"

    if num_bytes < _KIB:
        # For bytes, no decimal places are needed
        return f"[{tag}]{num_bytes}[/{tag}] B"
    elif num_bytes < _MIB:
        # For KiB, one decimal place is appropriate
        kib_value = num_bytes / _KIB
        return f"[{tag}]{kib_value:.1f}[/{tag}] KiB"
    elif num_bytes < _GIB:
        # For MiB, two decimal places offer good precision
        mib_value = num_bytes / _MIB
        return f"[{tag}]{mib_value:.2f}[/{tag}] MiB"
    else:
        # For GiB, two decimal places are also suitable
        gib_value = num_bytes / _GIB
        return f"[{tag}]{gib_value:.2f}[/{tag}] GiB"


def get_full_type_name(obj_type: Type[Any]) -> str:
    """
    Gets the full type name of an object.
    """
    return f"{obj_type.__module__}.{obj_type.__name__}"


def get_objects(max_untracked_search_depth: int = 3) -> list[Any]:
    """
    Gets all objects that are currently in memory in the Python process, that are not eligible
    for garbage collection.

    This is different from `gc.get_objects` in a few ways:

     - It always performs a garbage collection when it is called.
     - It finds untracked objects, as long as they are referred to (directly or indirectly) by
       tracked objects. Untracked objects include, for example, mutable objects and collections
       containing only immutable objects in CPython. The `max_untracked_search_depth` controls
       how deep this function searches for untracked objects if they are not referred to directly
       by tracked objects. Setting this to a higher value is more likely to find untracked
       objects but will take more time.
     - It ignores frame objects.
     - It removes duplicate objects.

    :param max_untracked_search_depth: The maximum depth to search for untracked objects. This
        defaults to 3, which is enough to find most untracked objects. For example, this
        will find objects in tuples that are in another collection. However, it may not find
        certain untracked objects, like nested tuples.
    """
    gc.collect()
    tracked_objects = gc.get_objects()

    all_objects = []
    seen_ids = set()

    for obj in tracked_objects:
        if not _is_excluded(obj):
            obj_id = id(obj)
            if obj_id not in seen_ids:
                all_objects.append(obj)
                seen_ids.add(obj_id)

    # Search the referents of the objects we have found, looking for untracked objects.
    objects_to_search = list(all_objects)
    for _ in range(max_untracked_search_depth):
        new_untracked_referents = []
        for obj in objects_to_search:
            try:
                referents = gc.get_referents(obj)
                # Go through all referents and add them to new_untracked_referents if we
                # haven't seen them before, and they are untracked (and not excluded).
                for referent in referents:
                    referent_id = id(referent)
                    if (
                        referent_id not in seen_ids
                        and not gc.is_tracked(referent)
                        and not _is_excluded(referent)
                    ):
                        new_untracked_referents.append(referent)
                        all_objects.append(referent)
                        seen_ids.add(referent_id)
            except ReferenceError:
                # Some objects might not be accessible
                pass
        objects_to_search = new_untracked_referents

    return all_objects


def _is_excluded(obj: Any) -> bool:
    try:
        return inspect.isframe(obj)
    except ReferenceError:
        # This can happen if the object is a weak reference proxy where the underlying
        # object has been garbage collected. We just ignore these objects.
        return True


def convert_graph_nodes(referrer_graph: nx.DiGraph) -> nx.DiGraph:
    """
    Converts a networkx graph with ReferrerGraphNode nodes to a graph
    with string nodes, transferring node attributes.
    """
    new_graph = nx.DiGraph()
    unique_ids: Dict[ReferrerGraphNode, int] = {}
    for unique_id, node in enumerate(referrer_graph.nodes()):
        unique_ids[node] = unique_id
        if isinstance(node, ReferrerGraphNode):
            attributes = asdict(node)
            attributes["object_id"] = attributes["id"]
            del attributes["id"]
            new_graph.add_node(unique_id, **attributes)
        else:
            raise ValueError(f"Unexpected type: {type(node)}")
    for u, v in referrer_graph.edges():
        if isinstance(u, ReferrerGraphNode) and isinstance(v, ReferrerGraphNode):
            new_graph.add_edge(unique_ids[u], unique_ids[v])
        else:
            raise ValueError(f"Unexpected type: {type(u)} or {type(v)}")
    return new_graph
