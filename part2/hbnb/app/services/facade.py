from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review


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
        self.user_repo.update(user_id, user_data)
        return self.user_repo.get(user_id)

    def create_place(self, place_data):
        place = Place(**place_data)
        self.place_repo.add(place)
        return place

    def update_place(self, place_id, place_data):
        self.place_repo.update(place_id, place_data)
        return self.place_repo.get(place_id)

    def get_place(self, place_id):
        """Get the place"""
        return self.place_repo.get(place_id)

    def get_all_places(self):
        places = self.place_repo.get_all()
        place_list = [place.to_dict() for place in places]
        return place_list

    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def update_amenity(self, amenity_id, amenity_data):
        self.amenity_repo.update(amenity_id, amenity_data)
        return self.amenity_repo.get(amenity_id)

    def get_amenity(self, amenity_id):
       return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        amenities = self.amenity_repo.get_all()
        amenity_list = [amenity.to_dict() for amenity in amenities]
        return amenity_list

    def create_review(self, review_data):
        review = Review(**review_data)
        self.review_repo.add(review)
        return review

    def update_review(self, review_id, review_data):
        self.review_repo.update(review_id, review_data)
        return self.review_repo.get(review_id)

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        reviews = self.review_repo.get_all()
        review_list = [review.to_dict() for review in reviews]
        return review_list

    def get_reviews_by_place(self, place_id):
        reviews = self.get_all_reviews()
        review_list = []
        for review in reviews:
            if review['place_id'] == place_id:
                review_list.append(review)
        return review_list

    def delete_review(self, review_id):
        self.review_repo.delete(review_id)
