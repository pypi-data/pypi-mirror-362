"""
Public interfaces used in leaky. These are imported into the main `__init__.py` file.
"""

from abc import ABC, abstractmethod
from typing import Any


class LeakMonitor(ABC):
    """
    A class that can be used as a context manager to monitor for memory leaks. The *second* time
    that the enclosed code is called, a summary of potential leaks will be printed to the console.
    """

    @abstractmethod
    def __enter__(self) -> None:
        """
        Starts leak monitoring.
        """
        pass

    @abstractmethod
    def __exit__(
        self, exc_type: type[BaseException] | None, exc_value: BaseException | None, traceback: Any
    ) -> None:
        """
        Ends leak monitoring and prints a summary of potential leaks.
        """
        pass

    def __call__(self) -> "LeakMonitor":
        return self
