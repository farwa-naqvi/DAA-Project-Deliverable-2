import os
import random

# Run this from the project root, same as closest_pair/generate_inputs.py
output_folder = "integer_multiplication/input_files"
os.makedirs(output_folder, exist_ok=True)

# number of digits in each of the two integers (all > 100)
input_sizes = [101, 150, 200, 300, 400, 500, 750, 1000, 1500, 2000]

for i, digits in enumerate(input_sizes, start=1):

    x = random.randint(10 ** (digits - 1), 10 ** digits - 1)
    y = random.randint(10 ** (digits - 1), 10 ** digits - 1)

    file_path = os.path.join(output_folder, f"input_{i}.txt")

    with open(file_path, "w") as file:
        file.write(str(x) + "\n")
        file.write(str(y) + "\n")

    print(f"Generated input_{i}.txt with two {digits}-digit integers")

print("\nAll 10 input files generated successfully.")
