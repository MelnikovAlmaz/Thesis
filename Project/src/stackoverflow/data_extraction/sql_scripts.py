"""
Created on Wed Aug  9 10:49:13 2017

@author: almaz
"""

CREATE_USER_TABLE = """
CREATE DATABASE User (
bronze integer,
silver integer,
gold integer,
view_count integer,
down_vote_count integer,
up_vote_count integer,
answer_count integer,
question_count integer,
account_id integer,
is_employee boolean,
last_modified_date date,
last_access_date date,
age integer,
reputation_change_year integer,
reputation_change_quarter integer,
reputation_change_month integer,
reputation_change_week integer,
reputation_change_day integer,
reputation integer,
creation_date date,
user_type character varying(255),
user_id integer PRIMARY KEY,
accept_rate integer      
);
"""

CREATE_TIMELINE_TABLE = """
create table timeline (
id serial primary key,
badge_id integer ,
post_id integer,
user_id integer,
timeline_type character varying(25),
post_type character varying(25),
creation_date date,
FOREIGN KEY (user_id) REFERENCES member (user_id));
"""

INSERT_USER = """
INSERT INTO member(
            bronze, silver, gold, view_count, down_vote_count, up_vote_count, 
            answer_count, question_count, account_id, is_employee, last_modified_date, 
            last_access_date, age, reputation_change_year, reputation_change_quarter, 
            reputation_change_month, reputation_change_week, reputation_change_day, 
            reputation, creation_date, user_type, user_id, accept_rate)
    VALUES (%, %, %, %, %, %, 
            %, %, %, %, %, 
            %, %, %, %, 
            %, %, %, 
            %, %, %, %, %);
"""