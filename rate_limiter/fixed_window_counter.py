"""
Fixed window counter algorithms works:
    i. Timeline is divided into fixed-size windows and counter is assigned for each window.
    ii. Each request increments the counter by one.
    iii. Once counter reaches pre-defined threshold, new requests are dropped until a new windows starts.

Pros:
    - Memory efficient.
    - Easy to understand.

Cons:
    - Spike in traffic at the edges of window allows more request than allowed quota to go through.
"""
import time

class FixedWindowCounter:
    def __init__(self, window_size, request_threshold):
        """
        Intialize the fixed window counter.

        Args:
            window_size (int): Duration of each window in seconds.
            request_threshold (int): Maximum number of requests allowed in a single window
        """
        self.window_size = window_size
        self.request_threshold = request_threshold
        self.current_window_start = self._get_current_window()
        self.request_count = 0

    def _get_current_window(self):
        """
        Get the start time of the current window.
        """
        return int(time.time() // self.window_size) * self.window_size
    
    def allow_request(self):
        """
        Process a request and check if it is allowed or should be dropped.

        Returns:
            bool: True, if request is allowed, False otherwise.
        """
        current_time = time.time()
        current_window_start = self._get_current_window()

        if current_window_start != self.current_window_start:
            self.current_window_start = current_window_start
            self.request_count = 0

        if self.request_count < self.request_threshold:
            self.request_count += 1
            return True
        return False
    
if __name__ == '__main__':
    rate_limiter = FixedWindowCounter(window_size=5, request_threshold=1)

    for i in range(15):
        if rate_limiter.allow_request():
            print(f"Request {i + 1}: Allowed (Window Start: {rate_limiter.current_window_start}, Count: {rate_limiter.request_count})")
        else:
            print(f"Request {i + 1}: Dropped (Window Start: {rate_limiter.current_window_start}, Count: {rate_limiter.request_count})")
        time.sleep(0.4)