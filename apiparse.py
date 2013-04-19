import urllib
import urllib2
import json
import pprint
import requests
from urllib2 import urlopen
import simplejson
from googlemaps import GoogleMaps
from brewerydb import *


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
#	jsonout = BreweryDb.beers()
	jsonout2 = BreweryDb.search({'type':'beer','q':'unibroue'})
	pprint.pprint(jsonout2)

#testing BreweryDB API connection
def test_brewerydb(*args):
	addition = add_terms(*args)
	url = "http://api.brewerydb.com/v2/" + addition + "?key=" + brewerydb_auth
	print url
	data = json.load(urllib2.urlopen(url))
	return pprint.pprint(data)

#testing beermapping API connection
def test_beermapping(typ, spec):
	type1 = str(typ)
	spec1 = str(spec)
	url = "http://beermapping.com/webservice/" + type1 + "/" + beermapping_auth + "/" + spec1
	print url
	data = json.load(urllib2.urlopen(url))
	return pprint.pprint(data)

#testing google maps API connection
def google_second():
	googleapi = 'http://maps.googleapis.com/maps/api/directions/json'
	origin = 'Bellflower,CA'
	destination = 'Austin,TX'
	url = '%s?origin=%s&destination=%s&sensor=false' % (googleapi, origin, destination)
	request = urlopen(url)
	results = simplejson.load(request)
	print results.keys()
	print results['status']
	for route in results['routes']:
		print route['summary']
		for leg in route['legs']:
		    print 'Start: %s @ %s' % (leg['start_address'], leg['start_location'])
		    print 'End: %s @ %s' % (leg['end_address'], leg['end_location'])
		    print 'Distance: %s and Duration: %s' % (leg['distance'], leg['duration'])
	for route in results['routes']:
	    for leg in route['legs']:
	        for step in leg['steps']:
	            print step['html_instructions'].decode('unicode-escape')
