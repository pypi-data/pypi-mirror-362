from pydantic.dataclasses import dataclass


class LeakyCount(int):
    """
    A count. This is used in preference to int so that it can be excluded from reports.
    """

    pass


@dataclass
class ApproximateSize:
    """
    Represents an approximate uncertain size. That is, a size where the lower bound is known
    approximately, and the upper bound may not be known at all.
    """

    approx_size: int = 0
    """
    If `upper_bound_known` is `True`, then this is the approximate size. If `upper_bound_known` is
    `False`, then this is the approximate lower bound of the size.
    """

    upper_bound_known: bool = True
    """
    Whether the upper bound of the size is known.
    """

    def __add__(self, other: "ApproximateSize") -> "ApproximateSize":
        return ApproximateSize(
            self.approx_size + other.approx_size, self.upper_bound_known and other.upper_bound_known
        )

    @property
    def prefix(self) -> str:
        if self.upper_bound_known:
            return "~"
        else:
            return ">="
