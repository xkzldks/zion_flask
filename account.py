from flask import Flask, Blueprint, flash, url_for
from flask import render_template, request, redirect, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from model2 import db
from uuid import getnode
import socket
import re
import chulseck

app = Flask(__name__)
app.secret_key = '123'

blue_account = Blueprint("account", __name__, url_prefix="/account")

@blue_account.route("/register", methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        check_code = request.form['check_password']
        admin_code = "zion0235" # register code(admin)
        guest_code = "9uest" # register code(guest)
        if check_code == admin_code or check_code == guest_code:
            # 아이디 중복 확인
            check_user = list(db.user.find({"username": username}))
            # 중복된 아이디가 없다면
            if not check_user:
                if check_code == guest_code:
                    user = {
                        "username": username,
                        "password": generate_password_hash(password),
                        "auth": 2
                    }
                else:
                    user = {
                        "username": username,
                        "password": generate_password_hash(password),
                        "auth": 1
                    }
                db.user.insert_one(user)
                flash('가입을 축하합니다!')   
                return render_template("login.html")
            else:
                print("존재")
                flash("이미 존재하는 아이디입니다.")
        else:
            flash("가입코드가 일치하지 않습니다.")
        
    return render_template("register.html")


@blue_account.route("/login", methods=('GET', 'POST'))
def login():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		check_user = db.user.find_one({"username": username})
		
		if check_user:
			if check_password_hash(check_user.get("password"), password):
				#s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
				#s.connect(("34.64.56.232",5000))
				#ip = s.getsockname()[0]
				#mac = ':'.join(re.findall('..','%012x'%getnode()))
				#print(username+"님 환영합니다.\n접근 ip : " + ip + "\nMAC : " + mac)
				client_ip = request.remote_addr
				client_mac = chulseck.mac_for_ip(client_ip)
				flash(username+"님 환영합니다. 접근 ip : " + client_ip)
				session['username'] = username
				s.close()
				return redirect("/")
			else:
				flash("아이디 또는 비밀번호를 확인해주세요.")
		else:
			flash("아이디 또는 비밀번호를 확인해주세요.")
	return render_template("login.html")


@blue_account.route("/logout")
def logout():
    if session.get('username'): 
        session.pop('username', None)
        flash('로그아웃이 완료되었습니다')
        return redirect('/')
