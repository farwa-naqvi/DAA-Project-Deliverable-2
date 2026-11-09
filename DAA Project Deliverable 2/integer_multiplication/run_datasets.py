import os
import csv
from algorithm import multiply, schoolbook_multiply

input_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input_files")
results_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")

os.makedirs(results_folder, exist_ok=True)

results = []

for i in range(1, 11):

    file_path = os.path.join(input_folder, f"input_{i}.txt")

    with open(file_path, "r") as file:
        x = int(file.readline())
        y = int(file.readline())

    result, execution_time, events = multiply(x, y)
    school_product, school_time, digit_mults = schoolbook_multiply(x, y)

    correct = result["product"] == school_product == x * y

    if not correct:
        raise ValueError(f"Wrong product for input_{i}.txt")

    digits = len(str(x))

    results.append([
        f"input_{i}.txt",
        digits,
        result["recursive_calls"],
        result["base_cases"],
        execution_time,
        digit_mults,
        school_time,
        correct
    ])

    print(f"\nInput File: input_{i}.txt")
    print(f"Digits per Number: {digits}")
    print(f"Recursive Calls: {result['recursive_calls']}")
    print(f"Base Cases: {result['base_cases']}")
    print(f"Karatsuba Time: {execution_time:.6f} seconds")
    print(f"Schoolbook Digit Multiplications: {digit_mults}")
    print(f"Schoolbook Time: {school_time:.6f} seconds")
    print(f"Product Verified: {correct}")

csv_path = os.path.join(results_folder, "results.csv")

with open(csv_path, "w", newline="") as file:
    writer = csv.writer(file)

    writer.writerow([
        "Input File",
        "Digits",
        "Recursive Calls",
        "Base Cases",
        "Karatsuba Time",
        "Schoolbook Digit Multiplications",
        "Schoolbook Time",
        "Product Verified"
    ])

    writer.writerows(results)

print("\nAll datasets processed successfully.")
print(f"Results saved in: {csv_path}")
