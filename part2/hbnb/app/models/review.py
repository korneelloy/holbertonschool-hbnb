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
        pattern = r'^[1-5]$'
        if re.match(pattern, value):
            self._rating = value
        else:
            raise ValueError('Rating must be an integer between 1 and 5')
    
    @property
    def comment(self):
        return self._comment

    @comment.setter
    def comment(self, value):
        pattern = r'^[a-zA-Z0-9]+$'
        if re.match(pattern, value) and len(pattern) < 300:
            self._comment = value
        else:
            raise ValueError('Comment must be 300 characters max and have letters and/or numbers')

    @property
    def place(self):
        return self.__place

    @place.setter
    def place(self, value):
        if isinstance(value, str):
            self.__place = value
        else:
            raise TypeError('Value must be a string')

    @property
    def user(self):
        return self.__user

    @user.setter
    def user(self, value):
        if isinstance(value, str):
            self.__user = value
        else:
            raise TypeError('Value must be a string')
