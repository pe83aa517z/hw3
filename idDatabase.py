import sqlite3, os

def open_database(path='idDatabase.db'):
    isFind = os.path.exists(path)
    db = sqlite3.connect(path)
    if not isFind:
        cur = db.cursor()
        cur.execute('CREATE TABLE staff(id INTEGER KEY,'
                    ' account TEXT, password TEXT, name TEXT, sex TEXT, age INTEGER, pay INTEGER, introduction TEXT, authority INTEGER)')
        add_manpower(db, 'a123', '123', 'Benson', 'man'  , 22, 150, '', 1)
        add_manpower(db, 'b123', '123', 'Ada'   , 'woman', 18, 200, '', 0)
        add_manpower(db, 'c123', '123', 'Chasel', 'man'  , 17, 170, '', 0)
        db.commit()
    return db

def add_manpower(db, account, password, name, sex, age, pay, introduction, authority):
    db.cursor().execute('INSERT INTO staff (account, password, name, sex, age, pay, introduction, authority)'
                        ' VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (account, password, name, sex, age, pay, introduction, authority))
    
def get_data_by_account(db, account):
    c = db.cursor()
    c.execute('SELECT name, sex, age, pay, introduction, password, authority FROM staff WHERE account=?'
              'ORDER BY id', (account,))
    return c.fetchall()

def update_by_account(db, account, password, name, sex, age, pay, introduction):
    c = db.cursor()
    c.execute('UPDATE staff SET name=?, sex=?, age=?, pay=?, introduction=?, password=? WHERE account=?'
              , (name, sex, age, pay, introduction, password, account))

    return

def is_account_legitimate(db, account):
    c = db.cursor()
    c.execute('SELECT * FROM staff WHERE account=?', (account,))
    ans = c.fetchall()
    if ans == []:
        return False
    return True

def myQuery(db, query, args):
    c = db.cursor()
    c.execute(query, args)
    return c.fetchall()

def cmp_user(db, account, password):
    c = db.cursor()
    c.execute('SELECT * FROM staff WHERE account=? and password=?', (account, password))
    ans = c.fetchall()
    if len(ans) == 1:
        return True
    return False
    
if __name__ == '__main__':
    db = open_database()
    ans = get_data_by_account(db, 'b123')

    
    