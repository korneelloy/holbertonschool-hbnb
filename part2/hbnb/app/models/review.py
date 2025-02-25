from app.models.basemodel import BaseModel

class Review(BaseModel):
    def __init__(self, comment, rating, place, user):
        super().__init__()
        self.rating = rating #public attribute
        self.comment = comment #public attribute
        self.place = place #private attribute
        self.user = user #private attribute
