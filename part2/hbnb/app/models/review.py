from app.models.basemodel import BaseModel

class Review(BaseModel):
    def __init__(self, comment, rating, place, user):
        super().__init__()
        self.rating = rating
        self.comment = comment
        self.place = place
        self.user = user
