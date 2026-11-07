# This creates the page for users to input data.
# The collected data is appended to the 'data.csv' file.

import streamlit as st
import pandas as pd
import os
import csv

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Survey",
    page_icon="📝",
)

# PAGE TITLE AND USER DIRECTIONS
st.title("Data Collection Survey 📝")
st.write("Please fill out the form below to add your data to the dataset.")

# DATA INPUT FORM
with st.form("survey_form"):

    category_input = st.text_input(
        "Which Georgia Tech course are you taking?"
    )

    value_input = st.text_input(
        "How many hours do you study for this course per week?"
    )

    submitted = st.form_submit_button("Submit Data")

    if submitted:
        if category_input.strip() and value_input.strip():
            try:
                study_hours = float(value_input)

                if not (0 <= study_hours <= 168):
                    st.error("Please enter study hours between 0 and 168.")
                else:
                    course = category_input.strip().upper()

                    # Append the response to data.csv
                    with open("data.csv", "a", newline="") as file:
                        writer = csv.writer(file)
                        writer.writerow([course, study_hours])

                    st.success("Your data has been submitted!")
                    st.write(f"**Course:** {course}")
                    st.write(f"**Weekly Study Hours:** {study_hours}")

            except ValueError:
                st.error("Please enter a valid number for study hours.")
        else:
            st.warning("Please fill out both fields.")


# DATA DISPLAY
st.divider()
st.header("Survey Results Summary")

# Check whether the CSV file exists and contains data
if os.path.exists("data.csv") and os.path.getsize("data.csv") > 0:

    current_data_df = pd.read_csv("data.csv")

    if not current_data_df.empty:

        # Ensure study hours are numeric
        current_data_df["Value"] = pd.to_numeric(
            current_data_df["Value"], errors="coerce"
        )

        # Standardize course names
        current_data_df["Category"] = (
            current_data_df["Category"].astype(str).str.strip().str.upper()
        )

        # Remove invalid entries from the displayed summary
        current_data_df = current_data_df.dropna(subset=["Value"])

        # Group responses by course
        summary_df = current_data_df.groupby("Category").agg(
            Responses=("Value", "count"),
            Average_Hours=("Value", "mean")
        ).reset_index()

        # Round average study hours
        summary_df["Average_Hours"] = (
            summary_df["Average_Hours"].round(1)
        )

        # Rename columns
        summary_df.columns = [
            "Course",
            "Responses",
            "Average Study Hours"
        ]

        # Display the organized summary table
        st.dataframe(
            summary_df,
            hide_index=True,
            use_container_width=True
        )

    else:
        st.info("No survey responses have been collected yet.")

else:
    st.warning("The 'data.csv' file is empty or does not exist yet.")
