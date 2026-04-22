from datetime import datetime

import pytest

from cc_statusq_kit.core.SystemEvent import DiscoveryStartedEvent, HealthReportEvent, SystemEvent


def test_system_event_timestamp_auto_generation():
    """
    Test that a SystemEvent generates a timestamp automatically if not provided.
    """
    # Create an event and immediately capture time
    event = SystemEvent()
    now = datetime.now()

    # Check that timestamp is a datetime object and is close to 'now'
    assert isinstance(event.timestamp, datetime)
    assert (now - event.timestamp).total_seconds() < 1


def test_system_event_immutability():
    """
    Test that events are frozen (immutable).
    """
    event = SystemEvent()
    # Attempting to change an attribute should raise a FrozenInstanceError (dataclasses)
    with pytest.raises(AttributeError):
        event.timestamp = datetime.now()


def test_discovery_started_event_initialization():
    """
    Test the DiscoveryStartedEvent specific attributes.
    """
    count_value = 5
    event = DiscoveryStartedEvent(count=count_value)

    assert event.count == count_value
    assert isinstance(event, SystemEvent)  # Verify inheritance


def test_health_report_event_data_integrity():
    """
    Test the HealthReportEvent correctly stores source and data dictionary.
    """
    source_id = "test-adapter"
    metrics = {"cpu": 10.5, "status": "ok"}

    event = HealthReportEvent(source=source_id, data=metrics)

    assert event.source == source_id
    assert event.data == metrics
    assert event.data["cpu"] == 10.5
    assert isinstance(event, SystemEvent)


def test_event_equality():
    """
    Test that two events with same data are considered equal (dataclass behavior).
    """
    fixed_time = datetime.now()
    event1 = DiscoveryStartedEvent(count=10, timestamp=fixed_time)
    event2 = DiscoveryStartedEvent(count=10, timestamp=fixed_time)

    assert event1 == event2


def test_event_representation():
    """
    Test that the __repr__ contains the relevant information.
    """
    event = HealthReportEvent(source="sensor", data={"val": 1})
    repr_str = repr(event)

    assert "HealthReportEvent" in repr_str
    assert "source='sensor'" in repr_str
    assert "data={'val': 1}" in repr_str
