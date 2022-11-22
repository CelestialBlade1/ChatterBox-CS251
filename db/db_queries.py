import psycopg2


conn = psycopg2.connect(dbname="chatterbox", user="chatterbox", password ="admin1234")
cur = conn.cursor()




def register_user(name, phone, age, password):
    try:
        cur.execute("insert into accounts values ({}, {}, {}, {})".format(name,phone, age, password))
        conn.commit()
        return True
    except:
        return False





def check_user_pass(phone, password):
    cur.execute("select * from accounts where phone = {} and password = {}".format(phone, password))
    b = cur.fetchone()
    if b == None:
        return False
    else:
        return True



def check_connection(phone):
    cur.execute("select serverid from userserver where phone={}".format(phone))
    output = cur.fetchall()

    if len(output) == 0:
        return "OFFLINE"
    else:
        return output[0]

register_user("Aman", 7977265537, 20, 'asdfghjkl')