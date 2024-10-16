import streamlit as st
import pandas as pd
import os

csv_path = os.path.join("utils", "db", "questions.csv")
music_path = os.path.join(os.getcwd(), "utils", "music", "music_test.mp3")


def load_questions(csv_file):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file)

    # Convert options from CSV rows into a list of questions
    questions = []
    for index, row in df.iterrows():
        questions.append({
            'question': row['Question'],
            'options': [row['Option_A'], row['Option_B'], row['Option_C'], row['Option_D']],
            'correct_answer': row['CorrectAnswer']
        })
    return questions


# Set Questions
all_questions = load_questions(csv_path)


def multiple_choice(question, answers, correct_answer, key):
    # Add a selectbox for the question
    select_box = st.selectbox(question, answers, key=f"{key}_selectbox")

    return select_box


# Define the "Start Game" page
def start_page():
    st.title("Welcome to the Quiz Game!")
    video_code = """
    <iframe width="900" height="600" 
    src="https://www.youtube.com/embed/l7LHPMUbkAc?si=ZDUmCx8jfNzAIHC-&autoplay=1&mute=1&controls=0&loop=1&playlist=l7LHPMUbkAc" 
    title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope"></iframe>
    """
    st.markdown(video_code, unsafe_allow_html=True)

    st.audio(music_path, format="audio/mp3", loop=True, autoplay=True)

    # Button to navigate to the game page
    if st.button('Start Game'):
        # Ensure session state is updated before rendering
        st.session_state.page = "game"
        st.rerun()  # Re-run the app to reflect the page change


# Define the game page
def game_page():
    # Get the current question index
    question_idx = st.session_state.current_question

    if 'is_checked' not in st.session_state:
        st.session_state.is_checked = False

    if question_idx < len(all_questions):
        # Display the current question
        q = all_questions[question_idx]
        ans = multiple_choice(
            q['question'],
            q['options'],
            q['correct_answer'],
            key=f"question_{question_idx}"
        )

        if not st.session_state.is_checked:
            if st.button('Check'):

                st.session_state.is_checked = True
                st.rerun()
        else:
            if q['correct_answer'] == ans:
                st.success("Well Done!!")
            else:
                st.error("Nice Try!")

            if st.button('Next'):
                st.session_state.is_checked = False
                st.session_state.current_question += 1
                st.rerun()

    else:
        st.write("Quiz Finished! Thanks for playing!")


# Main function to handle navigation
def main_st():
    if 'page' not in st.session_state:
        st.session_state.page = "start"  # Default page is start page
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0  # Start at the first question

    if st.session_state.page == "start":
        start_page()
    elif st.session_state.page == "game":
        game_page()


if __name__ == "__main__":
    main_st()
