# This creates the page for displaying data visualizations.

import streamlit as st
import json
import pandas as pd
import matplotlib.pyplot as plt
# PAGE CONFIGURATION
st.set_page_config(
    page_title="Visuals",
    page_icon="📈",
)

# PAGE TITLE
st.title("Data Visualizations 📈")


# PART 1: GRAPHS FROM data.json
# --- YOUR CODE GOES HERE ---

with open("data.json", "r") as file:
    data = json.load(file)

df = pd.DataFrame(data["data_points"])

st.header("Weekly Study Hours")

st.bar_chart(df, x="label", y="value")

st.header("Study Time Distribution")

if "subjects" not in st.session_state:
    st.session_state.subjects = df["label"].tolist()

selected = st.multiselect(
    "Select subjects:",
    df["label"].tolist(),
    key="subjects"
)

filtered = df[df["label"].isin(selected)]

# EXTRA CREDIT: Mean and Median for JSON data
if not filtered.empty:
    json_mean = filtered["value"].mean()
    json_median = filtered["value"].median()

    if "previous_json_mean" not in st.session_state:
        st.session_state.previous_json_mean = json_mean

    if "previous_json_median" not in st.session_state:
        st.session_state.previous_json_median = json_median

    mean_change = json_mean - st.session_state.previous_json_mean
    median_change = json_median - st.session_state.previous_json_median

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Mean Study Hours",
            f"{json_mean:.2f}",
            delta=f"{mean_change:+.2f}"
        )

    with col2:
        st.metric(
            "Median Study Hours",
            f"{json_median:.2f}",
            delta=f"{median_change:+.2f}"
        )

    st.session_state.previous_json_mean = json_mean
    st.session_state.previous_json_median = json_median


if not filtered.empty:
    fig, ax = plt.subplots()
    ax.pie(
        filtered["value"],
        labels=filtered["label"],
        autopct="%1.1f%%"
    )
    ax.set_title("Study Time by Subject")
    st.pyplot(fig)
    plt.close(fig)
else:
    st.warning("Please select at least one subject.")

# PART 2: GRAPHS FROM data.csv
# --- YOUR CODE GOES HERE ---
st.divider()
st.header("Student Survey Results")

# Read the CSV data
csv_df = pd.read_csv("data.csv")

# Calculate average study hours for each course
average_hours = csv_df.groupby("Category")["Value"].mean()

# STATIC VISUALIZATION: BAR CHART
st.subheader("Average Weekly Study Hours by Course")

fig2, ax2 = plt.subplots(figsize=(8, 5))

ax2.bar(average_hours.index, average_hours.values, color="steelblue")

ax2.set_title("Average Study Hours by Course")
ax2.set_xlabel("Course")
ax2.set_ylabel("Average Weekly Study Hours")

st.pyplot(fig2)
plt.close(fig2)



# DYNAMIC VISUALIZATION: PIE CHART
st.subheader("Study Hours Distribution by Course")

# Initialize session state
if "csv_courses" not in st.session_state:
    st.session_state.csv_courses = average_hours.index.tolist()

# Let users select courses
selected_courses = st.multiselect(
    "Select courses to include:",
    average_hours.index.tolist(),
    key="csv_courses"
)

# Filter the CSV data based on the selected courses
selected_hours = average_hours[
    average_hours.index.isin(selected_courses)
]

# EXTRA CREDIT: Mean and Median for CSV data
if not selected_hours.empty:
    csv_mean = selected_hours.mean()
    csv_median = selected_hours.median()

    # Store previous statistics using session state
    if "previous_csv_mean" not in st.session_state:
        st.session_state.previous_csv_mean = csv_mean

    if "previous_csv_median" not in st.session_state:
        st.session_state.previous_csv_median = csv_median

    # Calculate changes from the previous selection
    mean_change = csv_mean - st.session_state.previous_csv_mean
    median_change = csv_median - st.session_state.previous_csv_median

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Mean Study Hours",
            f"{csv_mean:.2f}",
            delta=f"{mean_change:+.2f}"
        )

    with col2:
        st.metric(
            "Median Study Hours",
            f"{csv_median:.2f}",
            delta=f"{median_change:+.2f}"
        )

    # Save current statistics for the next interaction
    st.session_state.previous_csv_mean = csv_mean
    st.session_state.previous_csv_median = csv_median

# Display the dynamic chart
if not selected_hours.empty and selected_hours.sum() > 0:
    fig3, ax3 = plt.subplots(figsize=(8, 5))

    ax3.pie(
        selected_hours.values,
        labels=selected_hours.index,
        autopct="%1.1f%%",
        startangle=90
    )

    ax3.set_title("Average Study Hours Distribution")
    st.pyplot(fig3)
    plt.close(fig3)
else:
    st.warning("Please select at least one course with study hours.")

