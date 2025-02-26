from app.models.basemodel import BaseModel
import re

class Review(BaseModel):
    def __init__(self, comment, rating, place, user):
        super().__init__()
        self.rating = rating #protected attribute
        self.comment = comment #protected attribute
        self.place = place #private attribute
        self.user = user #private attribute

    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, value):
        if 1 <= value <= 5:
            self._rating = value
        else:
            raise ValueError('Rating must be an integer between 1 and 5')
    
    @property
    def comment(self):
        return self._comment

    @comment.setter
    def comment(self, value):
        pattern = r'^[a-zA-Z0-9éèà!.,?:\'\s-]+$'
        if re.match(pattern, value) and len(pattern) < 300:
            self._comment = value
        else:
            raise ValueError('Comment must be 300 characters max and have letters and/or numbers')

    @property
    def place(self):
        return self.place

    @place.setter
    def place(self, value):
        from app.models.place import Place
        if isinstance(value, Place):
            self.place = value.id
        elif isinstance(value, str):
            self.place = value
        else:
            raise TypeError('Place must be a tupple of type place')

    @property
    def user(self):
        return self.user

    @user.setter
    def user(self, value):
        from app.models.user import User
        if isinstance(value, User):
            self.user = value.id
        elif isinstance(value, str):
            self.user = value            
        else:
            raise TypeError('User must be a tupple of type user')
