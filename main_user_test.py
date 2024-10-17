import time
import random
import streamlit as st
import snowflake.connector
from snowflake.connector import ProgrammingError
import pandas as pd
import uuid


def generate_unique_id():
    return str(uuid.uuid4())  # Generates a random UUID


def exe_sf(conn, sql: str, return_as_df=True):
    cur = conn
    try:
        cursor = cur.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()

        # Convert data to DataFrame
        if return_as_df:
            columns = [col[0] for col in cursor.description]
            dataframe = pd.DataFrame(data, columns=columns)
            return dataframe
        else:
            return data

    finally:
        cur.close()

def create_conn():
    return snowflake.connector.connect(
            user=st.secrets["snowflake"]["user"],
            password=st.secrets["snowflake"]["password"],
            role=st.secrets["snowflake"]["role"],
            account=st.secrets["snowflake"]["account"],
            warehouse=st.secrets["snowflake"]["warehouse"],
            database=st.secrets["snowflake"]["database"],
            schema=st.secrets["snowflake"]["schema"]
        )

class UserGUI:
    t = 0  # Time default sleep
    if False:
        conn = st.connection("snowflake")

        questions_df = conn.query("SELECT * FROM PROD_DATASCIENCE_DB.PRJ_003_WHOWANTSTOBEAMILLIONAIRE.QUESTIONS")
        score_df = conn.query("SELECT s.SCORE FROM PROD_DATASCIENCE_DB.PRJ_003_WHOWANTSTOBEAMILLIONAIRE.SCORE s")
    else:
        questions_df = exe_sf(create_conn(), sql="SELECT * FROM PROD_DATASCIENCE_DB.PRJ_003_WHOWANTSTOBEAMILLIONAIRE.QUESTIONS")
        score_df = exe_sf(create_conn(), sql="SELECT s.SCORE FROM PROD_DATASCIENCE_DB.PRJ_003_WHOWANTSTOBEAMILLIONAIRE.SCORE s")


    def __init__(self):
        if 'current_page' not in st.session_state:
            st.session_state.current_page = 'add_code_page'

        if 'debug' not in st.session_state:
            st.session_state.debug = False

        if 'user_id_logged_in' not in st.session_state:
            st.session_state.user_id_logged_in = None
        elif (st.session_state.user_id_logged_in != None) & (st.session_state.current_page == 'add_code_page'):
            st.session_state.current_page = 'question_page'

        if 'index_questions_df' not in st.session_state:
            st.session_state.index_questions_df = 0
        if 'index_user_answer' not in st.session_state:
            st.session_state.index_user_answer = 0
        if 'keep_playing' not in st.session_state:
            st.session_state.keep_playing = True
        if 'game_code' not in st.session_state:
            st.session_state.game_code = None

        if 'multiple_choice_options_shuffle' not in st.session_state:
            num_list = [0, 1, 2, 3]
            random.shuffle(num_list)

            st.session_state.multiple_choice_options_shuffle = num_list  # First Time not Shuffle

        self.cmd_get_session_info = """
            SELECT * FROM PROD_DATASCIENCE_DB.PRJ_003_WHOWANTSTOBEAMILLIONAIRE.GAME_SESSION gs
            WHERE gs.SESSION_CODE = '{}'
        """

        self.centered_buttons_questions = """
                                        <style>
                                        .stButton {
                                            display: flex;
                                            justify-content: center;
                                            font-weight: bold;
                                        }
                                        .answer-container {
                                            display: flex;
                                            justify-content: space-between;
                                            width: 100%;
                                        }
                                        .answer-text {
                                            flex-grow: 1; /* Ensure answer text takes up remaining space */
                                            text-align: center; /* Align answer text to the left */
                                            margin-left: 10px;
                                        }
                                        </style>
                                        """

    def show_score_menu(self):
        # for i, value in enumerate(self.score_df.itertuples()):
        #     disable_button = False if i == st.session_state.index_questions_df else True
        #
        #     st.sidebar.button(
        #         f"${value}",
        #         disabled=disable_button
        #     )
        pass

    def reload_page(self):
        time.sleep(self.t)
        st.rerun()

    def next_page(self, name_page):
        # st.write(name_page)
        st.session_state.current_page = name_page
        self.reload_page()

    def add_code_page(self):
        st.header("JOIN TO GAME")
        st.session_state.game_code = st.text_input(
            "Insert Here Your Game Code!"
        )

        if st.button("JOIN", key="join_button"):
            try:
                # df = self.conn.query(self.cmd_get_session_info.format(st.session_state.game_code))
                df = exe_sf(create_conn(), sql=self.cmd_get_session_info.format(st.session_state.game_code))
                # st.write(df)
                if len(df) == 0:
                    st.error("This is not a Valid Session Code 😢")
                elif len(df) == 1:
                    status = None
                    for row in df.itertuples():
                        status = row.SESSION_STATUS
                        st.session_state.game_code = row.SESSION_CODE

                    if status == "lobby":
                        st.success("This is a Valid Session Code")

                        self.next_page("register_page")
                    elif status == 'finished':
                        st.error("This session game is over 🤷‍♂️")
                    else:
                        st.error("Sorry, this game already started 😶‍🌫️")
                else:
                    st.error("Unknown Error, we will fix soon... 🤥")
            except Exception as e:
                st.error(f"Error: {e}")

            # self.next_page("register_page")

    def get_other_option_selectbox(self, section, initial_options, other="Other"):
        initial_options.append(other)

        default_options = st.selectbox(
            section,
            initial_options
        )

        if default_options == other:
            new_option = st.text_input(f"Write here your {section}")
            st.session_state[f"user_{section.lower().replace(' ', '_')}"] = new_option
        else:
            st.session_state[f"user_{section.lower().replace(' ', '_')}"] = default_options

    def register_page(self):
        st.header("Register Here! 📃")
        # st.write(f"Now that you joined the game ({st.session_state.game_code}), you need to register:")

        register_values_free = ['First Name', 'Middle Name (Optional)', 'Last Name']
        register_values_options = {
            "Department": ["Option1", "Option2"],
            "Country": ["Ecuador", "Miami"]
        }

        for value in register_values_free:
            st.text_input(f"{value}", key=f"user_{value.lower().replace(' ', '_')}")

        for section, options in register_values_options.items():
            self.get_other_option_selectbox(section, options)

        if st.button("Lets Play! 🎮"):
            if st.session_state.user_first_name and st.session_state.user_last_name:
                user_id = generate_unique_id()
                SQL = f"""INSERT INTO PROD_DATASCIENCE_DB.PRJ_003_WHOWANTSTOBEAMILLIONAIRE.USERS_MAP
                                    (user_id, user_first_name, user_middle_name, user_last_name, user_department, user_country, group_game_session_id)
                                    VALUES
                                    (
                                    '{user_id}',
                                    '{st.session_state.user_first_name}', 
                                    '{st.session_state["user_middle_name_(optional)"]}', 
                                    '{st.session_state.user_last_name}', 
                                    '{st.session_state.user_department}', 
                                    '{st.session_state.user_country}', 
                                    '{st.session_state.game_code}'
                                    )
                                    """
                # st.write(SQL)
                try:
                    # self.conn.query(SQL, ttl=600)
                    # self.conn.query("INSERT INTO PROD_DATASCIENCE_DB.PRJ_003_WHOWANTSTOBEAMILLIONAIRE.USERS_MAP (user_first_name, user_middle_name, user_last_name, user_department, user_country, group_game_session_id) VALUES ( 'Mateo', '', 'Sosa', 'Option2', 'Ecuador', 'WR514R' )", ttl=600)
                    exe_sf(create_conn(),
                           sql=SQL, return_as_df=False)
                except Exception as e:
                    st.error(f"An unexpected error occurred: {e}")
                st.success("You Have Been Registered!")
                st.session_state.user_id_logged_in = user_id
                time.sleep(1.5)
                self.next_page("question_page")
            else:
                st.error("Please fill in all fields. The middle name is the only optional field!")

    def get_current_session_state(self):
        df = exe_sf(create_conn(), sql=self.cmd_get_session_info.format(st.session_state.game_code))
        try:
            return df["SESSION_STATUS"].iloc[0]
        except:
            return 'waiting'


    def question_page(self):
        # Center buttons
        # st.write("Im Hereeee")
        session_status = self.get_current_session_state()
        # st.write(session_status)
        if (session_status == 'playing') & (st.session_state.keep_playing == True):
            st.markdown(self.centered_buttons_questions, unsafe_allow_html=True)

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

            answers_list = [q["CORRECT_ANSWER"], q["INCORRECT_OPTION_1"], q["INCORRECT_OPTION_2"], q["INCORRECT_OPTION_3"]]
            answers = [answers_list[i] for i in st.session_state.multiple_choice_options_shuffle]
            answer_containers = [container_A, container_B, container_C, container_D]

            answer_text = ''

            for i in range(4):
                index_char = chr(65 + i)  # 0 = A, 1 = B, ...

                answer_containers[i].markdown(
                    f"""
                                <div class="answer-container">
                                    <span class="answer-text">{answers[i]}</span>
                                </div>
                                """,
                    unsafe_allow_html=True
                )

                # answer_containers[i].write(answers[i])
                if answer_containers[i].button(index_char):
                    st.session_state.index_user_answer = answers[i]
                    answer_text = f'Your answer is: {index_char}'

            if answer_text:
                st.success(answer_text)

            if st.button("Check"):
                if st.session_state.index_user_answer == q["CORRECT_ANSWER"]:
                    st.success("Well Done!")
                else:
                    st.error("Nice Try!")
                    st.session_state.keep_playing = False

                if st.session_state.keep_playing:
                    if st.session_state.index_questions_df < len(self.questions_df):
                        st.session_state.index_questions_df += 1
                        self.reload_page()
                    else:
                        st.toast("You Finished the questions!")
                        st.balloons()
                else:
                    self.next_page("lose_page")

            self.reload_page()
        else:
            self.next_page("waiting_page")

        # st.write(st.session_state.game_code)



        # st.write(st.session_state.current_page)

    def lose_page(self):
        st.header("You lose!")

    def waiting_page(self):
        session_status = self.get_current_session_state()
        # st.write(session_status)
        if (session_status == 'waiting') | (session_status == 'lobby'):
            st.markdown(
                """
                <h1 style='text-align: center;'>Waiting Room</h1>
                """,
                unsafe_allow_html=True)

            # self.show_score_menu()

            waiter_container = st.container(border=True)
            cols = waiter_container.columns(2)
            with cols[0]:
                waiting_status = waiter_container.status("Waiting")
                waiting_status.write("Waiting for Host")

            time.sleep(2.5)
            self.reload_page()
        elif (session_status == 'finished'):
            time.sleep(10)
            self.next_page('add_code_page')
        elif (session_status == 'playing'):
            self.next_page("question_page")


    def run(self):
        if st.session_state.debug:
            st.session_state.current_page = "question_page"

        if st.session_state.current_page == "add_code_page":
            self.add_code_page()
        elif st.session_state.current_page == "register_page":
            self.register_page()
        elif st.session_state.current_page == "question_page":
            self.question_page()
        elif st.session_state.current_page == "waiting_page":
            self.waiting_page()
        elif st.session_state.current_page == "lose_page":
            self.lose_page()


app = UserGUI()
app.run()
