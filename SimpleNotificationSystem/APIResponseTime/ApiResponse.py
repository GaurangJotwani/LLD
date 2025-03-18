import time
from statistics import median

class APIResponseTester:
    def __init__(self):
        pass

    def run_test(self, func, iterations=10, *args, **kwargs):
        response_times = []

        for _ in range(iterations):
            start = time.time()
            func(*args, **kwargs)
            end = time.time()
            response_times.append(end - start)

        stats = {
            "count": len(response_times),
            "min": min(response_times) if response_times else None,
            "max": max(response_times) if response_times else None,
            "avg": sum(response_times) / len(response_times) if response_times else None,
            "median": median(response_times) if response_times else None
        }
        return stats

# --------------------------
# Example Usage & Test Cases
# --------------------------
if __name__ == "__main__":
    tester = APIResponseTester()

    def get_users():
        # Simulate processing delay for a GET /users API call.
        time.sleep(0.1)
        return ["user1", "user2", "user3"]

    def create_order(sleep_time):
        # Simulate processing delay based on the sleep_time parameter.
        time.sleep(sleep_time)
        return {"order_id": 12345}

    # Run tests for get_users function for 10 iterations.
    stats_get_users = tester.run_test(get_users, iterations=10)
    print("Stats for GET /users:", stats_get_users)

    # Run tests for create_order function for 10 iterations.
    stats_create_order = tester.run_test(create_order, iterations=10, sleep_time=0.3)
    print("Stats for POST /orders:", stats_create_order)
