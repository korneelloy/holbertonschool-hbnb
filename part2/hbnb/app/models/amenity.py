from app.models.basemodel import BaseModel

class Amenity(BaseModel):
    def __init__(self, name, description):
        super().__init__()
        self.name = name #protected attribute
        self.description = description #public attribute
        self.places = []

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
        if len(value) >= 50:
            raise ValueError("Name cannot be longer than 50 characters")
        self._name = value
    