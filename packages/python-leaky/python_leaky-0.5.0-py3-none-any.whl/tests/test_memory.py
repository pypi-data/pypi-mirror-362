from leaky.base import LeakyCount
from leaky.memory import (
    MemoryUsage,
    get_memory_usage,
    get_memory_usage_output,
)
from leaky.reports import MemoryUsageOutput


class TestGetMemoryUsage:
    """
    Tests the `get_memory_usage` function.
    """

    def test_get_memory_usage(self) -> None:
        """
        Test get_memory_usage.
        """
        result = get_memory_usage(LeakyCount(11))

        # There isn't much we can check here, but we can at least make sure
        # the result is a MemoryUsage object and has the expected fields.
        assert isinstance(result, MemoryUsage)
        assert isinstance(result.current_rss_bytes, int)
        assert result.current_rss_bytes > 0
        assert isinstance(result.system_percent_used, float)
        assert 0 <= result.system_percent_used <= 100
        assert isinstance(result.peak_rss_bytes, int)
        assert result.peak_rss_bytes > 0
        assert result.iteration_number == 11


class TestGetMemoryUsageOutput:
    """
    Tests the `get_memory_usage_output` function.
    """

    def test_with_previous(self) -> None:
        """
        Test get_memory_usage_output with both previous and new MemoryUsage objects.
        """
        previous = MemoryUsage(
            current_rss_bytes=1000,
            peak_rss_bytes=1500,
            system_percent_used=10.0,
            iteration_number=1,
        )

        new = MemoryUsage(
            current_rss_bytes=1200,
            peak_rss_bytes=1800,
            system_percent_used=12.0,
            iteration_number=2,
        )

        result = get_memory_usage_output(previous, new)

        assert isinstance(result, MemoryUsageOutput)
        assert result.current_rss_bytes == 1200
        assert result.peak_rss_bytes == 1800
        assert result.system_percent_used == 12.0
        assert result.current_rss_diff == 200  # 1200 - 1000
        assert result.peak_rss_diff == 300  # 1800 - 1500
        assert result.diff_from_iteration == 1

    def test_without_previous(self) -> None:
        """
        Test get_memory_usage_output when previous is None.
        """
        new = MemoryUsage(
            current_rss_bytes=1200,
            peak_rss_bytes=1800,
            system_percent_used=12.0,
            iteration_number=2,
        )

        result = get_memory_usage_output(None, new)

        assert isinstance(result, MemoryUsageOutput)
        assert result.current_rss_bytes == 1200
        assert result.peak_rss_bytes == 1800
        assert result.system_percent_used == 12.0
        assert result.current_rss_diff is None
        assert result.peak_rss_diff is None
        assert result.diff_from_iteration is None

    def test_with_none_peak_rss(self) -> None:
        """
        Test get_memory_usage_output when peak_rss_bytes is None.
        """
        previous = MemoryUsage(
            current_rss_bytes=1000,
            peak_rss_bytes=None,
            system_percent_used=10.0,
            iteration_number=1,
        )

        new = MemoryUsage(
            current_rss_bytes=1200,
            peak_rss_bytes=None,
            system_percent_used=12.0,
            iteration_number=2,
        )

        result = get_memory_usage_output(previous, new)

        assert isinstance(result, MemoryUsageOutput)
        assert result.current_rss_bytes == 1200
        assert result.peak_rss_bytes is None
        assert result.system_percent_used == 12.0
        assert result.current_rss_diff == 200  # 1200 - 1000
        assert result.peak_rss_diff is None  # Both are None
        assert result.diff_from_iteration == 1
