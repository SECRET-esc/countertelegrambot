import sqlite3

__connection = None


def get_connection():
    global __connection
    # check if connection was done if it not create connection
    if __connection is None:
        __connection = sqlite3.connect("db.db", check_same_thread=False)
    return __connection


def init_db(force: bool = False):
    # get connection
    conn = get_connection()
    # get cursor
    c = conn.cursor()

    # if force is true we trying to drop table
    if force:
        c.execute('DROP TABLE IF EXISTS USERS')
    # check if table not exists, if it true create table
    c.execute('''
            CREATE TABLE IF NOT EXISTS USERS 
                        (
                        id INTEGER PRIMARY KEY NOT NULL,
                        user_id INTEGER NOT NULL,
                        username TEXT,
                        user_sum INTEGER);
                        ''')
    # save changes
    conn.commit()


def add_test_user(username, number, id):
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        f'INSERT INTO USERS (user_id, username, user_sum) VALUES ({id}, "{username}", {number})')
    conn.commit()


def add_test_sum(sum, id):
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        f'UPDATE USERS SET user_sum={sum} WHERE user_id={id}')
    conn.commit()


def get_all_data():
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM USERS')
    res = c.fetchall()
    if len(res) <= 0:
        print("Empty")
    else:
        for row in res:
            print(row)


if __name__ == '__main__':
    init_db(True)
    # add_test_user('Georgy', 'Valeg', 0, 99);
    # add_test_sum(300, 300)
    # add_test_sum(200, 200)
    # add_test_sum(123213, 100)
    # add_test_sum(100, 123213)
    # add_test_sum(500, 99)
    get_all_data()
