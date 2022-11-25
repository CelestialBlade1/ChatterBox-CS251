import psycopg2

def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = ("""DROP TABLE General CASCADE""","""DROP TABLE GroupTable""",
        """
        CREATE TABLE General (
            phone_no BIGINT PRIMARY KEY,
            server_port BIGINT,
            server_ip VARCHAR(255),
            hashed_pwd VARCHAR(255) NOT NULL
        )
        """,
        """ CREATE TABLE GroupTable(
                phone_no BIGINT,
                group_id SERIAL
        )
        """
    )
    conn = None
    try:
        
        conn = psycopg2.connect(database="ChatDB", user="postgres", password="admin123", port=5432)
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    create_tables()