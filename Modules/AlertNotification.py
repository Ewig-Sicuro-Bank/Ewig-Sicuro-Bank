import streamlit as st
import time
def RetrieveNotifications(username, c,conn):
    c.execute('SELECT notifications,status,time FROM notificationtable WHERE username = ?',(username,))
    notifications = c.fetchall()
    #st.write(notifications)
    if len(notifications)==0:
        st.success("No notifications yet . .")
    else:
        count=0
        for i in notifications:
            if i[1]=="Unread":
                cols = st.columns(2)
                cols[0].success(i[0])
                if cols[1].checkbox("Mark Message "+str(count+1)+" as Read"):
                    c.execute("UPDATE notificationtable SET status = ? WHERE time = ? AND username = ?",("Read",i[2],username))
                    conn.commit()
        
            else:
                cols = st.columns(3)
                cols[0].warning(i[0])
                if cols[1].checkbox("Mark Message "+str(count+1)+" as Unread"):
                   c.execute("UPDATE notificationtable SET status = ? WHERE time = ? AND username = ?",("Unread",i[2],username))
                   conn.commit()
                if cols[2].checkbox("Delete Message "+str(count+1)):
                   c.execute("DELETE FROM notificationtable WHERE username = ? AND time = ?",(username,i[2]))
                   conn.commit()
            count+=1

def InsertNotifications(username, c, notification, conn):
    if len(notification)==0:
        return
    #st.write(username[0],notification)
    c.execute('INSERT INTO notificationtable VALUES(?,?,?,?)',(username,notification,"Unread",str(time.time())))
    conn.commit()

def DeleteNotification(username,c,notification,conn):
    c.execute('DELETE FROM notificationtable WHERE username = ? AND notifications = ?',(username,notification))
    conn.commit()

 