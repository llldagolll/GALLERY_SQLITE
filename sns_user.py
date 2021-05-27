# ログインなどユーザーに関する処理をまとめた
from flask import Flask, session, redirect, flash
from functools import wraps

from flask.templating import render_template
from photo_sqlite import select

# ユーザー名とパスワードの一覧 --- (*1)
# USER_LOGIN_LIST = {
#     'taro': 'aaa',
#     'jiro': 'bbb',
#     'sabu': 'ccc',
#     'siro': 'ddd',
#     'goro': 'eee' }

USER_LOGIN_LIST = select(
                    'SELECT user_id, password FROM users'
)



# ログインしているかの確認 --- (*2)
def is_login():
    return 'login' in session


# ログインを試行する --- (*3)
def try_login(form):
    user = form.get('user', '')
    password = form.get('pw', '')
    print('入力されたユーザid'+ user)
    print('入力されたpassword' + password)
    for i in range(len(USER_LOGIN_LIST)):
        print('ユーザリストのuserid' + USER_LOGIN_LIST[i]['user_id'])
        print('ユーザリストのpassword' +USER_LOGIN_LIST[i]['password'])
        if user != USER_LOGIN_LIST[i]['user_id'] and password != USER_LOGIN_LIST[i]['password']:
            print('存在しません。')

        elif user == USER_LOGIN_LIST[i]['user_id'] and password != USER_LOGIN_LIST[i]['password']:
            print('入力したパスワードが間違っています。')

        elif user != USER_LOGIN_LIST[i]['user_id'] and password == USER_LOGIN_LIST[i]['password']:
            print('入力したユーザidが間違っています。')
        else:
            session['login'] = user
            session['user_id'] = user
            return True




# ユーザー名を得る --- (*4)
def get_id():
    return session['login'] if is_login() else '未ログイン'

# 全ユーザーの情報を得る --- (*5)
def get_allusers():
    return [ u for u in USER_LOGIN_LIST ]












# # ログインを試行する --- (*3)
# def try_login(form):
#     user = form.get('user', '')
#     password = form.get('pw', '')
#     # パスワードチェック
#     if user not in USER_LOGIN_LIST: return False
#     if USER_LOGIN_LIST[user] != password:
#         return False
#     session['login'] = user
#     return True

# # ユーザー名を得る --- (*4)
# def get_id():
#     return session['login'] if is_login() else '未ログイン'

# # 全ユーザーの情報を得る --- (*5)
# def get_allusers():
#     return [ u for u in USER_LOGIN_LIST ]

# ログアウトする --- (*6)
def try_logout():
    session.pop('login', None)

# ログイン必須を処理するデコレーターを定義 --- (*7)
def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not is_login():
            return redirect('/login')
        return func(*args, **kwargs)
    return wrapper
