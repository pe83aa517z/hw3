from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect, url_for
import idDatabase


blueprint = Blueprint('ideal', __name__)

account  = ''
password = ''

@blueprint.route('/')
def login():
    global account 
    global password
    account  = ''
    password = ''
    return render_template('login.html')

@blueprint.route('/logout')
def logout():
    global account 
    global password
    account  = ''
    password = ''
    return redirect(url_for('.login'))
    #return render_template('logout.html')
'''
@blueprint.route('/recMessagePage')    
def recMessagePage():
    db = idDatabase.open_database()
    if not identity_verification(db):
        return redirect(url_for('.login'))
    idDatabase.myQuery('SELECT account,   FROM staff')
    
    
    return render_template('recMessage.html', list=)
'''




def isSignUp_and_check(db):
    account_local = request.form.get('account')
    password_local = request.form.get('password')
    name = request.form.get('name')
    
    if idDatabase.is_account_legitimate(db, account_local):
        print('The account is already in use')
        return False
    
    global account
    global password
    
    if name =='':
        return False
    
    if account_local == '' or account_local == None:
        return False
    else:
        account = account_local
    if password_local:
        password = password_local     
    return True

def update_data(db):
    if request.form.get('name') != None:
        name = request.form.get('name')
        sex = request.form.get('sex')
        age = request.form.get('age')
        pay = request.form.get('pay')
        introduction = request.form.get('introduction')
        if pay == '':
            pay = '0'
        if age == '':
            age = '0'
        if is_info_correct(pay, age, sex):
            age = int(age)
            pay = int(pay)
            if idDatabase.is_account_legitimate(db, account):
                idDatabase.update_by_account(db, account, password, name, sex, age, pay, introduction)
                db.commit()
            else:                
                idDatabase.add_manpower(db, account, password, name, sex, age, pay, introduction, 0)
                db.commit()
            return True
        return False
    return False

def isSupervisor(db):
    info = idDatabase.get_data_by_account(db, account)
    if info[0][6] > 0:
        return True
    return False

def getQuery(name, ageLow, ageHigh, payLow, payHigh):
    query = ' WHERE '
    args = []
    if name != '':
        args.append(name)
        query += 'name=? and '
    if ageLow != '' and ageLow.isdigit():
        args.append(ageLow)
        query += 'age>=? and '
    if ageHigh != '' and ageHigh.isdigit():
        args.append(ageHigh)
        query += 'age<=? and '
    if payLow != '' and payLow.isdigit():
        args.append(payLow)
        query += 'pay>=? and '
    if payHigh != '' and payHigh.isdigit():
        args.append(payHigh)
        query += 'pay<=? and '
    if query == ' WHERE ':
        return 'SELECT account, name, sex, age, pay, introduction, authority FROM staff', tuple(args)
    query = 'SELECT account, name, sex, age, pay, introduction, authority FROM staff' + query[:len(query)-4]
    return query, tuple(args)

def managementEdit():
    info = [None, None, None, None, None, None, None]
    data = request.form
    if len(data)>0:
        for key in data.keys():
            if key[:4] == 'info':
                temp1, index = key[4:].split('_')
                info[int(index)-1] = data[key]
     
        if info[0] != None:
            if is_info_correct(info[4], info[3], info[2], info[6]):
                db = idDatabase.open_database()
                strQuery='UPDATE staff SET name=?, sex=?, age=?, pay=?, introduction=?, authority=? WHERE account=?'
                temp = info.pop(0)
                info.append(temp)
                print(temp)
                idDatabase.myQuery(db, strQuery, info)
                db.commit()
                return True
    return False

def is_info_correct(pay, age, sex, authority='0'):
    if type(pay) == int or pay.isdigit():
        if type(age) == int or age.isdigit():
            if sex=='man' or sex=='woman' or sex=='':
                if type(authority) == int or authority.isdigit():
                    return True
    return False


@blueprint.route('/managementPage', methods=['GET', 'POST'])
def managementPage():
    db = idDatabase.open_database()
    if not identity_verification(db):
        return redirect(url_for('.login'))
    managementEdit()

    name = request.form.get('name')
    ageLow = request.form.get('ageLow')
    ageHigh = request.form.get('ageHigh')
    payLow = request.form.get('payLow')
    payHigh = request.form.get('payHigh')    
    if name != None:
        strQuery, args = getQuery(name, ageLow, ageHigh, payLow, payHigh)
        info = idDatabase.myQuery(db, strQuery, args)
        return render_template('managementPage.html', info=info, isShow=True)
        
    return render_template('managementPage.html')


def identity_verification(db):
    if account !='':
        if idDatabase.cmp_user(db, account, password):
            return True
    return False


@blueprint.route('/home', methods=['GET', 'POST'])
def home():
    db = idDatabase.open_database()
    if not identity_verification(db):
        if isSignUp_and_check(db):
            if not update_data(db):
                return redirect(url_for('.login'))
        else:
            return redirect(url_for('.login'))
    if request.form.get('name') != None:
        update_data(db)
        
    if isSupervisor(db):
        return redirect(url_for('.managementPage'))
    
    info = idDatabase.get_data_by_account(db, account)
    if info == []:
        return redirect(url_for('.login'))
    
    return render_template('home.html', info = info[0])

@blueprint.route('/home/edit')
def edit():
    print('edit account= ', account)
    db = idDatabase.open_database()
    if not identity_verification(db):
        return redirect(url_for('.login'))
    
    info = idDatabase.get_data_by_account(db, account)[0]
    return render_template('edit.html', info = info)

@blueprint.route('/logging', methods=['POST'])
def logging():   
    global account 
    global password
    if request.form.get('account'):
        account = request.form.get('account')
    if request.form.get('password'):
        password = request.form.get('password')

    db = idDatabase.open_database()
    if idDatabase.cmp_user(db, account, password):
        return redirect(url_for('.home'))
    print('fail')
    return redirect(url_for('.login'))

@blueprint.route('/signUp')
def signUp():
    return render_template('signUp.html')
