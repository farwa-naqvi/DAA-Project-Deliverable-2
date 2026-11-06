
import streamlit as st
import os
import sys
import matplotlib.pyplot as plt

project_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(project_folder, "closest_pair"))

from algorithm import closest_pair

input_folder = os.path.join(project_folder, "closest_pair", "input_files")


def show_closest_pair_page():
    st.title("Closest Pair of Points")
    st.write("Find the two closest points using the Divide and Conquer algorithm.")

    files = [
        f for f in os.listdir(input_folder)
        if f.endswith(".txt")
    ] if os.path.exists(input_folder) else []

    if not files:
        st.warning("No input files found. Generate the input files first.")
        return

    selected_file = st.selectbox("Select an input file", sorted(files))

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

        result, execution_time, steps = closest_pair(points)

        st.subheader("Results")

        col1, col2 = st.columns(2)
        col1.metric("Number of Points", n)
        col2.metric("Minimum Distance", f"{result['minimum_distance']:.4f}")

        st.write("**Closest Points:**", result["closest_points"])
        st.write("**Execution Time:**", f"{execution_time:.6f} seconds")
        st.write("**Recursive Calls:**", result["recursive_calls"])
        st.write("**Distance Comparisons:**", result["distance_comparisons"])

        st.subheader("Points Visualization")

        fig, ax = plt.subplots()

        x = [p[0] for p in points]
        y = [p[1] for p in points]

        ax.scatter(x, y, label="All Points")

        p1, p2 = result["closest_points"]

        ax.scatter(
            [p1[0], p2[0]],
            [p1[1], p2[1]],
            label="Closest Pair"
        )

        ax.plot(
            [p1[0], p2[0]],
            [p1[1], p2[1]]
        )

        ax.set_xlabel("X Coordinate")
        ax.set_ylabel("Y Coordinate")
        ax.set_title("Closest Pair of Points")
        ax.legend()

        st.pyplot(fig)

        st.subheader("Algorithm Working")

        for step in steps:
            st.write("•", step)
