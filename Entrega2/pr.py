from flask import Flask, request, render_template, session, redirect, url_for
from jinja2 import Environment, PackageLoader
from random import randint
import base64, os, shelve, pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
from operator import is_not
from functools import partial
import re, json, ast, sax_parser, tweepy

client = MongoClient('localhost', 27017)

app = Flask(__name__)
app.secret_key = os.urandom(24)

#Twitter API tokens
consumer_key = 'YOUR KEY HERE'
consumer_secret = 'YOUR KEY HERE'
access_token = 'YOUR TOKEN HERE'
access_token_secret = 'YOUR SECRET TOKEN HERE'

# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Creation of the actual interface, using authentication
api = tweepy.API(auth)
     
# Home page     
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
	
# Blog page     
@app.route("/blog")
def blog():
	if not session:
		session['url1'] = 0
		session['url2'] = 0
	session['url3'] = session['url2']
	session['url2'] = session['url1']
	session['url1'] = "http://localhost/blog"
	return render_template('template.html', page = "blog", session = session)

# Login user     
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

# Logout user     
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

# Register user     
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

# Profile user data page     
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

# Edit user data profile page     
@app.route('/profile/edit', methods=['GET', 'POST'])
def profile_edit():
	if not session:
		session['url1'] = 0
		session['url2'] = 0
	session['url3'] = session['url2']
	session['url2'] = session['url1']
	session['url1'] = "http://localhost/profile/edit"
	return render_template('template.html', page = "profile_edit", session = session)

# URL profile road page    
@app.route('/profile/road', methods=['GET', 'POST'])
def road():
	return render_template('template.html', page = "road", session = session)

# Search and add restaurants page     
@app.route('/restaurants', methods=['GET', 'POST'])
def restaurants():
	db = client['test']
	restaurants = db['restaurants']
	res_data = []
	restaurant = 0
	if(request.method == 'POST'):
		data = request.form
		restaurant = {'name' : str(data['rname']), 'cuisine' : str(data['rcuisine']), 'borough' : str(data['rborough']), 'address' : { 'street' : str(data['rstreet']), 'coord' : [ str(data['rcoordy']), str(data['rcoordx']) ] } };
		restaurants.insert_one(restaurant);
	return render_template('template.html', page = "restaurants", session = session, restaurant = restaurant, restaurants = res_data)

# All restaurants page     
@app.route('/restaurants/all', methods=['GET', 'POST'])
def restaurants_all():
	db = client['test']
	restaurants = db['restaurants']
	res_data = []
	if(request.method == 'GET'):
		if not 'start' in request.args or not 'end' in request.args:
			start = 0
			end = 10
		else:
			start = int(request.args['start'])
			end = int(request.args['end'])
		all_restaurants = restaurants.find({})
		restaurant = 0
		cnt = 0
	 	for res in all_restaurants:
	 		json_tmp = {}
			if ('address' in res) and ('coord' in res['address']) and res['address']['coord']:
			 	json_tmp['name'] = (res['name']).replace("'","")
			 	json_tmp['name'] = (json_tmp['name']).replace('"','')
			 	json_tmp['name'] = (json_tmp['name']).replace('\x1a','')
				json_tmp['cuisine'] = res['cuisine']
				json_tmp['cuisine'] = (json_tmp['cuisine']).replace('"','')
			 	json_tmp['cuisine'] = (json_tmp['cuisine']).replace('\x1a','')
				json_tmp['borough'] = res['borough']
				json_tmp['borough'] = (json_tmp['borough']).replace('"','')
			 	json_tmp['borough'] = (json_tmp['borough']).replace('\x1a','')
				json_tmp['street'] = (res['address']['street']).replace("'","")
				json_tmp['street'] = (json_tmp['street']).replace('"','')
				json_tmp['street'] = (json_tmp['street']).replace('\x1a','')
				json_tmp['coordx'] = (res['address']['coord'])[1]
				json_tmp['coordy'] = (res['address']['coord'])[0]
				res_data.append(json_tmp)
		page = (end/10-randint(1,14))
		while page < 0:
 			page = (end/10-randint(1,14))
	return render_template('template.html', page = "restaurants_all", session = session, restaurant = restaurant, restaurants = res_data, start = start, end = end, value = page)

# Search restaurant page  
@app.route('/restaurants/search', methods=['GET', 'POST'])
def restaurants_search():
	db = client['test']
	restaurants = db['restaurants']
	url = request.args
	restaurant = restaurants.find_one({"name": re.compile(".*"+url['name']+".*", re.IGNORECASE)})
	if restaurant: tweets = api.search(q=restaurant['name'], count=3)
	else: tweets=0
	if restaurant and ('address' in restaurant) and ('coord' in restaurant['address']) and restaurant['address']['coord']:
		print restaurant['address']['coord']
	return render_template('template.html', page = "restaurants_search", session = session, restaurant = restaurant, tweets = tweets)

# Edit existing restaurant page  
@app.route('/restaurants/edit', methods=['GET', 'POST'])
def restaurants_edit():
		db = client['test']
		restaurants = db['restaurants']
		url = request.args
		restaurant = restaurants.find_one({"_id": ObjectId(url['id'])})
		if(request.method == "POST"):
			data = request.form
			if data['rname']:
				restaurant['name'] = data['rname']
			if data['rcuisine']:
				restaurant['cuisine'] = data['rcuisine']
			if data['rborough']:
				restaurant['borough'] = data['rborough']
			if data['rstreet']:
				restaurant['address']['street'] = data['rstreet']
			if data['rcoordy'] and data['rcoordx']:
				restaurant['address']['coord'] = []
				restaurant['address']['coord'].append(data['rcoordy'])
				restaurant['address']['coord'].append(data['rcoordx'])

			restaurants.save(restaurant);
		print restaurant
		return render_template('template.html', page = "restaurants_edit", session = session, restaurant = restaurant)

# See restaurants in world map page  
@app.route('/restaurants/maps', methods=['GET', 'POST'])
def maps():
	db = client['test']
	restaurants = db['restaurants']
 	res_data = []
	all_restaurants = restaurants.find()
 	for restaurant in all_restaurants:
 		json_tmp = {}
		if ('address' in restaurant) and ('coord' in restaurant['address']) and restaurant['address']['coord']:
		 	json_tmp['name'] = (restaurant['name']).replace("'","")
		 	json_tmp['name'] = (json_tmp['name']).replace('"','')
		 	json_tmp['name'] = (json_tmp['name']).replace('\x1a','')
			json_tmp['coordx'] = restaurant['address']['coord'][1]
			json_tmp['coordy'] = restaurant['address']['coord'][0]
			res_data.append(json_tmp)
	return render_template('template.html', page = "maps", session = session, res_data = res_data, elements = len(res_data))

# See some statistics of restaurants page   
@app.route('/restaurants/statistics', methods=['GET', 'POST'])
def restaurants_statistics():
	db = client['test']
	restaurants = db['restaurants']
	
	#Cuisine treemap
	tmp = restaurants.distinct('cuisine')
	tmp = encodeAndCopy(tmp)

	cuisine = [None]*len(tmp)
	for i in range(0,len(tmp)):
		json_tmp = {}
		json_tmp['name'] = tmp[i]
		json_tmp['value'] = restaurants.find({"cuisine" : tmp[i]}).count()
		json_tmp['colorValue'] = i
		cuisine[i] = json_tmp

	#Borough circle
	tmp = restaurants.distinct('borough')
	tmp = encodeAndCopy(tmp)

	borough = [None]*(len(tmp)+1)
	elements = restaurants.count()
	cnt = 0
	global_y = 0.0
	for i in range(0,len(tmp)):
		json_tmp = {}
		tmp_y = float(restaurants.find({"borough" : tmp[i]}).count()*100/elements)
		if(tmp_y > 2):
			json_tmp['y'] = tmp_y
			json_tmp['name'] = tmp[i]
			if(tmp_y > 30): json_tmp['sliced'] = 'true'
			borough[cnt] = json_tmp
			cnt = cnt + 1
		else:
			global_y = global_y + tmp_y

	json_tmp = {}
	json_tmp['y'] = global_y
	json_tmp['name'] = 'Others'
	borough[cnt] = json_tmp
	borough = borough[0:cnt+1]

	return render_template('template.html', page = "restaurants_statistics", session = session, cuisine = cuisine, borough = borough)


# Search articles of RSS data file page   
@app.route('/rss', methods=['GET', 'POST'])
def rss():
	if(request.method == 'POST'):
		data = request.form
		list_data = sax_parser.generateRSSData(data['string_data'])
		rss_data = ''
		for element in list_data:
			rss_data += element
	elif(request.method == 'GET'):
		rss_data = 0
	return render_template('template.html', page = "rss", session = session, method = request.method, rss_data = rss_data)


# Not found page   
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

def encodeAndCopy(data):
	res = [None]*len(data)
	for i in range(0,len(data)):
		res[i] = data[i].encode('ascii', errors='replace')
	return res

if __name__ == "__main__":
	app.run(host='0.0.0.0', debug=True)
