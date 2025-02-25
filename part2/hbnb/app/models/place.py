from app.models.basemodel import BaseModel

class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        self.title = title #protected attribute
        self.description = description #public attribute
        self.price = price #private attribute
        self.latitude = latitude #private attribute
        self.longitude = longitude #private attribute
        self.owner = owner #private attribute
        self.reviews = []  # List to store related reviews
        self.amenities = []  # List to store related amenities

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)


    @property
    def title(self):
        """getter for title (protected property)"""
        return self._title

    @title.setter
    def title(self, value):
        """setter for title (protected property to check lenght)"""
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
        if value >= -180 and value <= 180:
            self.__longitude = value
        else:
            raise ValueError("The longitude must be between -180 and +180.")
    
    @property
    def owner(self):
        """getter for owner (private property)"""
        return self.__owner
    
    @owner.setter
    def owner(self, value):
        """setter for owner (private property)"""
        """
        owners = UserList()
        if value in owner.id:
            self.__owner = value
        else:
            raise ValueError("TThe owner doesn't seem to exists")
            """
