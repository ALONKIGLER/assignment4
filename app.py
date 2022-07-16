import os
from flask import Flask, redirect, render_template
from flask import url_for
from flask import render_template
from datetime import timedelta
from flask import request, session, jsonify
import mysql.connector
import time
import asyncio
import requests
import aiohttp
import random


app = Flask(__name__)

app.secret_key = '123'
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=20)

@app.route('/')
def index_func():
    return render_template('home_page.html')


@app.route('/contact')
def contact_func():
    return render_template('contact.html')


@app.route('/about')
def about_page():
    user_info = {'name': 'Alon Kigler', 'number of product': '3', 'product name': 'kiteAlon'}
    session['CHECK'] = 'about'
    return render_template('about_page.html',
                           user_info=user_info)
# ------------------------------------------------------------------------#
user_dict = {
    'alon': '4444',
    'kigler': '1111',
    'erez': '1111',
    'avu': '1111',
    'haha': '1111'
}

@app.route('/log_in', methods=['GET', 'POST'])
def login_func():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in user_dict:
            pas_in_dict = user_dict[username]
            if pas_in_dict == password:
                session['username'] = username
                session['logedin'] = True
                return render_template('home_page.html',
                                       message='Success',
                                       username=username)
            else:
                return render_template('log_in.html',
                                       message='Wrong password!')
        else:
            return render_template('log_in.html',
                                   message='The user dose not exist')
    return render_template('log_in.html')


@app.route('/log_out')
def logout_func():
    session['logedin'] = False
    session.clear()
    return redirect(url_for('login_func'))


@app.route('/session')
def session_func():
    # print(session['CHECK'])
    return jsonify(dict(session))




users=[{'name': 'kiteAlon', 'size': 'xl', 'price': '1500$', 'img': '1.jpg'},
       {'name': 'kiteErez', 'size': ' l', 'price': '400$', 'img': '2.jpg'},
       {'name': 'kiteDron', 'size': ' xs', 'price': '500$', 'img': '3.jpg'},
       {'name': 'kiteAVI', 'size': ' m', 'price': '700$', 'img': '4.jpg'},
       {'name': 'kiteAlone', 'size': ' s', 'price': '900$', 'img': '1.jpg'} ]

picFolder = os.path.join('static', 'pics')
print(picFolder)
app.config['UPLOAD_FOLDER'] = picFolder


@app.route('/catalog')
def catalog_func():
    if 'user_name' in request.args:
        user_name = request.args['user_name']
        user = next((item for item in users if item['name'] == user_name), None)
        if request.args['user_name'] == "":
            return render_template('catalog_page.html',
                                   users=users)
        if user in users:
            return render_template('catalog_page.html',
                                   user_name=user_name,
                                   pic1_name=os.path.join(app.config['UPLOAD_FOLDER'], user['img']),
                                   user=user)
        else:
            return render_template('catalog_page.html', message='product not found, Please try again ')
    return render_template('catalog_page.html')

# ------------------------------------------------- #
# --------------- part A -------------------------- #
# ------------------------------------------------- #


def interact_db(query, query_type: str):
    return_value = False
    connection = mysql.connector.connect(host='localhost',
                                         user='root',
                                         passwd='root',
                                         database='schema_web')
    cursor = connection.cursor(named_tuple=True)
    cursor.execute(query)
    #

    if query_type == 'commit':
        connection.commit()
        return_value = True

    if query_type == 'fetch':
        query_result = cursor.fetchall()
        return_value = query_result

    connection.close()
    cursor.close()
    return return_value

@app.route('/users')
def users():
    query = 'select * from users'
    users_list = interact_db(query, query_type='fetch')
    my_var = session.get('message', None)
    return render_template('users.html', users=users_list, message=my_var)


@app.route('/insert_user', methods=['POST'])
def insert_user():
    id_name = request.form['id']
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    print(f'{name} {email} {password} {id_name} ')
    query = "INSERT INTO users(id, name, email, password) VALUES ('%s','%s', '%s', '%s')" % (id_name, name, email, password)
    interact_db(query=query, query_type='commit')
    session['message'] = 'the Insert request of User ' + id_name + ' Succeeded'
    return redirect(url_for('users'))


@app.route('/delete_user', methods=['POST'])
def delete_user_func():
    user_id = request.form['id']
    query = "DELETE FROM users WHERE id='%s';" % user_id
    # print(query)
    interact_db(query, query_type='commit')
    session['message'] = 'the Delete request of user, id: ' + user_id + ' Succeeded'
    return redirect(url_for('users'))



@app.route('/update_user', methods=['POST'])
def update_user_func():
    id = request.form['id']
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    query = "UPDATE users SET email ='%s' WHERE id='%s';" % (email, id)
    interact_db(query, query_type='commit')
    query = "UPDATE users SET name ='%s' WHERE id='%s';" % (name, id)
    interact_db(query, query_type='commit')
    query = "UPDATE users SET password ='%s' WHERE id='%s';" % (password, id)
    interact_db(query, query_type='commit')
    session['message'] = 'the update request of User id: ' + id + ' Succeeded'
    return redirect(url_for('users'))


# ------------------------------------------------- #
# ---------------assignment4 part b -------------------------- #
# ------------------------------------------------- #

@app.route('/assignment4_return_list')
def fetch_from_databace():
 query = 'select * from users'
 users_list = interact_db(query, query_type='fetch')
 users_list_to_save = []
 for user in users_list:
     user_dict = {}
     user_dict['id'] = user.id
     user_dict['name'] = user.name
     user_dict['email'] = user.email
     user_dict['password'] = user.password
     users_list_to_save.append(user_dict)
     print(users_list_to_save)

 response = jsonify(users_list_to_save)
 return response

# ------------------------------------------------- #
# ---------------assignment4 fetch_front-------------------------- #
# ------------------------------------------------- #


@app.route('/assignment4_fetch_fe')
def fetch_fe_func():
    return render_template('fetch.html')


# ----------------------------------------------------- #
# --------------- assignment4 fetch_back-------------------------- #
# ---------------------------------------------------- #


def get_users_sync(from_val):
    user = []
    res = requests.get(f'https://reqres.in/api/users/{from_val}')
    user.append(res.json())
    print(user)
    return user

def save_users_to_session(user_li):
    users_list_to_save = []
    for user in user_li:
        user_dict = {}
        # user_dict['sprites'] = {}
        user_dict['sprites'] = user['data']['avatar']
        user_dict['first_name'] = user['data']['first_name']
        user_dict['last_name'] = user['data']['last_name']
        user_dict['email'] = user['data']['email']
        users_list_to_save.append(user_dict)
    session['userr'] = users_list_to_save


@app.route('/assignment4_fetch_be')
def fetch_be_func():
    if 'type' in request.args:
        num = int(request.args['num'])
        session['num'] = num
        user = []

        if request.args['type'] == 'sync':
            user = get_users_sync(num)

        save_users_to_session(user)
        return render_template('fetch_back.html',
            userss=user)
    else:
        session.clear()
        return render_template('fetch_back.html')


# ------------------------------------------------- #
# ---------****------assignment4 PART C -------****---------- #
# ------------------------------------------------- #


@app.route('/assignment4_get_users', defaults={'user_id': -1})
@app.route('/assignment4_get_users/<user_id>')
def get_user(user_id):
    user_id = int(user_id)
    if user_id == -1:
        query = f'select * from users'
        users_list = interact_db(query, query_type='fetch')
        return_list = []
        for user in users_list:
            user_dict = {
                'name': user.name,
                'email': user.email,
                'create_date': user.create_date
            }
            return_list.append(user_dict)
        return jsonify(return_list)


    query = f'select * from users where id={user_id}'
    users_list = interact_db(query, query_type='fetch')

    if len(users_list) == 0:
        return_dict = {
            'message': 'user not found'
        }
    else:
        user_list = users_list[0]
        return_dict = {
            'name': user_list.name,
            'email': user_list.email,
            'create_date': user_list.create_date
        }
    return jsonify(return_dict)

if __name__ == '__main__':
    app.run(debug=True)
