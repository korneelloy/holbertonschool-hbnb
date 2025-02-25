from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_all_users(self):
        users = self.user_repo.get_all()
        user_list = [user.to_dict() for user in users]
        return user_list

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)
    
    def update_user(self, user_id, user_data):
        updated_user = self.user_repo.update(user_id, user_data)
        return(updated_user)


    # Placeholder method for fetching a place by ID
    def create_place(self, place_data):
        place = Place(**place_data)
        self.place_repo.add(place)
        return place

    def update_place(self, place_id, place_data):
        # Placeholder for logic to update a place
        pass

    def get_place(self, place_id):
        """Get the place"""
        return self.place_repo.get(place_id)

    def get_place_id(self):
        """Get the place_id"""
        return self.place_repo.get()

    def get_all_places(self):
        # Placeholder for logic to retrieve all places
        pass

    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def update_amenity(self, amenity_id, amenity_data):
        # Placeholder for logic to update an amenity
        pass

    def get_amenity(self, amenity_id):
       return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo

    def create_review(self, review_data):
        # Placeholder for logic to create a review, including validation for user_id, place_id, and rating
        pass

    def update_review(self, review_id, review_data):
        # Placeholder for logic to update a review
        pass

    def get_review(self, review_id):
        # Placeholder for logic to retrieve a review by ID
        pass

    def get_all_reviews(self):
        # Placeholder for logic to retrieve all reviews
        pass

    def get_reviews_by_place(self, place_id):
        # Placeholder for logic to retrieve all reviews for a specific place
        pass

    def delete_review(self, review_id):
        # Placeholder for logic to delete a review
        pass
