"""
Leaking bucket algorithm is similar to the token bucket algorithm except that
requests are  processed at a fixed rate. It is usually implemented with a
first-in-first-out (FIFO) queue. It works as follows:
    i. When request arrives, the system checks if queue is full.
    ii. If it is not full, request is added to the queue.
    iii. Otherwise, the request is dropped.
    iv. Requests are pulled from queue and processed at regular intervals.

Pros:
    - Memory efficient.
    - Requests are processed at fixed intervals.

Cons:
    - Burst of traffic fills the queue along with older requests. If not
      processed in time, new requests will be dropped.
    - Tuning bucker size and outflow rate is challenging.
"""
import time
from collections import deque

class LeakingBucket:
    def __init__(self, bucket_size, outflow_rate):
        """
        Initialize the leaking bucket.

        Args:
            bucket_size (int): Maximum number of requests that bucket can hold (queue size).
            outflow_rate (int): Number of requests processed per second.
        """
        self.bucket_size = bucket_size
        self.outflow_rate = outflow_rate
        self.queue = deque()
        self.last_processed_time = time.monotonic()

    def _process_queue(self):
        """
        Process requests from the queue at the fixed outflow rate.
        """
        now = time.monotonic()
        elapsed_time = now - self.last_processed_time

        request_to_process = int(elapsed_time * self.outflow_rate)

        for _ in range(request_to_process):
            if self.queue:
                self.queue.popleft()
            else:
                break

        self.last_processed_time += request_to_process / self.outflow_rate

    def add_request(self):
        """
        Add a new request to the queue, dropping if the queue is full.

        Returns:
            bool: True, if request is added, False otherwise.
        """
        self._process_queue()
        
        if(len(self.queue) < self.bucket_size):
            self.queue.append(time.monotonic())
            return True
        return False
    
if __name__ == '__main__':
    bucket = LeakingBucket(bucket_size=5, outflow_rate=1)
    
    for i in range(15):
        if bucket.add_request():
            print(f"Request processed: {i + 1}              Queue size: {len(bucket.queue)}")
        else:
            print(f"Request dropped: {i + 1}                Queue size: {len(bucket.queue)}")
        time.sleep(0.4)
