from app.models.basemodel import BaseModel

class Amenity(BaseModel):
    def __init__(self, name, description):
        super().__init__()
        self.name = name #public attribute
        self.description = description #public attribute
        self.places = []

    def add_place(self, place):
        """Add a place to Amenity (Many-to-many relationship)"""
        self.places.append(place)
