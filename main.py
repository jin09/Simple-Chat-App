import hashlib
import hmac
import os
import random
import string
import json

import sys
from flask import Flask, render_template, request, redirect, make_response
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'blah!!fdgbsldf'
socketio = SocketIO(app)
msg_id = 1

try:
    with open('msg', 'r') as file:
        x = file.readline()
        # print x
        global msg_id
        msg_id = int(str(x))
except Exception, e:
    print e.message
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(exc_type, fname, exc_tb.tb_lineno, exc_tb.tb_frame.f_code.co_filename)
    with open('msg', 'w') as file:
        file.write('1')

# print msg_id


def increment_msg_id():
    try:
        global msg_id
        msg_id += 1
        with open('msg', 'w') as file:
            file.write(str(msg_id))
    except Exception, e:
        print e.message
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno, exc_tb.tb_frame.f_code.co_filename)
        global msg_id
        msg_id = 1
        with open('msg', 'w') as file:
            file.write('1')

######## Login Cookie pass hash handling #####################

SECRET = "lw45!y1dt9f0f*gyfg@xy$e56h2@ddfgh56udfgjdf32d#7s$t6h"


def make_salt():
    return ''.join(random.choice(string.letters) for x in xrange(5))


def make_user_cookie(user_id):
    return "%s|%s" % (str(user_id), str(hmac.new(SECRET, str(user_id)).hexdigest()))


def check_valid_cookie(test_cookie):
    if "|" not in test_cookie:
        return False
    user_val = test_cookie.split('|')[0]
    if make_user_cookie(user_val) == test_cookie:
        return True
    else:
        return False


###################################################################

@socketio.on('message')
def echoMessage(msg):
    try:
        global msg_id
        content = {}
        print('client to server: ' + msg)
        content['message'] = msg
        content['message_id'] = str(msg_id)
        increment_msg_id()
        send(json.dumps(content), broadcast=True)
    except Exception, e:
        print e.message
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno, exc_tb.tb_frame.f_code.co_filename)
        return False, str(e.message)


@socketio.on('like')
def like_mssg(msg):
    try:
        print('like: ' + str(msg))
        emit('like', msg, broadcast=True)
    except Exception, e:
        print e.message
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno, exc_tb.tb_frame.f_code.co_filename)
        return False, str(e.message)


@app.route('/login', methods=['POST', 'GET'])
def login():
    try:
        if request.method == 'GET':
            if 'name' in request.cookies:
                name_cookie = request.cookies['name']
                if check_valid_cookie(name_cookie):
                    return redirect('/app', code=302)
                else:
                    return render_template('login.html')
            else:
                return render_template('login.html')
        else:
            form = request.form
            if 'name' not in form:
                return render_template('login.html')
            name = form['name']
            # print name
            if name == '':
                return render_template('login.html')
            resp = make_response(redirect('/app', code=302))
            resp.set_cookie('name', str(make_user_cookie(name)))
            return resp
    except Exception, e:
        print e.message
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno, exc_tb.tb_frame.f_code.co_filename)
        return False, str(e.message)


@app.route('/app')
def main_chat_app():
    try:
        if 'name' in request.cookies:
            name_cookie = request.cookies['name']
            if check_valid_cookie(name_cookie):
                return render_template('chat.html')
            else:
                return redirect('/login', code=302)
        else:
            return redirect('/login', code=302)
    except Exception, e:
        print e.message
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno, exc_tb.tb_frame.f_code.co_filename)
        return False, str(e.message)


@app.route('/')
def root_page():
    try:
        if 'name' in request.cookies:
            name_cookie = request.cookies['name']
            if check_valid_cookie(name_cookie):
                return redirect('/app', code=302)
            else:
                return redirect('/login', code=302)
        else:
            return redirect('/login', code=302)
    except Exception, e:
        print e.message
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno, exc_tb.tb_frame.f_code.co_filename)
        return False, str(e.message)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
