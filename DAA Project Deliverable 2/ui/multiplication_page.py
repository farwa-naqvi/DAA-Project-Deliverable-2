import streamlit as st
import os
import csv
import importlib.util
import matplotlib.pyplot as plt

project_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
multiplication_folder = os.path.join(project_folder, "integer_multiplication")

# Both algorithm folders contain a file called algorithm.py, so load this one
# under its own module name to avoid clashing with closest_pair/algorithm.py
_spec = importlib.util.spec_from_file_location(
    "integer_multiplication_algorithm",
    os.path.join(multiplication_folder, "algorithm.py")
)
_algorithm = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_algorithm)

multiply = _algorithm.multiply
schoolbook_multiply = _algorithm.schoolbook_multiply

input_folder = os.path.join(multiplication_folder, "input_files")
results_csv = os.path.join(multiplication_folder, "results", "results.csv")


def short(n):
    """Shorten very long numbers so they fit on screen."""
    s = str(n)
    if len(s) <= 24:
        return s
    return f"{s[:10]}...{s[-10:]} ({len(s)} digits)"


def describe_step(event):
    """Show the numbers involved in one step."""
    if event["type"] == "divide":
        st.write(f"**x** = {short(event['x'])}")
        st.write(f"**y** = {short(event['y'])}")
        st.write(f"**Split position m** = {event['m']} digits")
        st.write(f"**a** = {short(event['a'])}, **b** = {short(event['b'])}")
        st.write(f"**c** = {short(event['c'])}, **d** = {short(event['d'])}")
    elif event["type"] == "combine":
        st.write(f"**a x c** = {short(event['ac'])}")
        st.write(f"**b x d** = {short(event['bd'])}")
        st.write(f"**(a + b) x (c + d)** = {short(event['abcd'])}")
        st.write(
            "**a x d + b x c** = (a + b)(c + d) - ac - bd = "
            f"{short(event['ad_bc'])}"
        )
        st.write(f"**Result** = {short(event['result'])}")
    else:
        st.write(f"**x** = {short(event['x'])}, **y** = {short(event['y'])}")
        st.write(f"**Result** = {short(event['result'])}")


def build_tree(events):
    """Work out position and progress of every call in the recursion tree."""
    nodes = {}
    for index, event in enumerate(events):
        node = nodes.setdefault(event["node_id"], {
            "id": event["node_id"],
            "parent": event["parent_id"],
            "depth": event["depth"],
            "digits": max(len(str(event["x"])), len(str(event["y"]))),
            "first": index,
            "last": index,
            "children": []
        })
        node["last"] = index

    for node in nodes.values():
        if node["parent"] is not None:
            nodes[node["parent"]]["children"].append(node["id"])

    next_leaf = [0]

    def place(node_id):
        node = nodes[node_id]
        if not node["children"]:
            node["pos"] = next_leaf[0]
            next_leaf[0] += 1
        else:
            for child in node["children"]:
                place(child)
            positions = [nodes[c]["pos"] for c in node["children"]]
            node["pos"] = sum(positions) / len(positions)

    place(0)
    return nodes


def draw_step(events, nodes, current_step):
    fig, ax = plt.subplots(figsize=(9, 5))

    active_id = events[current_step]["node_id"]

    for node in nodes.values():
        if node["parent"] is not None:
            parent = nodes[node["parent"]]
            ax.plot(
                [parent["pos"], node["pos"]],
                [-parent["depth"], -node["depth"]],
                color="gray", alpha=0.5, zorder=1
            )

    groups = {"Finished": [], "In progress": [], "Not started yet": []}
    for node in nodes.values():
        if node["id"] == active_id:
            continue
        if node["last"] <= current_step:
            groups["Finished"].append(node)
        elif node["first"] <= current_step:
            groups["In progress"].append(node)
        else:
            groups["Not started yet"].append(node)

    colors = {
        "Finished": "tab:green",
        "In progress": "tab:orange",
        "Not started yet": "lightgray"
    }

    for label, group in groups.items():
        if group:
            ax.scatter(
                [n["pos"] for n in group],
                [-n["depth"] for n in group],
                s=450, color=colors[label], label=label, zorder=2
            )

    active = nodes[active_id]
    ax.scatter(
        [active["pos"]], [-active["depth"]],
        s=600, color="tab:red", label="Current call", zorder=3
    )

    for node in nodes.values():
        ax.text(
            node["pos"], -node["depth"], str(node["digits"]),
            ha="center", va="center", fontsize=7, zorder=4
        )

    max_depth = max(n["depth"] for n in nodes.values())
    ax.set_yticks([-d for d in range(max_depth + 1)])
    ax.set_yticklabels([f"Level {d}" for d in range(max_depth + 1)])
    ax.set_xticks([])
    ax.set_title("Recursion Tree (numbers inside circles = digits)")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.02), ncol=4,
              fontsize=8, markerscale=0.4)
    ax.grid(True, axis="y", alpha=0.3)

    return fig


def draw_comparison():
    """Plot the saved results of run_datasets.py for all 10 input files."""
    if not os.path.exists(results_csv):
        return None

    digits, karatsuba_time, school_time = [], [], []
    with open(results_csv, newline="") as file:
        for row in csv.DictReader(file):
            digits.append(int(row["Digits"]))
            karatsuba_time.append(float(row["Karatsuba Time"]))
            school_time.append(float(row["Schoolbook Time"]))

    if not digits:
        return None

    fig, ax = plt.subplots(figsize=(9, 4))
    ax.plot(digits, school_time, marker="o", label="Schoolbook O(n^2)")
    ax.plot(digits, karatsuba_time, marker="o", label="Karatsuba O(n^1.585)")
    ax.set_xlabel("Number of Digits")
    ax.set_ylabel("Execution Time (seconds)")
    ax.set_title("Running Time on All 10 Datasets")
    ax.legend()
    ax.grid(True, alpha=0.3)

    return fig


def go_to_step(step):
    st.session_state["mult_step_index"] = step
    st.session_state["mult_step_slider"] = step + 1


def show_multiplication_page():
    st.title("Integer Multiplication")
    st.write(
        "Explore how the Divide and Conquer algorithm (Karatsuba) "
        "multiplies two very large integers."
    )

    if not os.path.exists(input_folder):
        st.warning("Input folder not found. Generate the input files first.")
        return

    files = sorted(
        [f for f in os.listdir(input_folder) if f.endswith(".txt")],
        key=lambda f: int(f.split("_")[1].split(".")[0])
    )

    if not files:
        st.warning("No input files found. Generate the input files first.")
        return

    selected_file = st.selectbox(
        "Select an input file", files, key="mult_selected_file"
    )

    if st.button("Run Integer Multiplication Algorithm"):
        file_path = os.path.join(input_folder, selected_file)

        with open(file_path, "r") as file:
            lines = [line.strip() for line in file if line.strip()]

        if len(lines) != 2 or not all(line.isdigit() for line in lines):
            st.error("Invalid input file.")
            return

        x, y = int(lines[0]), int(lines[1])

        result, execution_time, events = multiply(x, y)
        school_product, school_time, digit_mults = schoolbook_multiply(x, y)

        st.session_state["multiplication_data"] = {
            "x": x,
            "y": y,
            "file": selected_file,
            "result": result,
            "execution_time": execution_time,
            "events": events,
            "nodes": build_tree(events),
            "school_time": school_time,
            "digit_mults": digit_mults,
            "verified": result["product"] == school_product == x * y
        }

        go_to_step(0)

    if "multiplication_data" not in st.session_state:
        st.info("Select an input file and click Run to begin.")
        return

    data = st.session_state["multiplication_data"]
    result = data["result"]
    events = data["events"]

    st.subheader("Final Results")

    col1, col2, col3 = st.columns(3)

    col1.metric("Digits per Number", result["digits_x"])
    col2.metric("Karatsuba Time", f"{data['execution_time']:.6f} sec")
    col3.metric("Schoolbook Time", f"{data['school_time']:.6f} sec")

    st.write("**File:**", data["file"])
    st.write("**Recursive Calls (Karatsuba):**", result["recursive_calls"])
    st.write("**Base Cases (Karatsuba):**", result["base_cases"])
    st.write(
        "**Digit Multiplications (Schoolbook):**", data["digit_mults"]
    )

    if data["verified"]:
        st.success("Both algorithms gave the same product.")
    else:
        st.error("The two algorithms gave different products.")

    with st.expander("Show the full numbers and product"):
        st.write("**First number:**")
        st.code(str(data["x"]), language=None)
        st.write("**Second number:**")
        st.code(str(data["y"]), language=None)
        st.write("**Product:**")
        st.code(str(result["product"]), language=None)

    st.divider()

    st.subheader("Interactive Algorithm Working")

    total_steps = len(events)

    if total_steps == 0:
        st.warning("No visualization steps were generated.")
        return

    st.session_state.setdefault("mult_step_index", 0)
    st.session_state.setdefault("mult_step_slider", 1)

    current_step = min(st.session_state["mult_step_index"], total_steps - 1)

    st.progress((current_step + 1) / total_steps)

    st.write(f"Step {current_step + 1} of {total_steps}")

    event = events[current_step]

    st.subheader(f"{event['title']} (Level {event['depth']})")
    st.write(event["explanation"])

    describe_step(event)

    fig = draw_step(events, data["nodes"], current_step)
    st.pyplot(fig)
    plt.close(fig)

    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        st.button(
            "Previous Step",
            key="mult_previous",
            disabled=current_step == 0,
            use_container_width=True,
            on_click=go_to_step,
            args=(current_step - 1,)
        )

    with col2:
        if total_steps > 1:
            new_step = st.slider(
                "Move through the algorithm",
                min_value=1,
                max_value=total_steps,
                key="mult_step_slider"
            )

            if new_step != current_step + 1:
                st.session_state["mult_step_index"] = new_step - 1
                st.rerun()

    with col3:
        st.button(
            "Next Step",
            key="mult_next",
            disabled=current_step == total_steps - 1,
            use_container_width=True,
            on_click=go_to_step,
            args=(current_step + 1,)
        )

    st.divider()

    st.subheader("Performance on All Datasets")

    comparison = draw_comparison()

    if comparison is None:
        st.info("Run integer_multiplication/run_datasets.py to see this chart.")
    else:
        st.pyplot(comparison)
        plt.close(comparison)
