import pytest

from cc_statusq_kit.core.Monitorable import Monitorable

# --- Dummy Implementation for Testing ---


class ValidMonitor:
    """A class that correctly implements the Monitorable protocol."""

    def get_id(self) -> str:
        return "test-monitor"

    def pulse(self) -> None:
        pass

    def start_stream(self, interval: float) -> None:
        pass


class InvalidMonitor:
    """A class that misses methods from the Monitorable protocol."""

    def get_id(self) -> str:
        return "invalid"


# --- Tests ---


def test_monitorable_is_runtime_checkable():
    """
    Verify that Monitorable is decorated with @runtime_checkable,
    allowing isinstance() checks.
    """
    monitor = ValidMonitor()
    # This only works if @runtime_checkable is present in the Protocol definition
    assert isinstance(monitor, Monitorable)


def test_invalid_implementation_fails_check():
    """
    Verify that a class missing required methods is NOT considered a Monitorable.
    """
    bad_monitor = InvalidMonitor()
    assert not isinstance(bad_monitor, Monitorable)


def test_monitorable_contract_methods():
    """
    Test that an object satisfying the Monitorable protocol
    has all the expected callable methods.
    """
    monitor: Monitorable = ValidMonitor()

    # Verify method presence and basic behavior
    assert hasattr(monitor, "get_id")
    assert hasattr(monitor, "pulse")
    assert hasattr(monitor, "start_stream")

    assert monitor.get_id() == "test-monitor"


def test_protocol_cannot_be_instantiated():
    """
    Protocols are not meant to be instantiated directly.
    """
    with pytest.raises(TypeError):
        # Depending on Python version, this might raise TypeError
        # because Protocols are abstract.
        Monitorable()


def test_start_stream_parameters():
    """
    Verify that start_stream accepts the required 'interval' argument.
    """
    monitor = ValidMonitor()
    try:
        monitor.start_stream(interval=1.0)
    except TypeError:
        pytest.fail("start_stream should accept 'interval' as a parameter")
