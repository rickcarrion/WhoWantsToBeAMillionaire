import streamlit as st
import pandas as pd
import os

csv_path = os.path.join("utils", "db", "questions.csv")

def main_st():
    # Initial data for questions (can be loaded from a database or CSV later)
    if "questions_data" not in st.session_state:
        questions_csv = open(csv_path)

        if not questions_csv:
            st.session_state.questions_data = pd.DataFrame({
                "Question": [],
                "A": [],
                "B": [],
                "C": [],
                "D": [],
                "Correct Answer": [],
                "Use This Question": []
            })

            # Set the "Use This Question" column to Boolean
            st.session_state.questions_data["Use This Question"] = st.session_state.questions_data["Use This Question"].\
                astype(bool)
        else:
            st.session_state.questions_data = pd.read_csv(csv_path)

        questions_csv.close()

    # Display existing questions
    st.title("Who Wants to Be a Millionaire - Question Manager")
    st.subheader("Existing Questions")

    # Checkbox and Show Table
    columns_data = st.data_editor(
        st.session_state.questions_data,
        column_config={
           "Use This Question": st.column_config.CheckboxColumn(
               "Use This Question",
               default=True
           )
           },
        disabled=["Question", "A", "B", "C", "D", "Correct Answer"],
        hide_index=True
        )

    st.session_state.questions_data = columns_data

    # Input fields for adding new questions
    st.subheader("Add New Question")

    with st.form(key="add_question_form"):
        question = st.text_input("Question")
        option_a = st.text_input("Option A")
        option_b = st.text_input("Option B")
        option_c = st.text_input("Option C")
        option_d = st.text_input("Option D")
        correct_answer = st.selectbox("Correct Answer", ("A", "B", "C", "D"))

        submit_button = st.form_submit_button(label="Add Question")

    # Add the new question to the data if submitted
    if submit_button:
        new_data = pd.DataFrame({
            "Question": [question],
            "A": [option_a],
            "B": [option_b],
            "C": [option_c],
            "D": [option_d],
            "Correct Answer": [correct_answer],
            "Use This Question": [True]
        })
        # Use pd.concat to add new data
        st.session_state.questions_data = pd.concat([st.session_state.questions_data, new_data], ignore_index=True)
        st.success("Question added successfully!")
        st.rerun()  # This will refresh the app

    # Option to download the data as CSV
    # st.subheader("Download Questions Data")
    csv_data = st.session_state.questions_data.to_csv(index=False)
    st.download_button(
        label="Start Game",
        data=csv_data,
        file_name=os.path.join(".", "utils", "db", "questions_app.csv"),
        mime="text/csv"
    )
