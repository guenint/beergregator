import urllib
import urllib2
import json
import pprint
import requests
from bs4 import BeautifulSoup
from urllib2 import urlopen
import simplejson
from collections import defaultdict
from googlemaps import GoogleMaps
from brewerydb import *
from collections import Counter
from geopy import geocoders  
import geopy
import geopy.distance


#parse through APIs

brewerydb_auth = "079a83fb33046c975a4ff3475f1a4062"
beermapping_auth = "f7ce255aab176f13fb9ae1c5504094d3"
googlemaps_auth = "AIzaSyDELBXcYoUwiQQl-4us8UbG9hL7_iiMJug"


#add terms to url test_brewerydb API connection
def add_terms(*args):
	lis = list(args)
	if len(lis) == 0:
		return ""
	for key in range(len(lis)):
		modified = str(lis[key])
		lis[key] = modified + "/"
	return "".join(lis)

def all_beers():
	jsonout = BreweryDb.beer("oeGSxs")
	BreweryDb.configure("079a83fb33046c975a4ff3475f1a4062")
	jsonout2 = BreweryDb.styles()
	jsonout3 = BreweryDb.breweries()
	pprint.pprint(jsonout3)

#testing BreweryDB API connection
def test_brewerydb(*args):
	addition = add_terms(*args)
	url = "http://api.brewerydb.com/v2/" + addition + "?key=" + brewerydb_auth
	print url
	data = json.load(urllib2.urlopen(url))
	return pprint.pprint(data)


def load_csv(fname):
    breweries = []
    fields = ["brewery","id","city","state","lat","long"]
    for line in open(fname, 'rU'):
        brewline = line.split('|')
        brew = {}
        for key, attribute in enumerate(brewline):
        	if fields[key] != "id":
        		attribute = attribute.strip()
        		brew[fields[key]] = attribute
        breweries.append(brew)
    return breweries


def match_db(fname):
	breweries = load_csv(fname)
	for brewery in breweries:
		name = brewery["brewery"]
		modified = name.strip().replace(' ', '+')
		url = "http://api.brewerydb.com/v2/search?key=" + brewerydb_auth + "&q=" + modified
		fileload = json.load(urllib2.urlopen(url))
		if len(fileload) > 2:
			data = fileload["data"][0]
			g = geocoders.GeoNames()
			code = g.geocode("" + brewery["city"] + ", " + brewery["state"], exactly_one = False)
			if len(code) > 1:
				place, (lat, lon) = code[0]
				print name + "|" + data["id"] + "|" + brewery["city"] + "|" + brewery["state"] + "|" + str(lat) + "|" + str(lon)
				brewery["id"] = data["id"]
			elif len(code) == 1:
				place, (lat, lon) = g.geocode("" + brewery["city"] + ", " + brewery["state"])
				print name + "|" + data["id"] + "|" + brewery["city"] + "|" + brewery["state"] + "|" + str(lat) + "|" + str(lon)
				brewery["id"] = data["id"]
		else:
			print name + "|" + "None" + "|" + brewery["city"] + "|" + brewery["state"]
			brewery["id"] = None
	return breweries


def output_types(brewid):
	stylerawlist = defaultdict(list)
	if check_brewery(brewid):
		url = "http://api.brewerydb.com/v2/brewery/" + brewid + "/beers/?key=" + brewerydb_auth
		fileload = json.load(urllib2.urlopen(url))
		if len(fileload) == 1:
			return None
		if len(fileload) > 2:
			allbeers = fileload["data"]
			for beer in allbeers:
				if "style" in beer.keys():
					stylerawlist[beer["style"]["name"]].append(beer["name"])
	return stylerawlist

def check_brewery(brewid):
	try:
		url = "http://api.brewerydb.com/v2/brewery/" + brewid + "/beers/?key=" + brewerydb_auth
		fileload = json.load(urllib2.urlopen(url))
	except urllib2.HTTPError:
		return False
	return True

def aggregate_types(brewlist):
	full = defaultdict(list)
	for brewery in brewlist:
		brews = output_types(brewery)
		for key, lis in brews.iteritems():
			for beer in lis:
				full[key].append(beer)
	return sorted(full.iteritems(), key=lambda value: len(value[1]), reverse = True)

def get_brews(lat, lon, radius):
	brewlist = []
	point1 = geopy.Point(lat, lon)
	for line in open("breweries.csv", 'rU'):
		brewline = line.split('|')
		point2 = geopy.Point(brewline[4], brewline[5])
		dist = geopy.distance.distance(point1, point2).km
		if dist < float(radius):
			brewlist.append(brewline[1])
	return aggregate_types(brewlist)

# def localize(fname="breweries.csv", city, state):
# 	breweries = load_csv(fname)
# 	for brewery in breweries:
# 		brewid = brewery["id"]
