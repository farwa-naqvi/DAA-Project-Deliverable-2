
import os
import csv
import time
from algorithm import closest_pair

input_folder = os.path.join(os.path.dirname(__file__), "input_files")
results_folder = os.path.join(os.path.dirname(__file__), "results")

os.makedirs(results_folder, exist_ok=True)

results = []

for i in range(1, 11):

    file_path = os.path.join(input_folder, f"input_{i}.txt")

    with open(file_path, "r") as file:
        n = int(file.readline())
        points = []

        for line in file:
            x, y = map(float, line.split())
            points.append((x, y))

    if len(points) != n:
        raise ValueError(f"Invalid number of points in input_{i}.txt")

    result, execution_time, steps = closest_pair(points)

    results.append([
        f"input_{i}.txt",
        n,
        result["closest_points"],
        result["minimum_distance"],
        result["recursive_calls"],
        result["distance_comparisons"],
        execution_time
    ])

    print(f"\nInput File: input_{i}.txt")
    print(f"Number of Points: {n}")
    print(f"Closest Pair: {result['closest_points']}")
    print(f"Minimum Distance: {result['minimum_distance']:.4f}")
    print(f"Recursive Calls: {result['recursive_calls']}")
    print(f"Distance Comparisons: {result['distance_comparisons']}")
    print(f"Execution Time: {execution_time:.6f} seconds")

csv_path = os.path.join(results_folder, "results.csv")

with open(csv_path, "w", newline="") as file:
    writer = csv.writer(file)

    writer.writerow([
        "Input File",
        "Input Size",
        "Closest Points",
        "Minimum Distance",
        "Recursive Calls",
        "Distance Comparisons",
        "Execution Time"
    ])

    writer.writerows(results)

print("\nAll datasets processed successfully.")
print(f"Results saved in: {csv_path}")
