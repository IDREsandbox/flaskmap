#from config import *
from flask import Flask, jsonify, render_template, request
import simplejson
from playhouse.shortcuts import model_to_dict, dict_to_model
from flask_marshmallow import Marshmallow

# define the app here
app = Flask(__name__)

# here is the marshmallow app definition for the api
ma = Marshmallow(app)

# bring in the table models
from models import *

### api schema begins here ###
class bookingSchema(ma.Schema):
	class Meta:
		# Fields to expose through api
		# fields = ('fid', 'desc_', 'slug','sex','home_addre','x','y')
		fields = ('booking_nu','sex','race','charge_des','charge_lev','year','x','y','slug','age_categories','_cost','distance')
		json_module = simplejson

booking_schema = bookingSchema()
bookings_schema = bookingSchema(many=True)

class raceSchema(ma.Schema):
	class Meta:
		# Fields to expose through api
		# fields = ('fid', 'desc_', 'slug','sex','home_addre','x','y')
		fields = ('race','count')
		json_module = simplejson

race_schema = raceSchema()
races_schema = raceSchema(many=True)

### api schema ends here ###

# def basicQuery():
# 	global bookings
# 	global neighborhoods

# 	bookings = lapd.select()
#     # neighborhoods = lapd.select(lapd.slug).distinct().order_by(lapd.slug.asc())
# 	neighborhoods = lapd.select(lapd.slug).distinct().order_by(lapd.slug.asc())
# 	# bookings = lapd.select().where(lapd.slug == "downtown")

@app.route('/')
def index():
	# basicQuery()
	neighborhoods = lasd.select(lasd.slug).distinct().order_by(lasd.slug.asc())
	return render_template('index.html',neighborhoods = neighborhoods)

# select bookings within a radius
@app.route("/bookings/<lat>/<lng>/<distance>", methods=['GET'])
def get_bookings_by_distance(lat,lng,distance):
	coords = lng+' '+lat
	all_bookings = lasd.select().where(fn.ST_DWithin(lasd.geom, fn.ST_GeogFromText('POINT('+coords+')'),distance))
	result = bookings_schema.dump(all_bookings)
	return jsonify(result.data)

# select cost from a given point
@app.route("/cost/<lat>/<lng>", methods=['GET'])
def get_cost_by_distance(lat,lng):
	coords = lng+' '+lat
	all_bookings = lasd.select(lasd.sex,lasd.race,lasd.charge_des,lasd.charge_lev,lasd.year,lasd.x,lasd.y,lasd.slug,lasd.age_categories,lasd._cost,fn.ST_Distance(lasd.geom, fn.ST_GeogFromText('POINT('+coords+')')).alias('distance')).order_by(fn.ST_Distance(lasd.geom, fn.ST_GeogFromText('POINT('+coords+')'))).limit(1000)
	result = bookings_schema.dump(all_bookings)
	return jsonify(result.data)

# get bookings by neighborhood
@app.route("/<slug>/bookings/", methods=['GET'])
def get_bookings(slug):
	all_bookings = lasd.select().where(lasd.slug == slug)
	# all_bookings = lasd.select().where(lasd.slug == slug)
	result = bookings_schema.dump(all_bookings)
	return jsonify(result.data)

@app.route("/<slug>/<year>/race/", methods=['GET'])
def get_race(slug,year):
	all_bookings = lasd.select(lasd.race,fn.COUNT(lasd.race)).where(lasd.slug == slug,lasd.year==year).group_by(lasd.race)
	# all_bookings = lasd.select().where(lasd.slug == slug)
	result = races_schema.dump(all_bookings)
	return jsonify(result.data)


### not needed anymore ###
# @app.route('/_neighborhood')
# def neighborhood():
# 	slug = request.args.get('slug')
# 	# return slug
# 	bookings = lapd.select().where(lapd.slug == slug)
# 	# json_data = json.dumps(model_to_dict(bookings))
# 	# return json_data
# 	# return jsonify(model_to_dict(bookings))
# 	return BinaryJSONField({'rows':[model_to_dict(booking) for booking in bookings]})

@app.route('/_add_numbers')
def add_numbers():
	a = request.args.get('a', 0, type=int)
	b = request.args.get('b', 0, type=int)
	return jsonify(result=a + b)

# @app.route('/info')
# def info():
#   basicQuery()
#   return render_template('info.html', events=events)  

if __name__ == '__main__':
	app.run(debug=True)
