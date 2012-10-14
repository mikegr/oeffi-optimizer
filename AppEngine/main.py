import logging
import inspect
from pprint import pprint
from django.utils import simplejson
from datetime import datetime, timedelta, tzinfo 
from google.appengine.api import users
from google.appengine.ext import blobstore
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext.webapp.util import run_wsgi_app



MASK = "%a, %d %b %Y %H:%M:%S %Z" 

class Location(db.Model):
	name = db.TextProperty() 
	date = db.DateTimeProperty(auto_now_add=True)

class Exit(db.Model):
	location = db.IntegerProperty() 
	name = db.TextProperty() 
	hint = db.TextProperty() 
	date = db.DateTimeProperty(auto_now_add=True)


class LocationHandler(webapp.RequestHandler):
	
	def get(self):
		
		maxDateRow = db.GqlQuery('SELECT date FROM Location ORDER BY date').get()
		
		if (maxDateRow is not None): 
			modifiedSinceStr = self.request.headers.get('If-Modified-Since', None)
			
			modifiedSince = datetime.strptime(modifiedSinceStr, MASK) if modifiedSinceStr is not None else None
				
			logging.info("If-Modified-Since: " + str(modifiedSince))
			
			maxDate = maxDateRow.date.replace(microsecond=0)
			
			logging.info("maxDate:" + str(maxDate))
			
			isNotModified = maxDate <= modifiedSince
			
			logging.info("seconds:" + str(isNotModified))
			
			
			if ((modifiedSince is not None) and isNotModified):
				self.response.set_status(304)
				return
			else:
				self.response.headers['Last-Modified'] = maxDate.strftime(MASK) + "GMT"
				
		self.response.headers['Content-Type'] = 'application/json'
		locations = db.GqlQuery("SELECT * FROM Location");
		
		list = []
		for loc in locations:
			obj = {"key": str(loc.key()), "id": str(loc.key().id()), "name": loc.name}
			if loc.parent() is not None:
				obj['parent'] = str(loc.parent().key())
			
			list.append(obj)
		response = simplejson.dumps(list)

		self.response.out.write(response)
	

	def post(self):
		logging.info("POST")		
		val = self.request.body
		logging.info("BODY:" + val)		
		obj = simplejson.loads(val);
		logging.info("OBJECT:" + str(obj))	
		
		location = Location(name = obj['name'])  if 'parent' not in obj  else Location(parent = db.Key(encoded=str(obj['parent'])), name = obj['name'])
			
		location.put();
			
		self.response.out.write(str(location.key()));
	
class ExitHandler(webapp.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'application/json'
		locParam = self.request.get("location");
		logging.info("param: " + locParam)
		locationKey = db.Key(encoded=locParam)
		location = Location.get(locationKey)
		logging.info("location: " + str(location));
		exits = Exit.gql("WHERE ANCESTOR IS :1", location);
		#exits = Exit.all()
		#.ancestor(location)
		logging.info("exits: " + str(exits.count()));
		list = []
		for exit in exits:
			#pprint(inspect.getmembers(exit))
			obj = {"name": exit.name, "key": str(exit.key()), "hint": exit.hint, "location": str(exit.parent_key())}
			list.append(obj)
		response = simplejson.dumps(list)
		self.response.out.write(response)
	
	def post(self):
		logging.info("POST")		
		val = self.request.body
		logging.info("BODY:" + val)		
		obj = simplejson.loads(val);
		logging.info("OBJECT:" + str(obj))	
		location = db.Key(encoded=obj['location'])
		exit = Exit(parent=location, name = obj['name'], hint = obj['hint'])
		exit.put()
		#logging.info("exit: " + inspect(exit))
		#pprint(inspect.getmembers(exit))
		#logging.info("Parent id: " + str(exit.parent_key().id()))
		self.response.out.write(str(exit.key()));


def main():
	application = webapp.WSGIApplication([('/locations', LocationHandler), ('/exits', ExitHandler)])
	util.run_wsgi_app(application)

if __name__ == '__main__':
	main()