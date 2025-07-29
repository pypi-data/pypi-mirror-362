import time

class TimeLap:
    def __init__(self):
        self.start_time = None
        self.last_time = None

    def _log(self, label, elapsed):
        hours, rem = divmod(elapsed, 3600)
        minutes, seconds = divmod(rem, 60)
        milliseconds = (seconds - int(seconds)) * 1000
        formatted = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}.{int(milliseconds):03}"
        print(f"[{label}] {formatted}")

    def start(self, text="Start"):
        self.start_time = time.perf_counter()
        self.last_time = self.start_time
        self._log(text, 0)

    def now(self, text="Now"):
        if self.start_time is None:
            raise RuntimeError("timelap.start() must be called before timelap.now()")
        current = time.perf_counter()
        elapsed = current - self.start_time
        self.last_time = current
        self._log(text, elapsed)

    def stop(self, text="Stop"):
        if self.start_time is None:
            raise RuntimeError("timelap.start() must be called before timelap.stop()")
        current = time.perf_counter()
        elapsed = current - self.start_time
        self._log(text, elapsed)
        self.start_time = None
        self.last_time = None

timelap = TimeLap()