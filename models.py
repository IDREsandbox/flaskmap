# Import from peewee
from peewee import *

# Connect to the PostgresqlDatabase

db = PostgresqlDatabase(
    'postgres', user='postgres', password='yoh', host='localhost', port=5432)
# Connect to our database.
db.connect()

class GeomField(Field):
    db_field = 'geometry'
    def __init__(self, geom_type=None, geom_srid=None, **kwargs):
        self.geom_srid = geom_srid
        self.geom_type = geom_type
        super(GeomField, self).__init__(**kwargs)
        if geom_type:
            if geom_srid:
                self.db_field = 'geometry(%s, %s)' % (geom_type, geom_srid)
            else:
                self.db_field = 'geometry(%s)' % (geom_type, )

class lasd(Model):
    # These are all the fields it has
    # match up CharField/IntegerField/etc with correct type
    geom = GeomField()
    booking_nu = CharField(primary_key=True)  # primary key = unique id
    sex = CharField()
    race = CharField()
    # charge = CharField()
    charge_des = CharField()
    charge_lev = CharField()
    # bail = CharField()
    year = CharField()
    _cost = DecimalField(null=True)
    x = DecimalField(null=True)
    y = DecimalField(null=True)
    slug = CharField()
    age_categories = CharField()
    # distance = DecimalField(null=True)

    class Meta:
        # data is coming from schools.db
        database = db
        # and it's in the table called 'events'
        db_table = 'lasd_2012_2016'
