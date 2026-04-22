from unittest.mock import MagicMock

from cc_statusq_kit.core.SystemEvent import DiscoveryStartedEvent, HealthReportEvent, SystemEvent
from cc_statusq_kit.core.SystemEventBus import SystemEventBus


def test_bus_subscription_and_publish():
    """
    Test that a subscriber is notified when an event of the
    subscribed type is published.
    """
    bus = SystemEventBus()
    callback = MagicMock()

    # Subscribe to HealthReportEvent
    bus.subscribe(HealthReportEvent, callback)

    # Create and publish the event
    event = HealthReportEvent(source="test", data={"val": 1})
    bus.publish(event)

    # Verify the callback was executed with the event object
    callback.assert_called_once_with(event)


def test_bus_ignores_unsubscribed_events():
    """
    Test that publishing an event does not trigger callbacks
    subscribed to different event types.
    """
    bus = SystemEventBus()
    health_callback = MagicMock()
    discovery_callback = MagicMock()

    bus.subscribe(HealthReportEvent, health_callback)
    bus.subscribe(DiscoveryStartedEvent, discovery_callback)

    # Publish only a Discovery event
    event = DiscoveryStartedEvent(count=5)
    bus.publish(event)

    # Only the discovery callback should be called
    discovery_callback.assert_called_once_with(event)
    health_callback.assert_not_called()


def test_bus_polymorphism_subscription():
    """
    Test that subscribing to a base class (SystemEvent) also
    catches events of its subclasses.
    """
    bus = SystemEventBus()
    base_callback = MagicMock()

    # Subscribe to the root class
    bus.subscribe(SystemEvent, base_callback)

    # Publish a subclass event
    event = HealthReportEvent(source="CPU", data={})
    bus.publish(event)

    # The callback should be triggered due to inheritance (isinstance check)
    base_callback.assert_called_once_with(event)


def test_bus_multiple_subscribers_for_same_event():
    """
    Test that multiple callbacks can be registered for the
    same event type.
    """
    bus = SystemEventBus()
    callback_one = MagicMock()
    callback_two = MagicMock()

    bus.subscribe(HealthReportEvent, callback_one)
    bus.subscribe(HealthReportEvent, callback_two)

    event = HealthReportEvent(source="MultiTest", data={})
    bus.publish(event)

    callback_one.assert_called_once_with(event)
    callback_two.assert_called_once_with(event)


def test_bus_initialization_state():
    """
    Ensure the bus starts with no subscribers.
    """
    bus = SystemEventBus()
    assert bus._subscribers == {}
