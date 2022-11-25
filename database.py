import psycopg2

conn = psycopg2.connect(database="ChatDB", user="postgres", password="admin123", port=5432)
cur = conn.cursor()

def RegisterUser(username, hashed_password):
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