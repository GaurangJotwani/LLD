import time
from collections import OrderedDict
from abc import ABC, abstractmethod


class CacheStrategy(ABC):
    @abstractmethod
    def put(self, cache, key, value, ttl = None):
        pass
    
    @abstractmethod
    def get(self, cache, key):
        pass
    
    @abstractmethod
    def evict(self, cache):
        pass

class Cache:
    def __init__(self, cache_strategy):
        self.cache_strategy = cache_strategy
        self.store = OrderedDict()
    
    def put(self, key, value, ttl = None):
        self.cache_strategy.put(self, key, value, ttl)
    
    def get(self, key):
        self.cache_strategy.get(self, key)
    
    def evict(self):
        self.cache_strategy.evict(self)

class TimeEvictionStrategy(CacheStrategy):
    DEFAULT_TTL = 15

    def put(self, cache, key, value, ttl = None):
        ttl = ttl if ttl else TimeEvictionStrategy.DEFAULT_TTL
        if ttl < 0: raise ValueError("ttl cannot be less than zero")
        timestamp = time.time()
        self.cache.store[key] = (value, timestamp, ttl)
        cache.store.move_to_end(key)
    
    def get(self, cache, key):
        if key not self.cache.store:
            print("key not found")
            return -1
        value, timestamp, ttl = cache.store[key]
        current_time = time.time()

        if current_time - timestamp > ttl:
            del cache.store[key]
            return -1
        cache.store.move_to_end(key)
        return value
    
    def evict(self, cache):
        current_time = time.time()
        expired_keys = [key for key, (val, timestamp, ttl) in cache.store.items()
                        if current_time - timestamp > ttl]
        for key in expired_keys:
            del cache.store[key]
            print(f"[TimeEviction] Evicted key '{key}' at time {current_time:.2f}")

class SizeEvictionStrategy(CacheStrategy):
    def __init__(self, max_size):
        self.max_size = max_size

    def put(self, cache, key, value, ttl=None):
        # TTL is ignored in size-based eviction.
        cache.store[key] = value
        # Move key to the end as most recently used.
        cache.store.move_to_end(key)
        print(f"[SizeEviction] Put key '{key}' with value '{value}'.")
        if len(cache.store) > self.max_size:
            self.evict(cache)

    def get(self, cache, key):
        if key not in cache.store:
            print(f"[SizeEviction] Key '{key}' not found.")
            return -1
        # Move key to the end as most recently used.
        cache.store.move_to_end(key)
        value = cache.store[key]
        print(f"[SizeEviction] Key '{key}' accessed, value: {value}.")
        return value

    def evict(self, cache):
        while len(cache.store) > self.max_size:
            evicted_key, evicted_value = cache.store.popitem(last=False)
            print(f"[SizeEviction] Evicted key '{evicted_key}' due to size limit (max_size={self.max_size}).")

if __name__ == "__main__":
    print("=== Time-Based Eviction Strategy Tests ===")
    time_strategy = TimeEvictionStrategy()
    time_cache = Cache(time_strategy)
    
    print("\n[Test 1: Immediate Access with default TTL]")
    time_cache.put("foo", "bar")  # Uses default TTL (15 seconds)
    print("Get 'foo':", time_cache.get("foo"))
    
    print("\n[Test 2: Immediate Access with custom TTL=2]")
    time_cache.put("baz", "qux", ttl=2)
    print("Get 'baz':", time_cache.get("baz"))
    
    print("\n[Test 3: Access After Expiry]")
    time.sleep(3)
    print("Get 'baz' after expiry:", time_cache.get("baz"))
    
    print("\n[Test 4: Manual Eviction]")
    time_cache.put("alpha", 100, ttl=1)
    time_cache.put("beta", 200, ttl=5)
    time.sleep(2)
    print("Get 'alpha':", time_cache.get("alpha"))
    print("Get 'beta':", time_cache.get("beta"))
    time_cache.evict()
    print("Current keys after eviction (TimeEviction):", list(time_cache.store.keys()))
    
    print("\n=== Size-Based Eviction Strategy Tests ===")
    size_strategy = SizeEvictionStrategy(max_size=3)
    size_cache = Cache(size_strategy)
    
    print("\n[Test 5: Size Limit Eviction]")
    size_cache.put("one", 1)
    size_cache.put("two", 2)
    size_cache.put("three", 3)
    print("Current keys:", list(size_cache.store.keys()))
    
    # Inserting one more item should trigger eviction of the oldest entry.
    size_cache.put("four", 4)
    print("After adding 'four', current keys:", list(size_cache.store.keys()))
    
    print("\n[Test 6: Accessing Existing Key]")
    print("Get 'two':", size_cache.get("two"))