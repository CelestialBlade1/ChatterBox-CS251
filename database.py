"""This file contains the functions necessary to communicate with database.
"""

import psycopg2
#Generate the connection and the cursor instances of the object.
conn = psycopg2.connect(database="ChatDB", user="postgres", password="admin123", port=5432)
cur = conn.cursor()


def RegisterUser(username, hashed_password):
    """Function to add the entries of the new user to the database.
    :param username: Username of the new client
    :param hashed_password: Hashed Password of the new client.
    :returns: True or False depending on whether the entry already exists in the server or not.
    """
    cur.execute(f"""SELECT * FROM General
                WHERE phone_no = {username}""")
    ls = cur.fetchall()
    if len(ls)==0:
        cur.execute(f""" INSERT INTO General(phone_no, server_port, server_ip, hashed_pwd)
        VALUES({username},NULL,NULL,'{hashed_password}');""")
        conn.commit()
        return True
    else :
        return False

def Login(username, pwd):
    """Checks the username and the password of the logging user.
    :param username: Username of the logging user.
    :param password: Password of the logging user.

    :return: True if credentials match and False otherwise.
    """
    cur.execute(f"""SELECT * FROM General
                WHERE phone_no = {username} AND hashed_pwd = '{pwd}'""")
    ls = cur.fetchall()
    print(ls)
    if len(ls)!=0:
        return True
    else:
        return False


def userOnline(user, IP, PORT):
    """Marks the user as online"""
    cur.execute(f"""UPDATE General
                SET server_port={PORT}, server_ip='{IP}'
                WHERE phone_no={user};""")
    conn.commit()