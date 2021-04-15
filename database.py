import connection

connection.init_db()


def registerUser(first_name, last_name, id):
    conn = connection.get_connection()
    c = conn.cursor()
    c.execute(f'SELECT * FROM USERS WHERE user_id = {id};')
    user_check_data = c.fetchall()
    if len(user_check_data) <= 0:
        c.execute(
            f'INSERT INTO USERS (user_id, first_name, last_name, user_sum) VALUES ({id}, "{first_name}", "{last_name}", 0)')
        conn.commit()
        return True
    else:
        for row in user_check_data:
            print(row)
        return False


def addSum(sum, id):
    conn = connection.get_connection()
    c = conn.cursor()
    c.execute(f'UPDATE USERS SET user_sum={sum} WHERE user_id={id}')
    conn.commit()
    if c.rowcount > 0:
        return True
    else:
        return False


def showSum():
    conn = connection.get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM USERS ORDER BY user_sum DESC LIMIT 4')
    res = c.fetchall()
    array = []
    for row in res:
        array.append(row)
        print(row)
    return array










