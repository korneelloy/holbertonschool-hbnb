from app.models.amenity import Amenity

def test_amenity_creation():
    amenity = Amenity(name="Wi-Fi", description="There is Wi-Fi")
    assert amenity.name == "Wi-Fi"
    assert amenity.description == "There is Wi-Fi"
    print("Amenity creation test passed!")

test_amenity_creation()
