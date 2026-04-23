import threading
from typing import List

from .Monitorable import Monitorable
from .SystemEvent import DiscoveryStartedEvent
from .SystemEventBus import SystemEventBus


class StatusQ:
    def __init__(self, event_bus: SystemEventBus ):
        self._event_bus = event_bus
        self._children: List[Monitorable] = []

    def register_child(self, child: Monitorable):
        """Acepta una nueva aplicación hija en el ecosistema."""
        self._children.append(child)

    def pulse_all(self):
        """Lanza un latido único a todas las aplicaciones hijas."""
        self._event_bus.publish(DiscoveryStartedEvent(count=len(self._children)))
        for child in self._children:
            child.pulse()

    def telemetry_stream(self, interval: float, block: bool = True):
        """Inicia el flujo continuo de datos de todos los hijos."""
        threads = []
        for child in self._children:
            t = threading.Thread(target=child.start_stream, args=(interval,), daemon=True)
            threads.append(t)
            t.start()

        # TODO: esto se siente como un parche, implementar un diseño para integrar el echo que un adaptador hijo tome el control del programa  # noqa: E501
        if block:
            for t in threads:
                t.join()
