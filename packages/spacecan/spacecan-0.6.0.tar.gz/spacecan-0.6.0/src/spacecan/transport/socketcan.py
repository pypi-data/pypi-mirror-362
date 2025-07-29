import threading

import can

from .base import Bus
from ..primitives.can_frame import CanFrame


class SocketCanBus(Bus):
    def __init__(self, parent, channel):
        super().__init__(parent)
        self.channel = channel
        self._bus = can.Bus(interface="socketcan", channel=self.channel)
        self._thread = None

    def disconnect(self):
        self._bus.shutdown()

    def set_filters(self, filters):
        self._bus.set_filters(filters)

    def send(self, can_frame):
        msg = can.Message(
            arbitration_id=can_frame.can_id, data=can_frame.data, is_extended_id=False
        )
        try:
            self._bus.send(msg)
        except can.exceptions.CanOperationError:
            pass

    def start_receive(self):
        self._thread = threading.Thread(target=self._receive)
        self._thread.kill = False
        self._thread.start()

    def stop_receive(self):
        if self._thread:
            self._thread.kill = True
            self._thread.join()

    def _receive(self):
        thread = threading.current_thread()
        while not thread.kill:
            msg = self._bus.recv(0.1)
            if thread.kill:
                break
            if msg:
                can_frame = CanFrame(msg.arbitration_id, msg.data)
                self.frame_buffer.put(can_frame)
