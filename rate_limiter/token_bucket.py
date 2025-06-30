"""
Token Bucket is a rate-limiter algorithm for any service. It prevents any user
spamming a service with loads of requests. The working can be defined as:
    i. There is a bucket with n number of tokens.
    ii. There is a bucket refiller, filling the buckets, with lets say x number of token per unit time.
    iii. Whenever a requests arrives, if there is token available in bucket, assign the token to request.
    iv. If no tokens in bucket, request is dropped, limitting the service access rate.

Pros:
    - Easy to implement.
    - Memory efficient.
    - Allows burst of traffic for short period of time.

Cons:
    - Finding a tune between bucket size and token refill rate is challenging task.
"""
import time

class TokenBucket:
    def __init__(self, bucket_size, refill_rate):
        """
        Initialize the token bucket.

        Args:
            bucket_size (int): Maximum number of tokens bucket can hold.
            refill_rate (int): Number of tokens added to bucket per second.
        """
        self.bucket_size = bucket_size
        self.refill_rate = refill_rate
        # Assuming bucket is full in the beginning.
        self.tokens = bucket_size
        self.last_refill_time = time.monotonic()

    def _refill(self):
        """
        Refill the bucket with tokens based on the elapsed time since the last refill.
        """
        now = time.monotonic()
        elapsed_time = now - self.last_refill_time
        new_tokens = elapsed_time * self.refill_rate
        self.tokens = min(self.bucket_size, self.tokens + new_tokens)
        self.last_refill_time = now

    def allow_request(self, tokens=1):
        """
        Check if a request can be processed. If so, consume the required tokens.

        Args:
            tokens (int): Number of tokens required to process the request.

        Returns:
            bool: True, if request is allowed, False otherwise.
        """
        self._refill()
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False
    
if __name__ == '__main__':
    bucket = TokenBucket(bucket_size=5, refill_rate=1)
    for i in range(15):
        if bucket.allow_request():
            print(f"Request processed: {i + 1}      ||     Tokens left: {bucket.tokens:.1f}")
        else:
            print(f"Request dropped: {i + 1}        ||     Tokens left: {bucket.tokens:.1f}")
        time.sleep(0.4)
