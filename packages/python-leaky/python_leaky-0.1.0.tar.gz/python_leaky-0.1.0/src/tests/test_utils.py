import gc
from typing import Any, Tuple

import numpy as np

from leaky import utils


class NumpyArrayHolder:
    def __init__(self, size: int) -> None:
        self.payload = np.ones(size)


class TupleHolder:
    def __init__(self, the_tuple: Tuple[Any, ...]) -> None:
        self.the_tuple = the_tuple


class TestGetObject:
    """
    Tests for the `get_objects` function.
    """

    def test_get_objects_with_np_array_holder(self) -> None:
        """
        Tests that NumPy arrays are returned when they are instance attributes of a class.

        In Python 3.10, for example, instance attributes are held in a dict, and since CPython
        doesn't track collections of immutable objects, we need to search the referents for
        at least two levels to find the NumPy array in this case.
        """
        my_object = NumpyArrayHolder(128)
        objects = utils.get_objects()
        object_ids = {id(obj) for obj in objects}
        assert id(my_object.payload) in object_ids

    def test_get_objects_with_tuple_holder(self) -> None:
        """
        Tests that tuples are returned when they are instance attributes of a class.

        In Python 3.10, for example, instance attributes are held in a dict, and since CPython
        doesn't track collections of immutable objects, we need to search the referents for
        at least two levels to find the tuple in this case.
        """
        my_object = TupleHolder(("string in tuple",))
        objects = utils.get_objects()
        object_ids = {id(obj) for obj in objects}
        assert id(my_object.the_tuple) in object_ids
        assert id(my_object.the_tuple[0]) in object_ids

    def test_with_nested_tuples(self) -> None:
        """
        Tests the `get_objects` function with nested tuples. Nested tuples are interesting
        because they are both immutable and collections. Since CPython doesn't track
        collections of immutable objects, it's possible for nested tuples to "hide" objects
        from `get_objects`.

        Note: we need to increase `max_untracked_search_depth` to 5 to find the innermost
        tuple. This is because (in Python 3.10) we have the following reference chain:

        TupleHolder -> __dict__ -> Tuple c -> Tuple b -> Tuple a -> string
        """
        my_object = TupleHolder(self._get_nested_tuples())
        objects = utils.get_objects(max_untracked_search_depth=5)
        object_ids = {id(obj) for obj in objects}
        assert id(my_object.the_tuple) in object_ids
        assert id(my_object.the_tuple[0]) in object_ids
        assert id(my_object.the_tuple[0][0]) in object_ids
        assert id(my_object.the_tuple[0][0][0]) in object_ids

    def _get_nested_tuples(self) -> Tuple[Tuple[Tuple[str]]]:
        a = ("tuples all the way down",)
        b = (a,)
        c = (b,)
        # CPython stops tracking tuples if they contain only immutable objects, but
        # only when they are first seen by the garbage collector, so we need to collect
        # here to trigger this.
        gc.collect()
        return c
