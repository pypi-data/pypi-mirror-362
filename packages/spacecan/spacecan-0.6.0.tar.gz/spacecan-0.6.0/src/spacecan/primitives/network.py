import threading
import queue


class Network:
    """
    The Network class represents the redundant CAN system bus. It is
    initialized with a node ID and two bus objects, of which the nominal
    bus will be the selected bus (until the bus is switched).

    """

    def __init__(self, parent, node_id, bus_a, bus_b):
        self.parent = parent
        self.node_id = node_id
        self.bus_a = bus_a
        self.bus_b = bus_b

        self.selected_bus = self.bus_a
        self._thread = None

    def start(self):
        self.selected_bus.flush_frame_buffer()
        self.selected_bus.start_receive()
        self._thread = threading.Thread(target=self._process)
        self._thread.kill = False
        self._thread.start()

    def stop(self):
        self.selected_bus.flush_frame_buffer()
        self.selected_bus.stop_receive()
        if self._thread:
            self._thread.kill = True
            self._thread.join()

    def _process(self):
        thread = threading.current_thread()

        while not thread.kill:
            try:
                can_frame = self.selected_bus.frame_buffer.get(timeout=0.1)
            except queue.Empty:
                can_frame = None
                continue
            if thread.kill:
                break

            self.parent.received_frame(can_frame)

    def send(self, can_frame):
        self.selected_bus.send(can_frame)
