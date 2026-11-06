
import math
import time


def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def closest_pair(points):
    start_time = time.perf_counter()

    if len(points) < 2:
        raise ValueError("At least two points are required.")

    points = [(p[0], p[1], i) for i, p in enumerate(points)]

    points_x = sorted(points, key=lambda p: (p[0], p[1]))
    points_y = sorted(points, key=lambda p: (p[1], p[0]))

    events = []
    stats = {"recursive_calls": 0, "comparisons": 0}

    def get_coordinates(point_list):
        return [(p[0], p[1]) for p in point_list]

    def get_pair_coordinates(pair):
        if pair is None:
            return None
        return (
            (pair[0][0], pair[0][1]),
            (pair[1][0], pair[1][1])
        )

    def solve(px, py, depth=0):
        stats["recursive_calls"] += 1
        n = len(px)

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

            events.append({
                "type": "base",
                "title": "Base Case",
                "explanation": f"Only {n} points remain. Compare every pair directly.",
                "points": get_coordinates(px),
                "closest_pair": get_pair_coordinates(best_pair),
                "minimum_distance": min_dist,
                "depth": depth
            })

            return min_dist, best_pair

        mid = n // 2
        mid_x = px[mid][0]

        left_x = px[:mid]
        right_x = px[mid:]

        left_ids = {p[2] for p in left_x}

        left_y = [p for p in py if p[2] in left_ids]
        right_y = [p for p in py if p[2] not in left_ids]

        events.append({
            "type": "divide",
            "title": "Divide",
            "explanation": "Split the points into left and right halves using the vertical dividing line.",
            "points": get_coordinates(px),
            "left_points": get_coordinates(left_x),
            "right_points": get_coordinates(right_x),
            "mid_x": mid_x,
            "depth": depth
        })

        d1, pair1 = solve(left_x, left_y, depth + 1)
        d2, pair2 = solve(right_x, right_y, depth + 1)

        if d1 <= d2:
            min_dist, best_pair = d1, pair1
        else:
            min_dist, best_pair = d2, pair2

        strip = [
            p for p in py
            if abs(p[0] - mid_x) < min_dist
        ]

        events.append({
            "type": "strip",
            "title": "Check the Middle Strip",
            "explanation": "Check points near the dividing line because a closer pair may cross between the two halves.",
            "points": get_coordinates(px),
            "strip_points": get_coordinates(strip),
            "mid_x": mid_x,
            "closest_pair": get_pair_coordinates(best_pair),
            "minimum_distance": min_dist,
            "depth": depth
        })

        for i in range(len(strip)):
            for j in range(i + 1, min(i + 8, len(strip))):
                if strip[j][1] - strip[i][1] >= min_dist:
                    break

                stats["comparisons"] += 1
                d = distance(strip[i], strip[j])

                if d < min_dist:
                    min_dist = d
                    best_pair = (strip[i], strip[j])

        events.append({
            "type": "combine",
            "title": "Combine",
            "explanation": "Compare the middle-strip points with the best pair found so far and keep the smallest distance.",
            "points": get_coordinates(px),
            "strip_points": get_coordinates(strip),
            "mid_x": mid_x,
            "closest_pair": get_pair_coordinates(best_pair),
            "minimum_distance": min_dist,
            "depth": depth
        })

        return min_dist, best_pair

    min_dist, pair = solve(points_x, points_y)

    end_time = time.perf_counter()

    result = {
        "closest_points": get_pair_coordinates(pair),
        "minimum_distance": min_dist,
        "recursive_calls": stats["recursive_calls"],
        "distance_comparisons": stats["comparisons"]
    }

    return result, end_time - start_time, events


if __name__ == "__main__":
    n = int(input("Enter number of points (minimum 10): "))

    if n < 10:
        raise ValueError("Input size must be at least 10.")

    points = []

    for i in range(n):
        x, y = map(float, input(f"Enter point {i + 1} (x y): ").split())
        points.append((x, y))

    result, execution_time, events = closest_pair(points)

    print("\nClosest Pair Results")
    print("--------------------")
    print("Closest Points:", result["closest_points"])
    print("Minimum Distance:", result["minimum_distance"])
    print("Recursive Calls:", result["recursive_calls"])
    print("Distance Comparisons:", result["distance_comparisons"])
    print("Execution Time:", execution_time, "seconds")
    print("Visualization Steps:", len(events))
