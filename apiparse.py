import urllib
import json
import pprint
import requests
from urllib2 import urlopen
import simplejson
from googlemaps import GoogleMaps


#parse through APIs

brewerydb_auth = "079a83fb33046c975a4ff3475f1a4062"
beermapping_auth = "f7ce255aab176f13fb9ae1c5504094d3"
googlemaps_auth = "AIzaSyDELBXcYoUwiQQl-4us8UbG9hL7_iiMJug"
breweryURL = "http://api.brewerydb.com/v2/?key=079a83fb33046c975a4ff3475f1a4062"
beermappingURL = "http://beermapping.com/webservice/locquery/f7ce255aab176f13fb9ae1c5504094d3/"

#join 
def make_url(url, *args):
    lis = list(args)
    if len(lis) == 0:
        return url
    lis.insert(0, url)
    for key in range(len(lis)):
    	modified = str(lis[key])   
        lis[key] ="%s%s" % (modified.replace(' ', '+'), "/")
    return "".join(lis)[:-1]

#load json format
def load_json(URL):
	openURL = urllib.urlopen(URL)
	jsonURL = json.loads(openURL.read())
	return pprint.pprint(jsonURL)

#testing BreweryDB API connection
def test_brewerydb(URL):
	openURL = urllib.urlopen(URL)
	jsonURL = json.loads(openURL.read())
	return pprint.pprint(jsonURL)

#testing beermapping API connection
def test_beermapping():
	openURL = urllib.urlopen("http://beermapping.com/webservice/locquery/f7ce255aab176f13fb9ae1c5504094d3/")
	jsonURL = json.loads(openURL.read())
	return pprint.pprint(jsonURL)

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
