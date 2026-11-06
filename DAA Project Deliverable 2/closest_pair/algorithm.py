import math
import time


def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def closest_pair(points):
    start_time = time.perf_counter()

    points = [(p[0], p[1], i) for i, p in enumerate(points)]

    if len(points) < 2:
        raise ValueError("At least two points are required.")

    points_x = sorted(points, key=lambda p: (p[0], p[1]))
    points_y = sorted(points, key=lambda p: (p[1], p[0]))

    steps = []
    stats = {"recursive_calls": 0, "comparisons": 0}

    def solve(px, py):
        stats["recursive_calls"] += 1
        n = len(px)

        steps.append(f"Current subproblem contains {n} points.")

        if n <= 3:
            min_dist = float("inf")
            best_pair = None

            for i in range(n):
                for j in range(i + 1, n):
                    stats["comparisons"] += 1
                    d = distance(px[i], px[j])

                    if d < min_dist:
                        min_dist = d
                        best_pair = (px[i], px[j])

            steps.append(f"Base case: minimum distance = {min_dist:.4f}")
            return min_dist, best_pair

        # Divide the points into left and right halves
        mid = n // 2
        mid_x = px[mid][0]

        left_x = px[:mid]
        right_x = px[mid:]

        left_ids = {p[2] for p in left_x}

        left_y = [p for p in py if p[2] in left_ids]
        right_y = [p for p in py if p[2] not in left_ids]

        steps.append("Divided points into left and right halves.")

        # Find the closest pair in both halves
        d1, pair1 = solve(left_x, left_y)
        d2, pair2 = solve(right_x, right_y)

        if d1 <= d2:
            min_dist, best_pair = d1, pair1
        else:
            min_dist, best_pair = d2, pair2

        steps.append(f"Best distance from halves = {min_dist:.4f}")

        # Check points close to the dividing line
        strip = [p for p in py if abs(p[0] - mid_x) < min_dist]

        steps.append(f"Checking the middle strip containing {len(strip)} points.")

        for i in range(len(strip)):
            for j in range(i + 1, min(i + 8, len(strip))):
                if strip[j][1] - strip[i][1] >= min_dist:
                    break

                stats["comparisons"] += 1
                d = distance(strip[i], strip[j])

                if d < min_dist:
                    min_dist = d
                    best_pair = (strip[i], strip[j])

        steps.append(f"Combined result: minimum distance = {min_dist:.4f}")

        return min_dist, best_pair

    min_dist, pair = solve(points_x, points_y)

    end_time = time.perf_counter()

    result = {
        "closest_points": (
            (pair[0][0], pair[0][1]),
            (pair[1][0], pair[1][1])
        ),
        "minimum_distance": min_dist,
        "recursive_calls": stats["recursive_calls"],
        "distance_comparisons": stats["comparisons"]
    }

    execution_time = end_time - start_time

    return result, execution_time, steps


if __name__ == "__main__":
    n = int(input("Enter number of points (minimum 10): "))

    if n < 10:
        raise ValueError("Input size must be at least 10.")

    points = []

    for i in range(n):
        x, y = map(float, input(f"Enter point {i + 1} (x y): ").split())
        points.append((x, y))

    result, execution_time, steps = closest_pair(points)

    print("\nClosest Pair Results")
    print("--------------------")
    print("Closest Points:", result["closest_points"])
    print("Minimum Distance:", result["minimum_distance"])
    print("Recursive Calls:", result["recursive_calls"])
    print("Distance Comparisons:", result["distance_comparisons"])
    print("Execution Time:", execution_time, "seconds")

    print("\nAlgorithm Working")
    for step in steps:
        print(step)