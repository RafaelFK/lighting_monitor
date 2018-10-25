from django.http import HttpResponse
from django.core import serializers
from HTMLParser import HTMLParser
import json
import urllib2

reading = None
class SensorHTMLParser(HTMLParser):
    def handle_data(self, data):
        r = data.split()
        if len(r) > 0 and r[0] == 'Light:':
        	self.reading = r[1]
        	print r[1]

def node_address(node_id):
	print 'node_address'
	id = str(hex(int(node_id)))[2:]
	print 'id: {}'.format(id)
	return "http://[aaaa::212:74{:0>2}:{}:{}{:0>2}]/".format(*(id,) * 4)

def get_node_html_reading(node_id):
	print 'get_node_html_reading'
	res = urllib2.urlopen(node_address(node_id))
	return res.read()

def get_node_reading(node_id):
	print 'get_node_reading'
	parser = SensorHTMLParser()
	parser.feed(get_node_html_reading(node_id))
	return parser.reading

def sensors(request, node_id):
	print node_id
	read = get_node_reading(node_id)
	# read = 9
	return HttpResponse(json.dumps({node_id: read}), mimetype="application/json")