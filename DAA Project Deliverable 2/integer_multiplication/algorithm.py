import sys
import time

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

sys.setrecursionlimit(10000)

def schoolbook_multiply(x, y):
    """Classic O(n^2) digit-by-digit multiplication (baseline for comparison).

    Returns (product, execution_time, digit_multiplications).
    """
    start_time = time.perf_counter()

    a = str(x)[::-1]
    b = str(y)[::-1]
    res = [0] * (len(a) + len(b))
    digit_mults = 0

    for i, da in enumerate(a):
        carry = 0
        for j, db in enumerate(b):
            digit_mults += 1
            cur = res[i + j] + int(da) * int(db) + carry
            res[i + j] = cur % 10
            carry = cur // 10
        k = i + len(b)
        while carry:
            cur = res[k] + carry
            res[k] = cur % 10
            carry = cur // 10
            k += 1

    product = int("".join(map(str, res[::-1])))
    return product, time.perf_counter() - start_time, digit_mults


def multiply(x, y, trace_depth=3):
    """Karatsuba integer multiplication (divide and conquer).

    x * y = ac*10^(2m) + ((a+b)(c+d) - ac - bd)*10^m + bd
    where x = a*10^m + b and y = c*10^m + d.  Only 3 recursive
    multiplications are needed instead of 4.

    Returns (result, execution_time, events) - the same shape that
    closest_pair() returns, so the UI can treat both algorithms alike.

    The execution time is measured on a run WITHOUT tracing.  A second run
    records the step-by-step events for the UI, down to `trace_depth` levels
    (deeper recursion is still executed but not shown).
    """
    if x < 0 or y < 0:
        raise ValueError("Only non-negative integers are supported.")

    # 1) timed run, no tracing
    stats = {"recursive_calls": 0, "base_cases": 0}
    start_time = time.perf_counter()
    product = _karatsuba(x, y, stats, None, 0, 0, None)
    execution_time = time.perf_counter() - start_time

    # 2) traced run, used only for the visualisation
    trace_stats = {"recursive_calls": 0, "base_cases": 0}
    events = []
    ids = {"next": 0}
    _karatsuba(x, y, trace_stats, events, 0, trace_depth, None, ids)

    result = {
        "product": product,
        "digits_x": len(str(x)),
        "digits_y": len(str(y)),
        "recursive_calls": stats["recursive_calls"],
        "base_cases": stats["base_cases"],
    }
    return result, execution_time, events


def _karatsuba(x, y, stats, events, depth, max_depth, parent, ids=None):
    stats["recursive_calls"] += 1
    tracing = events is not None and depth <= max_depth

    node_id = None
    if tracing:
        node_id = ids["next"]
        ids["next"] += 1

    # Base case: a single-digit factor
    if x < 10 or y < 10:
        stats["base_cases"] += 1
        product = x * y
        if tracing:
            events.append({
                "type": "base", "title": "Base Case", "depth": depth,
                "node_id": node_id, "parent_id": parent, "x": x, "y": y,
                "result": product,
                "explanation": "One of the numbers has a single digit, so "
                               "multiply directly.",
            })
        return product

    # Deeper than we want to show: solve silently
    if tracing and depth == max_depth:
        silent = {"recursive_calls": 0, "base_cases": 0}
        product = _karatsuba(x, y, silent, None, depth, max_depth, None)
        stats["recursive_calls"] += silent["recursive_calls"]
        stats["base_cases"] += silent["base_cases"]
        events.append({
            "type": "solved", "title": "Solved Recursively", "depth": depth,
            "node_id": node_id, "parent_id": parent, "x": x, "y": y,
            "result": product,
            "explanation": "The same divide / recurse / combine steps are "
                           "applied to this smaller problem. The deeper "
                           "levels are hidden to keep the visualisation "
                           "readable.",
        })
        return product

    n = max(len(str(x)), len(str(y)))
    m = n // 2
    p = 10 ** m
    a, b = divmod(x, p)
    c, d = divmod(y, p)

    if tracing:
        events.append({
            "type": "divide", "title": "Divide", "depth": depth,
            "node_id": node_id, "parent_id": parent, "x": x, "y": y,
            "a": a, "b": b, "c": c, "d": d, "m": m,
            "explanation": f"Split both numbers {m} digits from the right: "
                           "x = a x 10^m + b and y = c x 10^m + d. "
                           "Then make three recursive multiplications: "
                           "a x c, b x d and (a + b) x (c + d).",
        })

    child = node_id if tracing else None
    ac = _karatsuba(a, c, stats, events, depth + 1, max_depth, child, ids)
    bd = _karatsuba(b, d, stats, events, depth + 1, max_depth, child, ids)
    abcd = _karatsuba(a + b, c + d, stats, events, depth + 1, max_depth,
                      child, ids)

    ad_bc = abcd - ac - bd
    product = ac * p * p + ad_bc * p + bd

    if tracing:
        events.append({
            "type": "combine", "title": "Combine", "depth": depth,
            "node_id": node_id, "parent_id": parent, "x": x, "y": y,
            "m": m, "ac": ac, "bd": bd, "abcd": abcd, "ad_bc": ad_bc,
            "result": product,
            "explanation": "Recover the middle term without a 4th "
                           "multiplication: a x d + b x c = "
                           "(a + b)(c + d) - ac - bd. Then combine: "
                           "ac x 10^(2m) + (ad + bc) x 10^m + bd.",
        })
    return product


if __name__ == "__main__":
    x = int(input("Enter first integer: "))
    y = int(input("Enter second integer: "))

    result, execution_time, events = multiply(x, y)
    expected, school_time, digit_mults = schoolbook_multiply(x, y)

    print("\nInteger Multiplication Results")
    print("------------------------------")
    print("Karatsuba product:", result["product"])
    print("Schoolbook product:", expected)
    print("Match:", result["product"] == expected == x * y)
    print("Recursive Calls:", result["recursive_calls"])
    print("Base Cases:", result["base_cases"])
    print("Karatsuba Time:", execution_time, "seconds")
    print("Schoolbook Time:", school_time, "seconds")
    print("Visualization Steps:", len(events))
