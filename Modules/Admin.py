import streamlit as st
import time
def AdminControl(c,conn):
	st.header("Admin Page")
	c.execute('SELECT * FROM userstable')
	admin_data = c.fetchall()
	c.execute('SELECT * FROM transactionstable')
	transaction_data = c.fetchall()
	#st.write(admin_data)
	opt2 = ["Review","Complaint"]
	st.header("Complaints & Reviews")
	opt3 = ["None"]
	c.execute('SELECT DISTINCT username FROM userstable') 
	usernames = c.fetchall()
	#st.write(usernames)
	for x in usernames:
		opt3.append(x[0])
	res2 = st.selectbox("Select a user",opt3)
	res3 = st.selectbox("Select the type of message",opt2)
	if res2!="None":
		user_complaints = RetrieveInfo(c,conn,res2,res3)
		for i in range(len(user_complaints)):
			st.info(str(i+1)+". "+user_complaints[i][1])
		#st.write(user_complaints)
	for i in range(len(admin_data)):
		transac = []
		for x in transaction_data:
			if x[0]==admin_data[i][0]:
				transac.append(x)
		st.write("")
		st.subheader("Account Details")
		st.write("Username : ",admin_data[i][0])
		st.write("Account No. : ",admin_data[i][2])
		st.write("Account Balance : ",admin_data[i][3])
		if admin_data[i][4]!=0:
			st.write("Loan Amount Pending : ",admin_data[i][4])
			st.write("Loan Time : ",admin_data[i][5]," Months")
		else:
			st.write("Loan Status : ",admin_data[i][6])
		st.write("")
		st.subheader("Transactions : \n\n")
		for x in transac:
			st.write("Transaction Amount : ",x[1])
			st.write("Transaction Type : ",x[2])
			st.write("Transaction Time : ",x[3])
			st.write("\n\n#-#-#-\n\n")
		
		st.write("\n*************\n")


def SendComplaint(complaint,username,type,c,conn):
    c.execute('INSERT INTO usercomplaints VALUES (?,?,?,?)',(username,complaint,type,str(time.time())))
    conn.commit()

def RetrieveInfo(c,conn,username,type_):
	c.execute('SELECT * FROM usercomplaints WHERE username = ? AND type = ?',(username,type_))
	complaint_data = c.fetchall()
	return complaint_data