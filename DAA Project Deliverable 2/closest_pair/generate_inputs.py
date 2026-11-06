
import os
import random

output_folder = "closest_pair/input_files"
os.makedirs(output_folder, exist_ok=True)

input_sizes = [120, 200, 350, 500, 750, 1000, 1500, 2000, 3000, 5000]

for i, n in enumerate(input_sizes, start=1):

    points = set()

    while len(points) < n:
        x = random.randint(0, 100000)
        y = random.randint(0, 100000)
        points.add((x, y))

    points = list(points)

    file_path = os.path.join(output_folder, f"input_{i}.txt")

    with open(file_path, "w") as file:
        file.write(str(n) + "\n")

        for x, y in points:
            file.write(f"{x} {y}\n")

    print(f"Generated input_{i}.txt with {n} points")

print("\nAll 10 input files generated successfully.")
