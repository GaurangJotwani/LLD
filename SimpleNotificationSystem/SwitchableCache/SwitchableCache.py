import time
from collections import OrderedDict
from abc import ABC, abstractmethod

# EvictionPolicy interface (Strategy pattern)
class EvictionPolicy(ABC):
    @abstractmethod
    def put(self, cache, key, value, size):
        pass
    @abstractmethod
    def get(self, cache, key):
        pass
    @abstractmethod
    def evict(self, cache):
        pass

# Time-based eviction policy
class TimeBasedEvictionPolicy(EvictionPolicy):
    def __init__(self, ttl_seconds=300):  # Default TTL is 5 minutes (300 sec)
        self.ttl_seconds = ttl_seconds

    def put(self, cache, key, value, size=None):
        # Store the value with the current timestamp
        timestamp = time.time()
        cache.store[key] = (value, timestamp)
        # Remove expired items right after insertion
        self.evict(cache)

    def get(self, cache, key):
        if key not in cache.store:
            return None
        value, timestamp = cache.store[key]
        # Check if the item has expired
        if time.time() - timestamp > self.ttl_seconds:
            del cache.store[key]
            return None
        return value

    def evict(self, cache):
        current_time = time.time()
        expired_keys = [
            key for key, (value, timestamp) in cache.store.items()
            if current_time - timestamp > self.ttl_seconds
        ]
        for key in expired_keys:
            del cache.store[key]

# Size-based eviction policy
class SizeBasedEvictionPolicy(EvictionPolicy):
    def __init__(self, max_size):
        self.max_size = max_size
        self.current_size = 0

    def put(self, cache, key, value, size):
        # Edge case: new item's size exceeds the total allowed cache size.
        if size > self.max_size:
            raise ValueError("New item size exceeds cache limitation.")
        # Add/update the item (store value along with its size)
        cache.store[key] = (value, size)
        self.current_size += size
        # Evict items if needed to maintain the size constraint
        self.evict(cache)

    def get(self, cache, key):
        if key not in cache.store:
            return None
        value, size = cache.store[key]
        return value

    def total_size(self, cache):
        # Compute the sum of sizes of all items in the cache.
        return self.current_size

    def evict(self, cache):
        # Evict items until the total size is within the limit.
        while self.total_size(cache) > self.max_size:
            # Remove the oldest inserted item (FIFO eviction) from the OrderedDict.
            cache.store.popitem(last=False)

# The Cache class (Context)
class Cache:
    def __init__(self, eviction_policy: EvictionPolicy):
        # Using an OrderedDict to facilitate eviction order (e.g., FIFO or LRU)
        self.store = OrderedDict()
        self.eviction_policy = eviction_policy

    def put(self, key, value, size=None):
        """
        Insert an item into the cache.
        For time-based policy, 'size' is ignored.
        For size-based policy, 'size' must be provided.
        """
        self.eviction_policy.put(self, key, value, size)

    def get(self, key):
        """
        Retrieve an item from the cache.
        """
        return self.eviction_policy.get(self, key)

# Example usage:
if __name__ == "__main__":
    # --- Using a Time-Based Cache ---
    print("Time-Based Cache:")
    time_policy = TimeBasedEvictionPolicy(ttl_seconds=10)  # Short TTL for demo purposes
    time_cache = Cache(eviction_policy=time_policy)
    time_cache.put("user1", "data1")
    print("Fetched:", time_cache.get("user1"))
    time.sleep(11)  # Wait until the key expires
    print("After TTL expired, fetched:", time_cache.get("user1"))
    
    # --- Using a Size-Based Cache ---
    print("\nSize-Based Cache:")
    size_policy = SizeBasedEvictionPolicy(max_size=100)  # Total allowed size is 100 units
    size_cache = Cache(eviction_policy=size_policy)
    size_cache.put("item1", "value1", size=30)
    size_cache.put("item2", "value2", size=50)
    print("Total size after 2 inserts:", size_policy.total_size(size_cache))
    
    # This insert is fine: total size becomes 30+50+10 = 90, within limit.
    size_cache.put("item3", "value3", size=10)
    print("Total size after 3 inserts:", size_policy.total_size(size_cache))
    
    # Insert that causes eviction: new item size 40 would push total to 30+50+10+40 = 130 (>100)
    try:
        size_cache.put("item4", "value4", size=40)
    except ValueError as e:
        print("Error:", e)
    # Instead, if the new item is valid (i.e. its size <= max_size) the policy evicts older items:
    size_cache.put("item4", "value4", size=20)
    print("Total size after item4 insert:", size_policy.total_size(size_cache))
    print("Cache content:", list(size_cache.store.keys()))
