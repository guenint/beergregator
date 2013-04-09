import urllib, json
import pprint
from googlemaps import GoogleMaps



#parse through breweryDB API

brewerydb_auth = "079a83fb33046c975a4ff3475f1a4062"
beermapping_auth = "f7ce255aab176f13fb9ae1c5504094d3"
googlemaps_auth = "AIzaSyDELBXcYoUwiQQl-4us8UbG9hL7_iiMJug"
breweryURL = "http://api.brewerydb.com/v2/"
beermappingURL = "http://beermapping.com/webservice/locquery/f7ce255aab176f13fb9ae1c5504094d3/"


def load_json(URL):
	openURL = urllib.urlopen(URL)
	jsonURL = json.loads(openURL.read())
	return pprint.pprint(jsonURL)


def google_maps_test():
	gmaps = GoogleMaps(googlemaps_auth)
	address = 'Constitution Ave NW & 10th St NW, Washington, DC'
	lat, lng = gmaps.address_to_latlng(address)
	return lat, lng