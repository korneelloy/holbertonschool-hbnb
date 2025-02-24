from app.models.basemodel import BaseModel

class User(BaseModel):
    def __init__(self, first_name, last_name, email, password, is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.is_admin = is_admin
        self.places = []
        self.reviews = []


    def add_place(self, place):
        """Add a place to the User (One-to-many relationship)"""
        self.places.append(place)

    def add_review(self, review):
        """Add a review to the User (One-to-many relationship)"""
        self.reviews.append(review)
