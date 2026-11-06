
import streamlit as st
import os
import sys
import matplotlib.pyplot as plt

project_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(project_folder, "closest_pair"))

from algorithm import closest_pair

input_folder = os.path.join(project_folder, "closest_pair", "input_files")


def draw_step(event):
    fig, ax = plt.subplots(figsize=(9, 5))

    points = event["points"]
    x = [p[0] for p in points]
    y = [p[1] for p in points]

    if event["type"] == "divide":
        left = event["left_points"]
        right = event["right_points"]

        if left:
            ax.scatter(
                [p[0] for p in left],
                [p[1] for p in left],
                label="Left Half"
            )

        if right:
            ax.scatter(
                [p[0] for p in right],
                [p[1] for p in right],
                label="Right Half"
            )

        mid_x = event["mid_x"]
        ax.axvline(mid_x, linestyle="--", label="Dividing Line")

    else:
        ax.scatter(x, y, label="Points")

        if event["type"] in ["strip", "combine"]:
            strip = event["strip_points"]

            if strip:
                ax.scatter(
                    [p[0] for p in strip],
                    [p[1] for p in strip],
                    label="Middle Strip"
                )

            mid_x = event["mid_x"]
            d = event["minimum_distance"]

            ax.axvspan(
                mid_x - d,
                mid_x + d,
                alpha=0.15,
                label="Strip Area"
            )

        pair = event["closest_pair"]

        if pair:
            p1, p2 = pair

            ax.scatter(
                [p1[0], p2[0]],
                [p1[1], p2[1]],
                label="Closest Pair"
            )

            ax.plot(
                [p1[0], p2[0]],
                [p1[1], p2[1]],
                linestyle="--",
                label="Distance"
            )

    ax.set_xlabel("X Coordinate")
    ax.set_ylabel("Y Coordinate")
    ax.set_title(event["title"])
    ax.legend()
    ax.grid(True, alpha=0.3)

    return fig


def show_closest_pair_page():
    st.title("Closest Pair of Points")
    st.write(
        "Explore how the Divide and Conquer algorithm finds "
        "the two closest points."
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

    selected_file = st.selectbox("Select an input file", files)

    if st.button("Run Closest Pair Algorithm"):
        file_path = os.path.join(input_folder, selected_file)

        with open(file_path, "r") as file:
            n = int(file.readline())
            points = [
                tuple(map(float, line.split()))
                for line in file
            ]

        if len(points) != n or n < 2:
            st.error("Invalid input file.")
            return

        result, execution_time, events = closest_pair(points)

        st.session_state["closest_pair_data"] = {
            "result": result,
            "execution_time": execution_time,
            "events": events,
            "input_size": n
        }

        st.session_state["step_index"] = 0

    if "closest_pair_data" not in st.session_state:
        st.info("Select an input file and click Run to begin.")
        return

    data = st.session_state["closest_pair_data"]
    result = data["result"]
    events = data["events"]

    st.subheader("Final Results")

    col1, col2, col3 = st.columns(3)

    col1.metric("Input Points", data["input_size"])
    col2.metric("Minimum Distance", f"{result['minimum_distance']:.4f}")
    col3.metric("Execution Time", f"{data['execution_time']:.6f} sec")

    st.write("**Closest Points:**", result["closest_points"])
    st.write("**Recursive Calls:**", result["recursive_calls"])
    st.write("**Distance Comparisons:**", result["distance_comparisons"])

    st.divider()

    st.subheader("Interactive Algorithm Working")

    total_steps = len(events)

    if total_steps == 0:
        st.warning("No visualization steps were generated.")
        return

    if "step_index" not in st.session_state:
        st.session_state["step_index"] = 0

    current_step = st.session_state["step_index"]
    current_step = min(current_step, total_steps - 1)

    st.progress((current_step + 1) / total_steps)

    st.write(f"Step {current_step + 1} of {total_steps}")

    event = events[current_step]

    st.subheader(event["title"])
    st.write(event["explanation"])

    if "minimum_distance" in event:
        st.write(
            "**Current minimum distance:**",
            f"{event['minimum_distance']:.4f}"
        )

    fig = draw_step(event)
    st.pyplot(fig)
    plt.close(fig)

    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        if st.button(
            "Previous Step",
            disabled=current_step == 0,
            use_container_width=True
        ):
            st.session_state["step_index"] -= 1
            st.rerun()

    with col2:
        new_step = st.slider(
            "Move through the algorithm",
            min_value=1,
            max_value=total_steps,
            value=current_step + 1,
            key="step_slider"
        )

        if new_step != current_step + 1:
            st.session_state["step_index"] = new_step - 1
            st.rerun()

    with col3:
        if st.button(
            "Next Step",
            disabled=current_step == total_steps - 1,
            use_container_width=True
        ):
            st.session_state["step_index"] += 1
            st.rerun()
