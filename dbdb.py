import sqlite3

def dbcon():
    return sqlite3.connect('mydb.db')

def create_table():
    try:
        query = '''
            CREATE TABLE "users" (
                "email" char(20),
                "password" char(10),
                "name" char(5),
                PRIMARY KEY("email")
            )
        '''
        db = dbcon()
        c = db.cursor()
        c.execute(query)
        db.commit()
    except Exception as e:
        print('db error:', e)
    finally:
        db.close()

def insert_user(email, password, name):
    try:
        db = dbcon()
        c = db.cursor()
        setdata = (email, password, name)
        c.execute("INSERT INTO users VALUES (?, ?, ?)", setdata)
        db.commit()
    except Exception as e:
        print('db error:', e)
    finally:
        db.close()

def select_user(email, pw):
    ret = ()
    try:
        db = dbcon()
        c = db.cursor()
        setdata = (email, pw)
        c.execute('SELECT * FROM users WHERE email = ? AND password = ?', setdata)
        ret = c.fetchone()
    except Exception as e:
        print('db error:', e)
    finally:
        db.close()
    return ret

def check_email(email):
    ret = ()
    try:
        db = dbcon()
        c = db.cursor()
        setdata = (email,)
        c.execute('SELECT * FROM users WHERE email = ?', setdata)
        ret = c.fetchone()
    except Exception as e:
        print('check_email db error:', e)
    finally:
        db.close()
    return ret

def select_all():
    ret = list()
    try:
        db = dbcon()
        c = db.cursor()
        c.execute('SELECT * FROM users')
        ret = c.fetchall()
    except Exception as e:
        print('db error:', e)
    finally:
        db.close()
    return ret

# insert_user('bb', '1234', 'aa')
print(select_all())