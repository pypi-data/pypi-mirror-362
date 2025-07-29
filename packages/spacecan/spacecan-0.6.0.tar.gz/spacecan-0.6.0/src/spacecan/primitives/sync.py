"""
The Sync service allows sending sync frames, either manually or
periodically. The Sync service is typically used by the network controller
node to allow responder nodes synchronize their behaviour upon receiving
this event.

"""

from .can_frame import CanFrame, ID_SYNC
from .timer import Timer


class SyncProducer:
    def __init__(self, parent):
        self.parent = parent
        self._running = False
        self._timer = None
        self._period = None

    def _send(self):
        self.parent.network.send(CanFrame(can_id=ID_SYNC))

        # schedule the next sending of sync
        self._timer = Timer(self._period, self._send)
        self._timer.start()

    def start(self, period):
        self._period = period
        if self._running:
            self.stop()
        self._running = True
        self._send()

    def stop(self):
        self._running = False
        if self._timer:
            self._timer.stop()
            self._timer = None
