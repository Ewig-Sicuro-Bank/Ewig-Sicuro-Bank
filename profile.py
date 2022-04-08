import streamlit as st
import pandas as pd

#Database Management
import sqlite3 as sq
conn = sq.connect('data.db')
c = conn.cursor()

def create_profiletable():
    c.execute('CREATE TABLE IF NOT EXISTS profiletable(first_name TEXT, last_name TEXT, gender TEXT, account_no BLOB, username TEXT)')

def add_profiledata(first_name, last_name, gender, username):
    