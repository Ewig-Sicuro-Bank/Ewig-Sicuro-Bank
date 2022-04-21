import string
from turtle import position
import streamlit as st
import pandas as pd
import numpy as np


# Security
import hashlib
def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False
# DB Management
import sqlite3 
conn = sqlite3.connect('data.db')
c = conn.cursor()
# DB  Functions
def create_usertable():
	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT,accountno TEXT,balance INTEGER)')


def add_userdata(username,password):
	#generate 10 len account number with mix of numbers and letters
	acc_no= ''.join(np.random.choice(list(string.ascii_letters + string.digits),10))
	c.execute('INSERT INTO userstable(username,password,accountno,balance) VALUES (?,?,?,?)',(username,password,acc_no,0))
	conn.commit()

def login_user(username,password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data


def view_all_users():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data



def main():
	"""Erig Sicuro Bank"""

	#st.title("Erig Sicuro Bank")
	st.image("logo.png")
	menu = ["Home","Login","SignUp"]
	choice = st.sidebar.selectbox("Menu",menu)

	if choice == "Home":
		st.subheader("Home")
		if st.button("Profile"):
			st.write("In progress ... ")
	elif choice == "Login":
		st.subheader("Profile")

		username = st.sidebar.text_input("User Name")
		password = st.sidebar.text_input("Password",type='password')
		if st.sidebar.checkbox("Login or sign out"):
			# if password == '12345':
			create_usertable()
			hashed_pswd = make_hashes(password)

			result = login_user(username,check_hashes(password,hashed_pswd))
			if result:
				st.success("Logged In as {}".format(username))
				st.write("Account Number: {}".format(result[0][2]))
				st.write("Balance: {}".format(result[0][3]))
				# deposit and withdraw buttons
				st.sidebar.subheader("Transaction")
				if st.sidebar.checkbox("Deposit"):
					amount = st.sidebar.number_input("Amount",min_value=0)
					c.execute('UPDATE userstable SET balance = balance + ? WHERE username = ?',(amount,username))
					conn.commit()
					st.success("Deposited {}".format(amount))
					c.execute('SELECT * FROM userstable WHERE username = ?',(username,))
					data = c.fetchall()
					st.write("Balance: {}".format(data[0][3]))
				if st.sidebar.checkbox("Withdraw"):
					amount = st.sidebar.number_input("Amount",min_value=0)
					# check wether sufficient balance is there or not
					c.execute('SELECT * FROM userstable WHERE username = ?',(username,))
					data = c.fetchall()
					if data[0][3] >= amount:
						c.execute('UPDATE userstable SET balance = balance - ? WHERE username = ?',(amount,username))
						conn.commit()
						st.success("Withdraw {}".format(amount))
						c.execute('SELECT * FROM userstable WHERE username = ?',(username,))
						data = c.fetchall()
						st.write("Balance: {}".format(data[0][3]))
					else:
						st.warning("Insufficient Balance")
				# transfer money to other user
				if st.sidebar.checkbox("Transfer"):
					account_number = st.sidebar.text_input("Account Number")
					amount = st.sidebar.number_input("Amount",min_value=0)
					# check wether sufficient balance is there or not
					c.execute('SELECT * FROM userstable WHERE username = ?',(username,))
					data = c.fetchall()
					if data[0][3] >= amount:
						c.execute('UPDATE userstable SET balance = balance - ? WHERE username = ?',(amount,username))
						conn.commit()
						c.execute('UPDATE userstable SET balance = balance + ? WHERE accountno = ?',(amount,account_number))
						conn.commit()
						st.success("Transfered {} to {}".format(amount,account_number))
				#print updated balance
				
			else:
				st.warning("Incorrect Username/Password")


	elif choice == "SignUp":
			st.subheader("Create New Account")
			new_user = st.text_input("Create  Username")
			new_password = st.text_input("Enter Password",type='password')
			again_password = st.text_input("Re enter the password",type='password')
			
			if again_password == new_password:
				if st.button("Signup"):
					create_usertable()
					add_userdata(new_user,make_hashes(new_password))
					st.success("You have successfully created a valid Account")
					st.info("Go to Login Menu to login")
			else:
				st.warning("Passwords Don't match!")




if __name__ == '__main__':
	main()