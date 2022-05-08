import streamlit as st
def RetrieveNotifications(username, c):
    c.execute('SELECT notifications FROM notificationtable WHERE username = ?',(username,))
    notifications = c.fetchall()
    #st.write(notifications)
    if len(notifications)==0:
        return ["No notifications yet . .",]
    else:
        return notifications

def InsertNotifications(username, c, notification, conn):
    if len(notification)==0:
        return
    c.execute('INSERT INTO notificationtable VALUES(?,?,?)',(username,notification,"Unread"))
    conn.commit()

def DeleteNotification(username,c,notification,conn):
    c.execute('DELETE FROM notificationtable WHERE username = ? AND notifications = ?',(username,notification))
    conn.commit()

 