from app.models.basemodel import BaseModel


class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner_id, amenities):
        super().__init__()
        self.title = title #protected attribute
        self.description = description #public attribute
        self.price = price #private attribute
        self.latitude = latitude #private attribute
        self.longitude = longitude #private attribute
        self.owner_id = owner_id #private attribute
        self.reviews = []  # List to store related reviews
        self.amenities = amenities if amenities else []

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        from app.models.amenity import Amenity
        if isinstance(amenity, Amenity):
            amenity = amenity.id
        self.amenities.append(amenity)

    def to_dict(self):
        return {'id': self.id,
                'title': self.title,
                'description': self.description,
                'price': self.price,
                'latitude': self.latitude, 
                'longitude': self.longitude,
                'owner_id': self.owner_id,
                'reviews' : self.reviews,
                'amenities': self.amenities
            }


    @property
    def title(self):
        """getter for title (protected property)"""
        return self._title

    @title.setter
    def title(self, value):
        """setter for title (protected property to check lenght)"""
        if not isinstance(value, str):
            raise TypeError("The title should be a string")
        if len(value) >= 100:
            raise ValueError("Title cannot be longer than 100 characters")
        self._title = value
    
    @property
    def price(self):
        """getter for price (private property)"""
        return self.__price
    
    @price.setter
    def price(self, value):
        """setter for price (private property)"""
        if not isinstance(value, (int, float)):
            raise TypeError("The price should be an float")
        if value >= 0:
            self.__price = value
        else:
            raise ValueError("The price must be a positive float number.")
    
    @property
    def latitude(self):
        """getter for latitude (private property)"""
        return self.__latitude
    
    @latitude.setter
    def latitude(self, value):
        """setter for latitude (private property)"""
        if not isinstance(value, (int, float)):
            raise TypeError("The latitude should be a float")
        if value >= -90 and value <= 90:
            self.__latitude = value
        else:
            raise ValueError("The latitude must be between -90 and 90.")
    
    @property
    def longitude(self):
        """getter for longitude (private property)"""
        return self.__longitude
    
    @longitude.setter
    def longitude(self, value):
        """setter for longitude (private property)"""
        if not isinstance(value, (int, float)):
            raise TypeError("The longitude should be a float")
        if value >= -180 and value <= 180:
            self.__longitude = value
        else:
            raise ValueError("The longitude must be between -180 and +180.")
    
    @property
    def owner_id(self):
        """getter for owner (private property)"""
        return self.__owner_id
    
    @owner_id.setter
    def owner_id(self, value):
        from app.models.user import User
        if isinstance(value, User):
            self.__owner_id = value.id
        elif isinstance(value, str):
            self.__owner_id = value
        else:
            raise TypeError('Owner must be a tupple of type User or a string')
        
        """
        user_mail = facade.get_user_by_email(value)
        if user_mail:
            self.__owner = value
        else:
            raise ValueError("The owner doesn't seem to exists")
        """

