from app.models.place import Place
from app.models.user import User
from app.models.review import Review

def test_place_creation():
    owner = User(first_name="Alice", last_name="Smith", email="alice.smith@example.com", password='Chaussette1')
    place = Place(title="Cozy Apartment", description="A nice place to stay", price=100.0, latitude=37.7749, longitude=-122.4194, owner_id=owner.id, amenities=[])

    # Adding a review
    review = Review(comment="Great stay!", rating=5, place_id=place.id, user_id=owner.id)
    place.add_review(review)

    assert place.title == "Cozy Apartment"
    assert place.price == 100
    assert len(place.reviews) == 1
    assert place.reviews[0].comment == "Great stay!"
    print("Place creation and relationship test passed!")

test_place_creation()
