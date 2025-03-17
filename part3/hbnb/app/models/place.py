from .baseclass import BaseModel
from app import db
from .amenity_place import amenity_place
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class Place(BaseModel):
    __tablename__ = 'places'

    _title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    _price = db.Column(db.Float, nullable=False)
    _latitude = db.Column(db.Float(90), nullable=False)
    _longitude = db.Column(db.Float(180), nullable=False)
    _owner_id = db.Column(db.String, ForeignKey('users.id'), nullable=False)
    amenities = db.relationship('Amenity', secondary=amenity_place, lazy='subquery', backref=db.backref('places', lazy=True))    
    reviews = relationship('Review', backref='place', lazy=True)

    def add_review(self, review_id):
        """Add a review to the place."""
        self.reviews.append(review_id)

    def delete_review(self, review_id):
        """Delete a review from the place when review removed."""
        self.reviews.remove(review_id)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        from app.models.amenity import Amenity
        # Getting amenity ID to add it in amenities
        if isinstance(amenity, Amenity):
            amenity = amenity.id
        self.amenities.append(amenity)


    def to_dict(self):
        """Convert a data object to dictionary"""
        return {'id': self.id,
                'title': self.title,
                'description': self.description,
                'price': self.price,
                'latitude': self.latitude, 
                'longitude': self.longitude,
                'owner_id': self.owner_id
            }


    @property
    def title(self):
        """Getter for title (protected property)"""
        return self._title


    @title.setter
    def title(self, value):
        """Setter for title (protected property to check length)"""
        # Checking if title is a string
        if not isinstance(value, str):
            raise TypeError("The title should be a string")
        # Checking the minimum length of title
        if len(value) < 5:
            raise ValueError("Title cannot be less than 5 characters")
        # Checking the maximul length of title
        if len(value) >= 100:
            raise ValueError("Title cannot be longer than 100 characters")
        self._title = value


    @property
    def price(self):
        """Getter for price (private property)"""
        return self._price


    @price.setter
    def price(self, value):
        """Setter for price (private property)"""
        # Checking if price is an integer or a float
        if not isinstance(value, (int, float)):
            raise TypeError("The price should be an float or integer")
        # Ensuring that the price is not 0
        if value >= 0:
            self._price = value
        else:
            raise ValueError("The price must be a positive float number.")


    @property
    def latitude(self):
        """Getter for latitude (private property)"""
        return self._latitude


    @latitude.setter
    def latitude(self, value):
        """Setter for latitude (private property)"""
        # Checking if the latitude is an integer or a float
        if not isinstance(value, (int, float)):
            raise TypeError("The latitude should be a float or integer")
        # Ensuring that the latitude is between -90 and 90
        if value >= -90 and value <= 90:
            self._latitude = value
        else:
            raise ValueError("The latitude must be between -90 and 90.")


    @property
    def longitude(self):
        """Getter for longitude (private property)"""
        return self._longitude


    @longitude.setter
    def longitude(self, value):
        """Setter for longitude (private property)"""
        # Checking if the longitude is an integer or a float
        if not isinstance(value, (int, float)):
            raise TypeError("The longitude should be a float or integer")
        # Ensuring that the longitude is between -180 and 180
        if value >= -180 and value <= 180:
            self._longitude = value
        else:
            raise ValueError("The longitude must be between -180 and +180.")


    @property
    def owner_id(self):
        """Getter for owner (private property)"""
        return self._owner_id


    @owner_id.setter
    def owner_id(self, value):
        """Setter for owner (private property)"""
        from app.models.user import User
        # Ensuring that owner_id is really an ID
        if isinstance(value, User):
            self._owner_id = value.id
        elif isinstance(value, str):
            self._owner_id = value
        else:
            raise TypeError('Owner must be a tupple of type User or a string')
