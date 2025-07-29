import queue


class Bus:
    def __init__(self, parent):
        self.parent = parent
        self.frame_buffer = queue.Queue()

    def disconnect(self):
        pass

    def flush_frame_buffer(self):
        self.frame_buffer = queue.Queue()

    def set_filters(self, filters):
        raise NotImplementedError

    def send(self, can_frame):
        raise NotImplementedError

    def start_receive(self):
        raise NotImplementedError

    def stop_receive(self):
        raise NotImplementedError
