import os
from yelpapi import YelpAPI
import requests

from functools import wraps 
from flask import Flask, redirect, render_template, request, session, url_for

MY_API_KEY = os.getenv("YELP_API_KEY"); 
yelp_api = YelpAPI(MY_API_KEY)

def login_required(f):
    #https://flask.palletsprojects.com/en/2.1.x/patterns/viewdecorators/
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session["username"] is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def find(location, categories, price_range):

    #Contact API endpoint. 
    try: 
        response = yelp_api.search_query(term="restaurants", location=location, categories=categories, price=price_range, sort_by='best_match', limit=4)
    except requests.RequestException:
        return None
    
    #Parse the data.
    try:
        results = response["businesses"]
        parsed = []
        for result in results:
            business = {}
            business["name"] = result["name"]
            business["rating"] = result["rating"]
            business["categories"] = result["categories"][0]["title"]
            business["price"] = result["price"]
            business["image"] = result["image_url"]
            address = result["location"]['display_address']
            business["location"] = ", ".join(address)
            business["website"] = result["url"]
            parsed.append(business)
        return parsed 
    except:
        return None
    