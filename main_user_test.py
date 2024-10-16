import time
import streamlit.components.v1 as components
import streamlit as st


class UserGUI:
    t = 3  # Time default sleep
    conn = st.connection("snowflake")
    questions_df = conn.query("SELECT * FROM PROD_DATASCIENCE_DB.PRJ_003_WHOWANTSTOBEAMILLIONAIRE.QUESTIONS", ttl=600)

    def __init__(self):
        if 'current_page' not in st.session_state:
            st.session_state.current_page = 'add_code_page'
        if 'debug' not in st.session_state:
            st.session_state.debug = True
        if 'index_questions_df' not in st.session_state:
            st.session_state.index_questions_df = 0

    def reload_page(self):
        time.sleep(self.t)
        st.rerun()

    def next_page(self, name_page:str):
        st.session_state.current_page = name_page
        self.reload_page()

    def add_code_page(self):
        st.header("JOIN TO GAME")
        st.text_input(
            "Insert Here Your Game Code!",
            key='code_input'
        )

        if st.button("JOIN", key="join_button"):
            # Check if input is right
            st.success("Hi!")
            self.next_page("register_page")

    def register_page(self):
        st.header("Register Here!")
        st.write(f"Now that you joined the game ({st.session_state.code_input}), you need to register:")

        register_values = ['Name', 'Date Birth', 'Name Group']

        for value in register_values:
            st.text_input(
                f"{value}",
                key=f"user_{value.lower().replace('', '_')}"
            )

        if st.button("Register Your Group"):
            st.success("You Registered a Group!")
            self.next_page("question_page")

    def question_page(self):
        def set_answer_container():
            q_text = "Holaaaa"

            html_code = """
            <div style="cursor: pointer; padding: 20px; text-align: center; background-color: white;">
                <p onclick="handleClick()">
                    <span style='text-decoration: line-through double red;'>""" + q_text + """</span>!
                </p>
            </div>
            
            <script>
                function handleClick() {
                  alert("You clicked the text!");
                }
            </script>
            """

            # Use components.html to display the HTML
            components.html(html_code, height=100)

        st.header("Question Time! 🥳🥳")

        q = self.questions_df.iloc[st.session_state.index_questions_df]
        # st.write(q)
        st.subheader(q["QUESTION"])  # Show Question

        col1, col2 = st.columns(2)
        with col1:
            container_A = st.container(border=True)
            container_C = st.container(border=True)
        with col2:
            container_B = st.container(border=True)
            container_D = st.container(border=True)

        answers = [q["CORRECT_ANSWER"], q["INCORRECT_OPTION_1"], q["INCORRECT_OPTION_2"], q["INCORRECT_OPTION_3"]]
        answer_containers = [container_A, container_B, container_C, container_D]
        button_colors = {
            "Green": "#4CAF50",
            "Blue": "#008CBA",
            "Red": "#f44336",
            "Orange": "#ff9800"
        }

        for i in range(4):
            answer_containers[]

        if st.button("Check"):
            if st.session_state.index_questions_df < len(self.questions_df):
                st.session_state.index_questions_df += 1
                self.reload_page()

    def run(self):
        if st.session_state.debug:
            st.session_state.current_page = "question_page"

        if st.session_state.current_page == "add_code_page":
            self.add_code_page()
        elif st.session_state.current_page == "register_page":
            self.register_page()
        elif st.session_state.current_page == "question_page":
            self.question_page()


app = UserGUI()
app.run()
