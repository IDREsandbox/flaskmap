from flask_sqlalchemy import SQLAlchemy

DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user='postgres',pw='yoh',url='localhost:5432',db='postgres')

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning

db = SQLAlchemy(app)


# # Import from peewee
# from peewee import *

# # Connect to the PostgresqlDatabase
# from sqlalchemy import create_engine
# engine = create_engine('postgresql://postgres:yoh@localhost:5432/postgres')



# db = PostgresqlDatabase('postgres', user='postgres', password='yoh',
# 													 host='localhost', port=5432)
# # Connect to our database.
# db.connect()


class lasd(Model):
	# These are all the fields it has
	# match up CharField/IntegerField/etc with correct type

	booking_nu = CharField(primary_key=True) # primary key = unique id
	sex = CharField()
	race = CharField()
	charge = CharField()
	charge_des = CharField()
	charge_lev = CharField()
	bail = CharField()
	year = CharField()
	longitude = DecimalField(null = True)
	latitude = DecimalField(null = True)
	slug = CharField()
	age_categories = CharField()
	
	class Meta:
		# data is coming from schools.db
		database = db
		# and it's in the table called 'events'
		db_table = 'lasd_2012_2016'


