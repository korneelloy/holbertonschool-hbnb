from sqlalchemy import Table, Column, String, ForeignKey
from app import db

amenity_place = db.Table('amenity_place',
                         Column('amenity_id', String, ForeignKey('amenity.id'), primary_key=True),
                         Column('place_id', String, ForeignKey('place.id'), primary_key=True)
                         )
