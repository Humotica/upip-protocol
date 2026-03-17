"""UPIP Example: Fibonacci sequence with hash verification."""
import hashlib
import json


def fibonacci(n):
    a, b = 0, 1
    result = []
    for _ in range(n):
        result.append(a)
        a, b = b, a + b
    return result


fib = fibonacci(50)
digest = hashlib.sha256(json.dumps(fib).encode()).hexdigest()
print(f"Fibonacci(50) = {fib[-1]}")
print(f"Sequence hash: {digest}")
print(f"Sum: {sum(fib)}")
