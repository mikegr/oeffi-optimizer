import logging
import inspect
from pprint import pprint
from django.utils import simplejson
from datetime import datetime
from google.appengine.api import users
from google.appengine.ext import blobstore
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext.webapp.util import run_wsgi_app

class Location(db.Model):
	name = db.TextProperty() 

class Exit(db.Model):
	location = db.IntegerProperty() 
	name = db.TextProperty() 
	hint = db.TextProperty() 

class LocationHandler(webapp.RequestHandler):
	
	def get(self):
		self.response.headers['Content-Type'] = 'application/json'
		locations = db.GqlQuery("SELECT * FROM Location");
		
		list = []
		for loc in locations:
			obj = {"key": str(loc.key()), "id": str(loc.key().id()), "name": loc.name}
			if loc.parent() is not None:
				obj['parent'] = loc.parent().key().id()
			
			list.append(obj)
		response = simplejson.dumps(list)
		self.response.out.write(response)
	

	def post(self):
		logging.info("POST")		
		val = self.request.body
		logging.info("BODY:" + val)		
		obj = simplejson.loads(val);
		logging.info("OBJECT:" + str(obj))	
				
		location = Location(name = obj['name'])
		
		if 'parent' in obj:
			parent = obj['parent']
			location.parent = db.Key.from_path('Location', parent)
		
		location.put();
		
		self.response.out.write(str(location.key().id()));
	
class ExitHandler(webapp.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'application/json'
		locParam = self.request.get("location");
		logging.info("param: " + locParam)
		locationKey = db.Key.from_path('Location', int(locParam))
		location = Location.get(locationKey)
		logging.info("location: " + str(location));
		exits = Exit.gql("WHERE ANCESTOR IS :1", location);
		#exits = Exit.all()
		#.ancestor(location)
		logging.info("exits: " + str(exits.count()));
		list = []
		for exit in exits:
			#pprint(inspect.getmembers(exit))
			obj = {"name": exit.name, "id": str(exit.key().id()), "hint": exit.hint, "location": str(exit.parent_key().id())}
			list.append(obj)
		response = simplejson.dumps(list)
		self.response.out.write(response)
	
	def post(self):
		logging.info("POST")		
		val = self.request.body
		logging.info("BODY:" + val)		
		obj = simplejson.loads(val);
		logging.info("OBJECT:" + str(obj))	
		location = db.Key.from_path('Location', int(obj['location']))
		logging.info("Location: " + str(location.id()))
		exit = Exit(parent=location, name = obj['name'], hint = obj['hint'])
		exit.put()
		#logging.info("exit: " + inspect(exit))
		#pprint(inspect.getmembers(exit))
		logging.info("Parent id: " + str(exit.parent_key().id()))
		self.response.out.write(str(exit.key().id()));


def main():
	application = webapp.WSGIApplication([('/locations', LocationHandler), ('/exits', ExitHandler)])
	util.run_wsgi_app(application)

if __name__ == '__main__':
	main()