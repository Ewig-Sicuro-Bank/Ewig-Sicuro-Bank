import string
from turtle import position
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
MONTH_TIME = 60*60*24*30
USD = 0.013
JPY = 1.673
EURO = 0.012

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
	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT,accountno TEXT,balance INTEGER,loanamount INTEGER,loantime INTEGER,loan_start INTEGER)')
	c.execute('CREATE TABLE IF NOT EXISTS exchangetable(username TEXT,USD TEXT, EURO TEXT, JPY TEXT)')

def add_userdata(username,password):
	#generate 10 len account number with mix of numbers and letters
	acc_no= ''.join(np.random.choice(list(string.ascii_letters + string.digits),10))
	c.execute('INSERT INTO userstable(username,password,accountno,balance,loanamount,loantime,loan_start) VALUES (?,?,?,?,?,?,?)',(username,password,acc_no,0,0,0,0))
	conn.commit()
	c.execute('INSERT INTO exchangetable VALUES(?,?,?,?)',(username,0,0,0))

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
				c.execute('SELECT * FROM userstable WHERE username = ?',(username,))
				data = c.fetchall()
				#if st.button("Account Details"):
				st.write("Account Number: {}".format(data[0][2]))
				#if st.button("Balance"):
				st.write("Balance: {}".format(data[0][3]))
				#if st.button("Loan Amount with intrest"):
				if data[0][4] != 0:
					st.write("Loan Amount with intrest: {}".format(data[0][4]))
					#if st.button("Loan Time "):
					st.write("Loan Time: {} Months".format(data[0][5]))
					#if st.button("Loan Status"):
					st.write("Loan Status: {}".format("Pending" if data[0][4]!=0 else "None"))
				#tt = datetime.now()
				#time_now = tt.second
				#st.write(result[0][4],result[0][5],result[0][6])
				#if result[0][4]!=0:
				#	 if result[0][6]+(result[0][5]*MONTH_TIME) < time_now:
				#	 	st.error("Warning! Loan not repayed within time limit!")
				# deposit and withdraw buttons
				st.sidebar.subheader("Transaction")
				if st.sidebar.checkbox("Deposit"):
					amount = st.sidebar.number_input("Amount",min_value=0)
					c.execute('UPDATE userstable SET balance = balance + ? WHERE username = ?',(amount,username))
					conn.commit()
					st.success("Deposited {}".format(amount))
					c.execute('SELECT * FROM userstable WHERE username = ?',(username,))
					data = c.fetchall()
					#st.write("Balance: {}".format(data[0][3]))
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
						#st.write("Balance: {}".format(data[0][3]))
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
				c.execute('SELECT * FROM userstable WHERE username = ?',(username,))
				data = c.fetchall()
				temp_pay = data[0][4]
				if st.sidebar.checkbox("Loan Request") and temp_pay==0:
					loan_time = st.sidebar.number_input("Loan Time (In months)",min_value=0)
					loan_amount = st.sidebar.number_input("Loan Amount",min_value=0)
					intrest_pay = round(loan_amount*(0.05)*(loan_time/12)) 
					a = datetime.now()
					current_time = a.second
					st.write(loan_amount,loan_time,current_time,intrest_pay)
					c.execute('UPDATE userstable SET loanamount = ?,loantime = ?,loan_start = ?, balance = balance + ? WHERE username = ?',(loan_amount+intrest_pay,int(loan_time),current_time,loan_amount,username))
					conn.commit()
					st.success("Loan Requested")
					result = data
				c.execute('SELECT * FROM userstable WHERE username = ?',(username,))
				data = c.fetchall()
				temp_pay = data[0][4]
				# pay loan
				if st.sidebar.checkbox("Pay Loan") and temp_pay!=0:
					loan_amount = st.sidebar.number_input("Loan Amount",min_value=0)
					c.execute('SELECT * FROM userstable WHERE username = ?',(username,))
					data = c.fetchall()
					pay_loan = data[0][4]
					if data[0][3] >= loan_amount:
						status = "None"
						if pay_loan-loan_amount==0: status="Paid"
						#else: status="Pending"
						c.execute('UPDATE userstable SET loanamount = ? WHERE username = ?',(pay_loan-loan_amount,username))
						conn.commit()
						c.execute('UPDATE userstable SET balance = balance - ? WHERE username = ?',(loan_amount,username))
						conn.commit()
						c.execute('SELECT * FROM userstable WHERE username = ?',(username,))
						data = c.fetchall()
						if data[0][4]==0:
							st.success("Loan Paid")
						#st.write("Loan Amount: {}".format(data[0][4]))
						#st.write("Loan Time: {} Months".format(data[0][5]))
						#st.write("Loan Status: {}".format(data[0][4]!=0))
					else:
						st.warning("Insufficient Balance")
				#print updated balance
				if st.sidebar.checkbox("Money Exchange"):
					st.sidebar.header("Currencies")
					if st.sidebar.button("INR->USD"):
						dollars = st.sidebar.number_input("Enter the amount of INR you want to convert to USD:")
						c.execute('UPDATE userstable SET balance = balance - ? WHERE username = ?', (dollars,username))
						c.execute('UPDATE exchangetable SET USD = USD + ? WHERE username = ?',(dollars*USD,username))
						conn.commit()
					if st.sidebar.button("INR->EUR"):
						euros = st.sidebar.number_input("Enter the amount of INR you want to convert to EURO:")
						c.execute('UPDATE userstable SET balance = balance - ? WHERE username = ?', (euros,username))
						c.execute('UPDATE exchangetable SET EURO = EURO + ? WHERE username = ?',(euros*EURO,username))
						conn.commit()
					if st.sidebar.button("INR->JPY"):
						yen = st.sidebar.number_input("Enter the amount of INR you want to convert to JPY:")
						c.execute('UPDATE userstable SET balance = balance - ? WHERE username = ?', (yen,username))
						c.execute('UPDATE exchangetable SET JPY = JPY + ? WHERE username = ?',(yen*JPY,username))
						conn.commit()
					
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

