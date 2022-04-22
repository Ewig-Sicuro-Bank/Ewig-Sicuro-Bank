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
	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT,accountno TEXT,balance INTEGER,loanamount INTEGER,loantime TEXT,loanstatus TEXT)')


def add_userdata(username,password):
	#generate 10 len account number with mix of numbers and letters
	acc_no= ''.join(np.random.choice(list(string.ascii_letters + string.digits),10))
	c.execute('INSERT INTO userstable(username,password,accountno,balance,loanamount,loantime,loanstatus) VALUES (?,?,?,?,?,?,?)',(username,password,acc_no,0,0,"None","Not yet taken"))
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
				st.write("Loan Amount: {}".format(result[0][4]))
				st.write("Loan Time: {}".format(result[0][5]))
				st.write("Loan Status: {}".format(result[0][6]))
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
					else:
						st.warning("Insufficient Balance")
				# loan request
				if st.sidebar.checkbox("Loan Request"):
					loan_amount = st.sidebar.number_input("Loan Amount",min_value=0)
					loan_time = st.sidebar.text_input("Loan Time")
					c.execute('UPDATE userstable SET loanamount = ?,loantime = ?,loanstatus = ? WHERE username = ?',(loan_amount,loan_time,"Pending",username))
					conn.commit()
					st.success("Loan Requested")
					c.execute('SELECT * FROM userstable WHERE username = ?',(username,))
					data = c.fetchall()
					st.write("Loan Amount: {}".format(data[0][4]))
					st.write("Loan Time: {}".format(data[0][5]))
					st.write("Loan Status: {}".format(data[0][6]))
				
				# pay loan
				if st.sidebar.checkbox("Pay Loan"):
					loan_amount = st.sidebar.number_input("Loan Amount",min_value=0)
					c.execute('SELECT * FROM userstable WHERE username = ?',(username,))
					data = c.fetchall()
					pay_loan = data[0][4]
					if data[0][3] >= loan_amount:
						status = "None"
						if pay_loan-loan_amount==0: status="Paid"
						else: status="Pending"
						c.execute('UPDATE userstable SET loanamount = ?,loanstatus = ? WHERE username = ?',(pay_loan-loan_amount,status,username))
						conn.commit()
						st.success("Loan Paid")
						c.execute('UPDATE userstable SET balance = balance - ? WHERE username = ?',(loan_amount,username))
						conn.commit()
						c.execute('SELECT * FROM userstable WHERE username = ?',(username,))
						data = c.fetchall()
						st.write("Loan Amount: {}".format(data[0][4]))
						st.write("Loan Time: {}".format(data[0][5]))
						st.write("Loan Status: {}".format(data[0][6]))
					else:
						st.warning("Insufficient Balance")
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

