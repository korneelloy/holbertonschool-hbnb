from app.models.basemodel import BaseModel
import re

class User(BaseModel):
    def __init__(self, first_name, last_name, email, password, is_admin=False):
        super().__init__()
        self.first_name = first_name #protected attribute
        self.last_name = last_name #protected attribute
        self.email = email #private attribute
        self.password = password #private attribute
        self.is_admin = is_admin #private attribute
        self.places = []
        self.reviews = []

    @property
    def first_name(self):
        """getter for first_name (protected property)"""
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        """setter for first_name (protected property to check lenght)"""
        if not isinstance(value, str):
            raise TypeError("First name should be a string")
        if len(value) >= 50:
            raise ValueError("First name cannot be longer than 50 characters")
        self._first_name = value

    @property
    def last_name(self):
        """getter for last_name (protected property)"""
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        """setter for last_name (protected property to check lenght)"""
        if not isinstance(value, str):
            raise TypeError("Last name should be a string")
        if len(value) >= 50:
            raise ValueError("Last name cannot be longer than 50 characters")
        self._last_name = value

    @property
    def email(self):
        """getter for email (private property)"""
        return self.__email
    
    @email.setter
    def email(self, value):
        """setter for email (private property)"""
        if not isinstance(value, str):
            raise TypeError("The email should be a string")
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if re.match(pattern, value):
            self.__email = value
        else:
            raise ValueError("The email doesn't seem to be an correct email address. Please check.")

    @property
    def password(self):
        """getter for password (private property)"""
        return self.__password
    
    @password.setter
    def password(self, value):
        """setter for password (private property)"""
        if not isinstance(value, str):
            raise TypeError("The password should be a string")
        pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$"
        if re.match(pattern, value):
            self.__password = value
        else:
            raise ValueError("The password should be at least 8 characters long, and contain at least one upper, and one lowercase, and one digit.")
    
    @property
    def is_admin(self):
        """getter for is_admin (private property)"""
        return self.__is_admin
    
    @is_admin.setter
    def is_admin(self, value):
        """setter for is_admin (private property)"""
        self.__is_admin = value
    
    def add_place(self, place):
        """Add a place to the User (One-to-many relationship)"""
        self.places.append(place)

    def add_review(self, review):
        """Add a review to the User (One-to-many relationship)"""
        self.reviews.append(review)

