import streamlit as st
import random
import string
import os
import time
import threading

music_path = os.path.join(os.getcwd(), "utils", "music", "music_test.mp3")

class StreamlitApp:
    def __init__(self):
        if 'logged_in' not in st.session_state:
            st.session_state.logged_in = False
        if 'current_page' not in st.session_state:
            st.session_state.current_page = "start_page"
        if 'session_game_code' not in st.session_state:
            st.session_state.session_game_code = None

    @staticmethod
    def idx_to_num(idx):
        return chr(97 + idx)

    @staticmethod
    def generate_code(length=6):
        # Generate the first three letters (uppercase)
        letters = ''.join(random.choices(string.ascii_uppercase, k=3)).upper()
        # Generate the last three digits
        digits = ''.join(random.choices(string.digits, k=3))

        # Combine the letters and digits
        code = letters + '-' +digits
        return code

    def start_page(self):
        #st.title("Welcome to WHO WANTS TO BE A MILLIONAIRE Game!")
        video_code = """
            <iframe width="900" height="600" 
            src="https://www.youtube.com/embed/l7LHPMUbkAc?si=ZDUmCx8jfNzAIHC-&autoplay=1&mute=1&controls=0&loop=1&playlist=l7LHPMUbkAc" 
            title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope"></iframe>
            """
        st.markdown(video_code, unsafe_allow_html=True)

        st.audio(music_path, format="audio/mp3", loop=True, autoplay=True)

        if st.button('Generate Game Code'):
            # Ensure session state is updated before rendering
            st.session_state.session_game_code = self.generate_code()
            st.header('Your Game Code is "{}"'.format(st.session_state.session_game_code))

        # Button to navigate to the game page
        if st.button('Start Game'):
            # Ensure session state is updated before rendering
            st.session_state.current_page = "game_questions"
            st.rerun()  # Re-run the app

    def countdown_timer(self, duration):
        """Countdown timer that updates the session state."""
        while duration > 0:
            time.sleep(1)
            duration -= 1
            st.session_state.time_left = duration
            st.rerun()  # Rerun to update the timer display

    def game_questions(self):
        question_time = 10
        if "success_message" not in st.session_state:
            st.session_state.success_message = False
        if "time_left" not in st.session_state:
            st.session_state.time_left = question_time
        if "correct_ans" not in st.session_state:
            st.session_state.correct_ans = "???"

        q = {
            "Question": "What is the capital of France?",
            "Answers": ["Paris", "Rome", "Berlin", "Madrid"],
            "CorrectAnswer": 0
        }

        st.header("Question!")

        col1, col2 = st.columns(2)
        with col1:
            st.write(q["Question"])

        with col2:
            # Timer in col2
            timer_placeholder = st.empty()  # Placeholder for the timer display

        st.markdown("---")

        # Show all the answers
        for idx, ans in enumerate(q["Answers"]):
            st.write(f"{self.idx_to_num(idx)}: {ans}")

        st.success(f"The correct answer was: {st.session_state.correct_ans}")

        # Timer countdown
        while st.session_state.time_left > 0:
            timer_placeholder.write(f"⏳ Time left: {st.session_state.time_left} seconds")
            time.sleep(1)
            st.session_state.time_left -= 1
            st.rerun()

        # Show Answer button
        with col2:
            if st.button("Show Answer"):
                st.session_state.success_message = True
                st.session_state.correct_ans = q["Answers"][q["CorrectAnswer"]]
                st.rerun()

        if st.session_state.success_message:
            # Reset timer and state for next question
            if st.button("Next"):
                st.session_state.success_message = False
                st.session_state.correct_ans = "???"
                st.session_state.time_left = question_time
                st.rerun()  # Rerun to update the UI

    def run(self):
        if st.session_state.current_page == 'start_page':
            self.start_page()
        if st.session_state.current_page == "game_questions":
            self.game_questions()
