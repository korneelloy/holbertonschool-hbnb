from app import db, bcrypt
import uuid
import re
from .baseclass import BaseModel

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

    def to_dict(self):
        """Convert a data object to dictionary"""
        return {
            'user_id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email
            }


    def hash_password(self, password):
        from app import bcrypt
        """Hashes the password before storing it."""
        return (bcrypt.generate_password_hash(password).decode('utf-8'))


    def verify_password(self, password):
        from app import bcrypt
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)


    def delete_review(self, review_id):
        """Delete a review from the user when review removed."""
        self.reviews.remove(review_id)


    @property
    def first_name(self):
        """Getter for first_name (protected property)"""
        return self._first_name


    @first_name.setter
    def first_name(self, value):
        """Setter for first_name (protected property to check lenght)"""
        # Checking if first name is a string
        if not isinstance(value, str):
            raise TypeError("First name should be a string")
        # Checking the length of the first name
        if len(value) >= 50 or len(value) < 2:
            raise ValueError("First name cannot be longer than 50 characters or shorter than 2 characters")
        self._first_name = value


    @property
    def last_name(self):
        """Getter for last_name (protected property)"""
        return self._last_name


    @last_name.setter
    def last_name(self, value):
        """Setter for last_name (protected property to check lenght)"""
        # Checking if the last_name is a string
        if not isinstance(value, str):
            raise TypeError("Last name should be a string")
        # Checking the length of the last_name
        if len(value) >= 50 or len(value) < 2:
            raise ValueError("Last name cannot be longer than 50 characters or shorter than 2 characters")
        self._last_name = value


    @property
    def email(self):
        """Getter for email (private property)"""
        return self.__email


    @email.setter
    def email(self, value):
        """Setter for email (private property)"""
        # Checking if the email is a string
        if not isinstance(value, str):
            raise TypeError("The email should be a string")
        # Handling allowed characters in email
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if re.match(pattern, value):
            self.__email = value
        else:
            raise ValueError("The email doesn't seem to be an correct email address. Please check.")


    @property
    def password(self):
        """Getter for password (private property)"""
        return self.__password


    @password.setter
    def password(self, value):
        """Setter for password (private property)"""
        # Checking if the password is a string
        if not isinstance(value, str):
            raise TypeError("The password should be a string")
        # Handling allowed characters in password
        pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$"
        if re.match(pattern, value):
            self.__password = self.hash_password(value)
        else:
            raise ValueError("The password should be at least 8 characters long, and contain at least one upper, and one lowercase, and one digit.")


    @property
    def is_admin(self):
        """Getter for is_admin (private property)"""
        return self.__is_admin


    @is_admin.setter
    def is_admin(self, value):
        """Setter for is_admin (private property)"""
        self.__is_admin = value


    def add_place(self, place):
        """Add a place to the User (One-to-many relationship)"""
        self.places.append(place)


    def add_review(self, review):
        """Add a review to the User (One-to-many relationship)"""
        self.reviews.append(review)

