import threading


class Timer:
    def __init__(self, period, callback):
        self._period = period
        self._callback = callback
        self._running = False
        self._timer = None

    def start(self):
        if self._running:
            self.stop()
        self._running = True
        self._timer = threading.Timer(self._period, self._callback)
        self._timer.start()

    def stop(self):
        self._running = False
        if self._timer:
            self._timer.cancel()
