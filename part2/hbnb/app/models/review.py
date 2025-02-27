from app.models.basemodel import BaseModel
import re

class Review(BaseModel):
    def __init__(self, comment, rating, place_id, user_id):
        super().__init__()
        self.rating = rating #protected attribute
        self.comment = comment #protected attribute
        self.place_id = place_id #private attribute
        self.user_id = user_id #private attribute

    def to_dict(self):
        return {
            'review_id': self.id,
            'rating': self.rating,
            'comment': self.comment,
            'place_id': self.place_id,
            'user_id': self.user_id
            }

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
        pattern = r'^[a-zA-Z0-9éèàç!.,?:\'\s-]+$'
        if re.match(pattern, value) and len(pattern) < 300:
            self._comment = value
        else:
            raise ValueError('Comment must be 300 characters max and have letters and/or numbers')

    @property
    def place_id(self):
        return self.__place_id

    @place_id.setter
    def place_id(self, value):
        from app.models.place import Place
        if isinstance(value, Place):
            self.__place_id = value.id
        elif isinstance(value, str):
            self.__place_id = value
        else:
            raise TypeError('Place must be a tupple of type place or an ID')

    @property
    def user_id(self):
        return self.__user_id

    @user_id.setter
    def user_id(self, value):
        from app.models.user import User
        if isinstance(value, User):
            self.__user_id = value.id
        elif isinstance(value, str):
            self.__user_id = value            
        else:
            raise TypeError('User must be a tupple of type user')
