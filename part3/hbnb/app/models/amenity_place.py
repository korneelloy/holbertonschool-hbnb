from sqlalchemy import Table, Column, String, ForeignKey, UUID
from app import db


amenity_place = db.Table('amenity_place',
                         Column('place_id', UUID(as_uuid=True), ForeignKey('places.id'), primary_key=True),
                         Column('amenity_id', UUID(as_uuid=True), ForeignKey('amenities.id'), primary_key=True)
                         )
