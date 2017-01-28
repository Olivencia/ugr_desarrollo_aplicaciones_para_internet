from django.shortcuts import render, HttpResponse
from random import randint
import base64, os, shelve, pymongo
from bson.objectid import ObjectId
from operator import is_not
from functools import partial
import re, json, ast
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from pymongo import MongoClient
import tweepy
from django import template
from django.shortcuts import render
from django.http import HttpResponseRedirect
from myweb.forms import addRestaurant, modifyRestaurant


client = MongoClient('localhost', 27017)

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

@csrf_exempt
def index(request):
	db = client['test']
	restaurants = db['restaurants']
	res_data = []
	restaurant = 0
	exists = False
	if(request.method == 'POST'):
		data = request.POST
		form = addRestaurant(request.POST)
		restaurant = {'name' : str(data['rname']), 'cuisine' : str(data['rcuisine']), 'borough' : str(data['rborough']), 'address' : { 'street' : str(data['rstreet']), 'coord' : [ str(data['rcoordy']), str(data['rcoordx']) ] } };
		r = restaurants.find_one({'name' : restaurant['name']})
		if(r):
			exists = True
		else:			
			restaurants.insert_one(restaurant);
		print restaurant
	else:
		form = addRestaurant()

	context = {
		'page' : 'restaurants',
		'restaurant' : restaurant,
		'form' : form,
		'exists' : exists,
	}

	return render(request,'template.html', context)

@csrf_exempt
def search(request):
	db = client['test']
	restaurants = db['restaurants']
	url = request.GET
	restaurant = restaurants.find_one({"name": re.compile(".*"+url['name']+".*", re.IGNORECASE)})
	if restaurant: 
		tweets = api.search(q=restaurant['name'], count=3)
		r_id = restaurant['_id']
	else: 
		tweets=0
		r_id = 0
	context = {
		'page' : "restaurants_search", 
		'restaurant' : restaurant,
		'tweets' : tweets,
		'r_id' : r_id
	}

	return render(request, 'template.html', context)

@login_required
@csrf_exempt
def edit(request):
	db = client['test']
	restaurants = db['restaurants']
	url = request.GET
	restaurant = restaurants.find_one({"_id": ObjectId(url['id'])})
	if(request.method == "POST"):
		data = request.POST
		form = modifyRestaurant(request.POST)
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
	else:
		form = modifyRestaurant(restaurant)


	context = {
		'page' : "restaurants_edit", 
		'restaurant' : restaurant,
		'form' : form,
	}
	return render(request, 'template.html', context)

@csrf_exempt
def test(request):
    return render(request,'template.html', {})
