from datetime import datetime
import streamlit as st
import time
from dateutil.relativedelta import relativedelta
import Modules.AlertNotification as alerts
def DepositTransaction(username,amount,c,conn,opt7):
							if opt7=="Checking":
								c.execute('UPDATE checkingacctable SET balance = balance + ? WHERE username = ?',(amount,username))
								conn.commit()
								return

							c.execute('SELECT * FROM userstable WHERE username = ?',(username,))
							data = c.fetchall()
							if amount>0:
								c.execute('UPDATE userstable SET balance = balance + ? WHERE username = ?',(amount,username))
								conn.commit()
								st.success("Deposited {}".format(amount))
								c.execute('INSERT INTO transactionstable VALUES(?,?,?,?)',(username,amount,"CREDIT",str(time.ctime())))
								conn.commit()
								c.execute('SELECT * FROM userstable WHERE username = ?',(username,))
								data = c.fetchall()
								alerts.InsertNotifications(username,c,"Amount of "+str(amount)+" Has been credited to your account.",conn)
							#st.write("Balance: {}".format(data[0][3]))

def WithdrawTransaction(username,amount,c,conn,opt7):
							st.write(datetime.date(datetime.today()))
							if opt7=="Checking":
								c.execute('SELECT * FROM checkingacctable WHERE username = ?',(username,))
								data8 = c.fetchall()
								if data8[0][2] < amount:
									st.sidebar.warning("Insufficient Balance")
									return
								else:
									c.execute('UPDATE checkingacctable SET balance = balance - ? WHERE username = ?',(amount,username))
									conn.commit()
									c.execute('UPDATE checkingacctable SET last_payment = ? WHERE username = ?',(str(amount),username))
									conn.commit()
									date_after_month = datetime.date(datetime.today()+ relativedelta(months=1))
									c.execute('UPDATE checkingacctable SET duedate = ? WHERE username = ?',(date_after_month,username))
									conn.commit()
									return
							c.execute('SELECT * FROM userstable WHERE username = ?',(username,))
							data = c.fetchall()
							if data[0][3] >= amount:
								if amount > 0:
									c.execute('UPDATE userstable SET balance = balance - ? WHERE username = ?',(amount,username))
									conn.commit()
									alerts.InsertNotifications(username,c,"Amount of "+str(amount)+" Has been debited from your account.",conn)
									c.execute('INSERT INTO transactionstable VALUES(?,?,?,?)',(username,amount,"DEBIT",str(time.ctime())))
									conn.commit()
									st.success("Withdraw {}".format(amount))
									c.execute('SELECT * FROM userstable WHERE username = ?',(username,))
									data = c.fetchall()
								st.write("Balance: {}".format(data[0][3]))
							else:
								st.warning("Insufficient Balance")

def MoneyTransfer(username,account_number,amount,c,conn):
							c.execute('SELECT * FROM userstable WHERE username = ?',(username,))
							data = c.fetchall()
							if st.button("Pay Now"):
								if data[0][3] >= amount and amount > 0:
									c.execute('UPDATE userstable SET balance = balance - ? WHERE username = ?',(amount,username))
									conn.commit()
									c.execute('INSERT INTO transactionstable VALUES(?,?,?,?)',(username,amount,"DEBIT",str(time.ctime())))
									conn.commit()
									c.execute('UPDATE userstable SET balance = balance + ? WHERE accountno = ?',(amount,account_number))
									conn.commit()
									c.execute('SELECT username FROM userstable WHERE accountno = ?',(account_number,))
									second_username = c.fetchall()
									if len(second_username)>0:
										c.execute('INSERT INTO transactionstable VALUES(?,?,?,?)',(username,amount,"DEBIT",str(time.ctime())))
										conn.commit()
										alerts.InsertNotifications(second_username[0][0],c,"Amount of "+str(amount)+" Has been credited to your account.",conn)
										alerts.InsertNotifications(username,c,"Amount of "+str(amount)+" Has been debited from your account.",conn)
										st.success("Transfered {} to {}".format(amount,account_number))
									else:
										st.warning("Transaction Error . . ")
								else:
									st.warning("Transaction Error . . ")