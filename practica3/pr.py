from flask import Flask, request, render_template, session, redirect, url_for
from jinja2 import Environment, PackageLoader
from random import randint
import base64
import os
import shelve

app = Flask(__name__)
app.secret_key = os.urandom(24)
     
@app.route("/")
@app.route("/home")
def home():
	if not session:
		session['url1'] = 0
		session['url2'] = 0
	session['url3'] = session['url2']
	session['url2'] = session['url1']
	session['url1'] = "http://localhost"
	return render_template('template.html', page = "home", session = session)
	
@app.route("/blog")
def blog():
	if not session:
		session['url1'] = 0
		session['url2'] = 0
	session['url3'] = session['url2']
	session['url2'] = session['url1']
	session['url1'] = "http://localhost/blog"
	return render_template('template.html', page = "blog", session = session)

@app.route('/login', methods=['POST'])
def login():
	logged = False
	if(request.method == 'POST'):
		data = request.form
		if os.path.isfile('data.key'):
			f = open('data.key','r')
			line = f.read().split('\n')
			if(len(line) > 1):
				for i in range(0, len(line) - 1):
					key = line[i].split(':')[0]
					username = line[i].split(':')[1]
					if(username == data['uname']):
						db = shelve.open("data.db") 
						password = db[key]['password'] 
						if(password == data['psw']):
							session['username'] = data['uname']
							session['password'] = data['psw']
							session['name'] = db[key]['name']
							session['lastname'] = db[key]['lastname']
							session['address'] = db[key]['address']
							session['key'] = key

						db.close()
			f.close() 
	return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('password', None)
    session.pop('name', None)
    session.pop('lastname', None)
    session.pop('address', None)
    session.pop('url1', None)
    session.pop('url2', None)
    session.pop('url3', None)
    session.pop('key', None)
    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
	if not 'url1' in session:
		session['url1'] = 0
		session['url2'] = 0
	if not 'username' in session:
		session['url3'] = session['url2']
		session['url2'] = session['url1']
		session['url1'] = "http://localhost/register"
		if(request.method == 'GET'):	
			return render_template('template.html', page = "register", session = session)
		else:
			if(request.method == 'POST'):
				data = request.form
				exists = False
				f = 0
				key_ref = 1246803579
				if os.path.isfile('data.key'):
					f = open('data.key','r+')
				else:
					f = open('data.key', 'w+')
				line = f.read().split('\n')
				key = str(key_ref + len(line) - 1)
				if(len(line) > 1):
					for i in range(0, len(line) - 1):
						file_key = line[i].split(':')[0]
						username = line[i].split(':')[1]
						if(username == data['uname']):
							exists = True
				if(exists == False and (data['psw1'] == data['psw2'])):
					f.write(str(key) + ':' + data['uname'])
					f.write("\n") 
					db = shelve.open("data.db") 
					db[key] = {'username' : str(data['uname']).lower(), 'password' : str(data['psw1']), 'name' : str(data['name']), 'lastname' : str(data['lastname']), 'address' : str(data['address'])}
				f.close()
			return render_template('template.html', page = "home", session = session)
	else:
		return render_template('template.html', page = "profile_view", session = session)

@app.route('/profile/view', methods=['GET', 'POST'])
def profile_view():
	if not session:
		session['url1'] = 0
		session['url2'] = 0
	session['url3'] = session['url2']
	session['url2'] = session['url1']
	session['url1'] = "http://localhost/profile/view"
	if(request.method == 'POST'):	
		data = request.form
		key = session['key']
		if((data['psw1'] == data['psw2'])):
			db = shelve.open("data.db") 
			if(db[key]['password'] == data['psw1']):
				db[key] = {'username' : str(data['uname']).lower(), 'password' : str(session['password']), 'name' : str(data['name']), 'lastname' : str(data['lastname']), 'address' : str(data['address'])}
				if(data['uname'] != ''):
					session['username'] = data['uname']
				if(data['name'] != ''):
					session['name'] = db[key]['name']
				if(data['lastname'] != ''):
					session['lastname'] = db[key]['lastname']
				if(data['address'] != ''):
					session['address'] = db[key]['address']
				return render_template('template.html', page = "profile_view", session = session)
			else:
				return render_template('template.html', page = "profile_edit", session = session)
		else:
			return render_template('template.html', page = "profile_edit", session = session)
	else:
		return render_template('template.html', page = "profile_view", session = session)

@app.route('/profile/edit', methods=['GET', 'POST'])
def profile_edit():
	if not session:
		session['url1'] = 0
		session['url2'] = 0
	session['url3'] = session['url2']
	session['url2'] = session['url1']
	session['url1'] = "http://localhost/profile/edit"
	return render_template('template.html', page = "profile_edit", session = session)

@app.route('/profile/road', methods=['GET', 'POST'])
def road():
	return render_template('template.html', page = "road", session = session)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == "__main__":
	app.run(host='0.0.0.0', debug=True)
