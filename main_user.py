import snowflake.connector
import streamlit as st
import pandas as pd


def making_snowflake_conn():
    # Establish connection to Snowflake
    conn2 = snowflake.connector.connect(
        user=user_sf,
        password=password_sf,
        role=role_sf,
        account=account_sf,
        warehouse=warehouse_sf,
        database=database_sf,
        schema=schema_sf
    )
    return conn2


def exe_sf(sql: str, return_as_df=True):
    try:
        conn = making_snowflake_conn()
        cursor = conn.cursor()
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
        conn.close()


user_sf = st.secrets["snowflake"]["user"]
password_sf = st.secrets["snowflake"]["password"]
role_sf = st.secrets["snowflake"]["role"]
account_sf = st.secrets["snowflake"]["account"]
warehouse_sf = st.secrets["snowflake"]["warehouse"]
database_sf = st.secrets["snowflake"]["database"]
schema_sf = st.secrets["snowflake"]["schema"]

# Now you can use these variables in your app
st.write("user_sf Key:", user_sf)
st.write("password_sf:", password_sf)

st.write(exe_sf("SELECT * FROM PROD_DATASCIENCE_DB.PRJ_003_WHOWANTSTOBEAMILLIONAIRE.QUESTIONS"))
