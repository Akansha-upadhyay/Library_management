import mysql.connector
import streamlit as st
import pandas as pd


def get_connection():
    return mysql.connector.connect(
        host=st.secrets["mysql"]["host"],
        port=int(st.secrets["mysql"]["port"]),
        user=st.secrets["mysql"]["user"],
        password=st.secrets["mysql"]["password"],
        database=st.secrets["mysql"]["database"]
    )


def fetch_data(query, params=None):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(query, params or ())
        rows = cursor.fetchall()
        return pd.DataFrame(rows)
    finally:
        cursor.close()
        conn.close()


def execute_query(query, params=None):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(query, params or ())
        conn.commit()
        return True, "Operation completed successfully."

    except Exception as e:
        conn.rollback()
        return False, str(e)

    finally:
        cursor.close()
        conn.close()