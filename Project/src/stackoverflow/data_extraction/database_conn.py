"""
Created on Wed Aug  9 10:06:09 2017

@author: almaz
"""

import psycopg2
from Project.src.stackoverflow.data_extraction.sql_scripts import INSERT_USER


def get_connection():
    conn = psycopg2.connect(
        database="stackoverflow",
        user="almaz",
        host="/tmp/",
        password="Melnik23")
    cursor = conn.cursor()
    return cursor


def create_user(user):
    # Init User table
    connection = get_connection()
    query = INSERT_USER.format(
        user.bronze
    )
    connection.execute()
