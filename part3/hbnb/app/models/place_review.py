from sqlalchemy import Table, Column, String, ForeignKey
from app import db

place_review = db.Table('place_review',
                         Column('place_id', String, ForeignKey('place.id'), primary_key=True),
                         Column('review_id', String, ForeignKey('review.id'), primary_key=True)
                         )
