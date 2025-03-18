import time
from abc import ABC, abstractmethod

# --- RateLimiter Interface ---
class RateLimiter(ABC):
    @abstractmethod
    def allow_request(self) -> bool:
        """
        Determines if a request is allowed under the current rate limiting rules.
        """
        pass

# --- Leaky Bucket Implementation ---
class LeakyBucketRateLimiter(RateLimiter):
    def __init__(self, capacity: int, leak_rate: float):
        """
        :param capacity: Maximum number of requests that can be queued.
        :param leak_rate: Number of requests that leak per second.
        """
        self.capacity = capacity
        self.leak_rate = leak_rate  # requests per second
        self.last_check = time.time()
        self.current_level = 0.0  # using float to allow fractional leakage

    def allow_request(self) -> bool:
        now = time.time()
        # Calculate time passed since last check and leak the bucket accordingly
        time_passed = now - self.last_check
        leaked = time_passed * self.leak_rate
        self.current_level = max(0.0, self.current_level - leaked)
        self.last_check = now

        if self.current_level < self.capacity:
            # There's space in the bucket, so add a request (fill the bucket) and allow the request.
            self.current_level += 1
            return True
        else:
            # Bucket is full; reject the request.
            return False

# --- Token Bucket Implementation ---
class TokenBucketRateLimiter(RateLimiter):
    def __init__(self, capacity: int, refill_rate: float):
        """
        :param capacity: Maximum number of tokens in the bucket.
        :param refill_rate: Number of tokens added per second.
        """
        self.capacity = capacity
        self.refill_rate = refill_rate  # tokens per second
        self.tokens = capacity  # start with a full bucket
        self.last_check = time.time()

    def allow_request(self) -> bool:
        now = time.time()
        # Refill tokens based on elapsed time
        time_passed = now - self.last_check
        added_tokens = time_passed * self.refill_rate
        self.tokens = min(self.capacity, self.tokens + added_tokens)
        self.last_check = now

        if self.tokens >= 1:
            # Consume one token for the incoming request
            self.tokens -= 1
            return True
        else:
            # Not enough tokens available; reject the request.
            return False

# --- Example Usage ---
if __name__ == "__main__":
    # Create instances of each rate limiter.
    leaky_bucket = LeakyBucketRateLimiter(capacity=5, leak_rate=1)  # 1 request per second leakage, max 5 requests queued
    token_bucket = TokenBucketRateLimiter(capacity=5, refill_rate=1)  # 1 token per second, bucket size 5

    # Simulate a burst of requests
    print("Leaky Bucket Results:")
    for i in range(10):
        allowed = leaky_bucket.allow_request()
        print(f"Request {i+1}: {'Allowed' if allowed else 'Rejected'}")
        time.sleep(0.3)  # simulate time between requests

    print("\nToken Bucket Results:")
    for i in range(10):
        allowed = token_bucket.allow_request()
        print(f"Request {i+1}: {'Allowed' if allowed else 'Rejected'}")
        time.sleep(0.3)  # simulate time between requests
