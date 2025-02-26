from app.models.basemodel import BaseModel
import re

class Amenity(BaseModel):
    def __init__(self, name, description):
        super().__init__()
        self.name = name #protected attribute
        self.description = description #protected attribute
        self.places = [] #public attribute

    def add_place(self, place):
        """Add a place to Amenity (Many-to-many relationship)"""
        self.places.append(place)

    @property
    def name(self):
        """getter for name (protected property)"""
        return self._name

    @name.setter
    def name(self, value):
        """setter for name (protected property to check lenght)"""
        if not isinstance(value, str):
            raise TypeError("The name should be a string")
        if len(value) >= 50 or len(value) < 2:
            raise ValueError("Name cannot be longer than 50 characters")
        self._name = value

    @property
    def description(self):
        return self._description
    
    @description.setter
    def description(self, value):
        pattern = r'^[a-zA-Z0-9éèà!.,?:\'\s-]+$'
        if re.match(pattern, value) and len(pattern) < 300:
            self._description = value
        else:
            raise ValueError('Description must be 300 characters max and have letters and/or numbers')
    