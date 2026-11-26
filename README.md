# Divide and Conquer Project (DAA Deliverable 2)

Interactive Streamlit demo of two Divide and Conquer algorithms.

## Group Members
- Amnn Jindani (24K-2584)
- Farwa Batool Naqvi (24L-2508)

## Algorithms
| Algorithm | Technique | Complexity |
|---|---|---|
| Closest Pair of Points | Split by x, check the middle strip | O(n log n) |
| Integer Multiplication (Karatsuba) | 3 recursive multiplications instead of 4 | O(n^1.585) |

## How to run
```bash
pip install streamlit matplotlib
cd "DAA Project Deliverable 2"
python main.py
```

## Project structure
- `closest_pair/`, `integer_multiplication/`: `algorithm.py`, `generate_inputs.py`, `run_datasets.py`, `input_files/`, `results/results.csv`
- `ui/`: Streamlit dashboard and pages
- `main.py`: launches the dashboard

## Regenerating data (run from project root)
```bash
python closest_pair/generate_inputs.py
python integer_multiplication/generate_inputs.py
python closest_pair/run_datasets.py
python integer_multiplication/run_datasets.py
```
