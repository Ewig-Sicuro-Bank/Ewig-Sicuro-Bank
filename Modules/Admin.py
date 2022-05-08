import streamlit as st
def AdminControl(c,conn):
	st.header("Admin Page")
	c.execute('SELECT * FROM userstable')
	admin_data = c.fetchall()
	c.execute('SELECT * FROM transactionstable')
	transaction_data = c.fetchall()
	#st.write(admin_data)
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