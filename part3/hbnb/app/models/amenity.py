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


    def to_dict(self):
        """Convert a data object to dictionary"""
        return {
            'amenity_id': self.id,
            'name': self.name,
            'description': self.description
            }


    @property
    def name(self):
        """Getter for name (protected property)"""
        return self._name


    @name.setter
    def name(self, value):
        """Setter for name (protected property to check type + length)"""
        if not isinstance(value, str):
            raise TypeError("The name should be a string")
        if len(value) >= 50 or len(value) < 2:
            raise ValueError("Name cannot be less than 2 nor longer than 50 characters")
        self._name = value

    @property
    def description(self):
        """Getter for description (protected property)"""
        return self._description
    
    @description.setter
    def description(self, value):
        """Setter for description (protected property to check validity + length)"""
        pattern = r'^[a-zA-Z0-9éèàç!.,?:\'\s-]+$'
        if re.match(pattern, value) and len(pattern) < 300:
            self._description = value
        else:
            raise ValueError('Description must be 300 characters max and have letters and/or numbers')
    