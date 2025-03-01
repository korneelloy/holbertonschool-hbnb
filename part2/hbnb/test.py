import unittest
from app import create_app
import json

class Test_Endpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    """--------------------USER TEST-----------------------"""

    def test1_create_user(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com",
            "password": "TestPassword56"
        })
        message = json.loads(response.text)
        Test_Endpoints.id = message["id"]
        self.assertEqual(response.status_code, 201)

    def test1_create_user_invalid_empty_data_first_name(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "",
            "last_name": "test",
            "email": "test@test.com",
            "password": "TestPassword56"
        })
        self.assertEqual(response.status_code, 400)

    def test1_create_user_invalid_empty_data_last_name(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Vitushan",
            "last_name": "",
            "email": "test@test.com",
            "password": "TestPassword56"
        })
        self.assertEqual(response.status_code, 400)

    def test1_create_user_invalid_empty_data_email_name(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Vitushan",
            "last_name": "Test",
            "email": "",
            "password": "TestPassword56"
        })
        self.assertEqual(response.status_code, 400)

    def test1_create_user_invalid_empty_data_pw(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Vitushan",
            "last_name": "Test",
            "email": "test@test.com",
            "password": ""
        })
        self.assertEqual(response.status_code, 400)

    def test1_create_user_invalid_email(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Vitushan",
            "last_name": "Dupont",
            "email": "invalid-email",
            "password": "TestPassword56"
        })
        self.assertEqual(response.status_code, 400)

    def test1_create_user_invalid_pw_sans_majuscules(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Vitushan",
            "last_name": "Dupont",
            "email": "test@test.com",
            "password": "testsansmajuscules456"
        })
        self.assertEqual(response.status_code, 400)

    def test1_create_user_invalid_pw_without_numbers(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Vitushan",
            "last_name": "Dupont",
            "email": "test@test.com",
            "password": "testSansChiffres"
        })
        self.assertEqual(response.status_code, 400)

    def test2_change_user(self):
        route = f'/api/v1/users/{Test_Endpoints.id}'
        response = self.client.put(route, json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@exahhjmple.com",
            "password": "TestPassword56"
        })
        self.assertEqual(response.status_code, 200)

    def test2_change_user_invalid(self):
        route = f'/api/v1/users/{Test_Endpoints.id}'
        response = self.client.put(route, json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@exahhjmple.com",
            "password": "passwordinvalid"
        })
        self.assertEqual(response.status_code, 400)
    
    def test3_liste_all_users(self):
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, 200)

    def test0_liste_all_users_with_zero_users(self):
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, 404)

    def test4_get_user_by_id(self):
        response = self.client.get(f'/api/v1/users/{Test_Endpoints.id}')
        self.assertEqual(response.status_code, 200)

    def test4_get_user_by_id_wrong(self):
        response = self.client.get('/api/v1/users/xxx')
        self.assertEqual(response.status_code, 404)

    """--------------------AMENITIES TEST-----------------------"""

    def test1_create_amenity(self):
        response = self.client.post('/api/v1/amenities/', json={
            "name": "lavabo",
            "description": "un très joli lavabo",
        })
        self.assertEqual(response.status_code, 201)

    def test1_create_amenity_invalid_data(self):
        response = self.client.post('/api/v1/amenities/', json={
            "name": "",
            "description": "un très joli lavabo"
        })
        self.assertEqual(response.status_code, 400)

    def test2_get_amenities_list(self):
        response = self.client.get('/api/v1/amenities/')
        self.assertEqual(response.status_code, 200)

    def test0_get_amenities_empty_list(self):
        response = self.client.get('/api/v1/amenities/')
        self.assertEqual(response.status_code, 404)

    def test3_get_amenity_by_id(self):
        amenity = self.client.post('/api/v1/amenities/', json={
            "name": "lavabo",
            "description": "un très joli lavabo",
        })
        amenity_id = json.loads(amenity.text)
        response = self.client.get(f'/api/v1/amenities/{amenity_id['id']}')
        self.assertEqual(response.status_code, 200)

    def test3_get_amenity_by_id_wrong(self):
        response = self.client.get('/api/v1/amenities/xxx')
        self.assertEqual(response.status_code, 404)

    def test4_change_amenity(self):
        amenity = self.client.post('/api/v1/amenities/', json={
            "name": "lavabo",
            "description": "un très joli lavabo",
        })
        amenity_id = json.loads(amenity.text)
        response = self.client.put(f'/api/v1/amenities/{amenity_id['id']}', json={
            "name": "piscine",
            "description": "ca change"
        })
        self.assertEqual(response.status_code, 200)

    def test4_change_amenity_invalid(self):
        amenity = self.client.post('/api/v1/amenities/', json={
            "name": "lavabo",
            "description": "un très joli lavabo",
        })
        amenity_id = json.loads(amenity.text)
        response = self.client.put(f'/api/v1/amenities/{amenity_id['id']}', json={
            "name": "",
            "description": "ca change"
        })
        self.assertEqual(response.status_code, 400)
    
    def test5_list_all_amenities(self):
        response = self.client.get('/api/v1/amenities/')
        self.assertEqual(response.status_code, 200)

    def test0_list_all_amenities_with_zero_amenities(self):
        response = self.client.get('/api/v1/amenities/')
        self.assertEqual(response.status_code, 404)

    """--------------------PLACE TEST -----------------------"""

    def test6_create_place(self):
        owner = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com",
            "password": "TestPassword56"
        })
        owner_id = json.loads(owner.text)
        amenity = self.client.post('/api/v1/amenities/', json={
            "name": "lavabo",
            "description": "un très joli lavabo",
        })
        amenity_id = json.loads(amenity.text)
        place = self.client.post('/api/v1/places/', json={
            'title': 'maison',
            'description': "C'est une belle maison",
            'price': 99,
            'latitude': 45,
            'longitude': 65,
            'owner_id': owner_id['id'],
            'amenities': [amenity_id['id']]
        })
        self.assertEqual(place.status_code, 201)

    def test6_create_place_invalid_data(self):
        owner = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe2@example.com",
            "password": "TestPassword56"
        })
        owner_id = json.loads(owner.text)
        amenity = self.client.post('/api/v1/amenities/', json={
            "name": "lavabo",
            "description": "un très joli lavabo",
        })
        amenity_id = json.loads(amenity.text)
        place = self.client.post('/api/v1/places/', json={
            'title': 'maison',
            'description': "C'est une belle maison",
            'price': '3_vitushan',
            'latitude': 45,
            'longitude': 65,
            'owner_id': owner_id['id'],
            'amenities': [amenity_id['id']]
        })
        self.assertEqual(place.status_code, 400)

    def test6_get_place_by_id(self):
        owner = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe1@example.com",
            "password": "TestPassword56"
        })
        owner_id = json.loads(owner.text)
        amenity = self.client.post('/api/v1/amenities/', json={
            "name": "lavabo",
            "description": "un très joli lavabo",
        })
        amenity_id = json.loads(amenity.text)
        place = self.client.post('/api/v1/places/', json={
            'title': 'maison',
            'description': "Cest une belle maison",
            'price': 99,
            'latitude': 45,
            'longitude': 65,
            'owner_id': owner_id['id'],
            'amenities': [amenity_id['id']]
        })
        place_id = json.loads(place.text)
        response = self.client.get(f'/api/v1/places/{place_id['id']}')
        self.assertEqual(response.status_code, 200)

    def test7_get_all_places(self):
        response = self.client.get('/api/v1/places/')
        self.assertEqual(response.status_code, 200)

    def test0_get_place_empty_list(self):
        response = self.client.get('/api/v1/places/')
        self.assertEqual(response.status_code, 404)

    def test6_update_place(self):
        owner = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe3@example.com",
            "password": "TestPassword56"
        })
        owner_id = json.loads(owner.text)
        amenity = self.client.post('/api/v1/amenities/', json={
            "name": "lavabo",
            "description": "un très joli lavabo",
        })
        amenity_id = json.loads(amenity.text)
        place = self.client.post('/api/v1/places/', json={
            'title': 'maison',
            'description': "Cest une belle maison",
            'price': 99,
            'latitude': 45,
            'longitude': 65,
            'owner_id': owner_id['id'],
            'amenities': [amenity_id['id']]
        })
        place_id = json.loads(place.text)
        response = self.client.put(f'/api/v1/places/{place_id['id']}', json={
            'title': 'villa',
            'description': "Cest une belle villa",
            'price': 99,
            'latitude': 45,
            'longitude': 65,
            'owner_id': owner_id['id'],
            'amenities': [amenity_id['id']]
        })
        self.assertEqual(response.status_code, 200)

    def test6_put_place_invalid_data(self):
        owner = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe4@example.com",
            "password": "TestPassword56"
        })
        owner_id = json.loads(owner.text)
        amenity = self.client.post('/api/v1/amenities/', json={
            "name": "lavabo",
            "description": "un très joli lavabo",
        })
        amenity_id = json.loads(amenity.text)
        place = self.client.post('/api/v1/places/', json={
            'title': 'maison',
            'description': "C'est une belle maison",
            'price': 99,
            'latitude': 45,
            'longitude': 65,
            'owner_id': owner_id['id'],
            'amenities': [amenity_id['id']]
        })
        place_id = json.loads(place.text)
        response = self.client.put(f'/api/v1/places/{place_id['id']}', json={
            'title': 'villa',
            'description': "Cest une belle villa",
            'price': '3_Vithushan_pas_cher',
            'latitude': 45,
            'longitude': 65,
            'owner_id': owner_id['id'],
            'amenities': [amenity_id['id']]
        })
        self.assertEqual(response.status_code, 400)

    """--------------------REVIEW TEST -----------------------"""

    def test7_create_review(self):
        owner = self.client.post('/api/v1/users/', json={
            "first_name": "VithushOne",
            "last_name": "Vit",
            "email": "Vithushone1@example.com",
            "password": "TestPassword56"
        })
        owner_id = json.loads(owner.text)
        user = self.client.post('/api/v1/users/', json={
            "first_name": "VithushTwo",
            "last_name": "Vit",
            "email": "Vithushtwo1@example.com",
            "password": "TestPassword56"
        })
        user_id = json.loads(user.text)
        amenity = self.client.post('/api/v1/amenities/', json={
            "name": "lavabo",
            "description": "un très joli lavabo",
        })
        amenity_id = json.loads(amenity.text)
        place = self.client.post('/api/v1/places/', json={
            'title': 'maison',
            'description': "Cest une belle maison",
            'price': 99,
            'latitude': 45,
            'longitude': 65,
            'owner_id': owner_id['id'],
            'amenities': [amenity_id['id']]
        })
        place_id = json.loads(place.text)
        review = self.client.post('/api/v1/reviews/', json={
            "rating": 5,
            "comment": "En effet elle est belle",
            "user_id": user_id['id'],
            "place_id": place_id['id']
        })
        self.assertEqual(review.status_code, 201)

    def test7_owner_create_review(self):
        owner = self.client.post('/api/v1/users/', json={
            "first_name": "VithushOne",
            "last_name": "Vit",
            "email": "Vithushone2@example.com",
            "password": "TestPassword56"
        })
        owner_id = json.loads(owner.text)
        amenity = self.client.post('/api/v1/amenities/', json={
            "name": "lavabo",
            "description": "un très joli lavabo",
        })
        amenity_id = json.loads(amenity.text)
        place = self.client.post('/api/v1/places/', json={
            'title': 'maison',
            'description': "Cest une belle maison",
            'price': 99,
            'latitude': 45,
            'longitude': 65,
            'owner_id': owner_id['id'],
            'amenities': [amenity_id['id']]
        })
        place_id = json.loads(place.text)
        review = self.client.post('/api/v1/reviews/', json={
            "rating": 5,
            "comment": "En effet elle est belle",
            "user_id": owner_id['id'],
            "place_id": place_id['id']
        })
        self.assertEqual(review.status_code, 401)

    def test8_create_review_invalid_input(self):
        owner = self.client.post('/api/v1/users/', json={
            "first_name": "VithushOne",
            "last_name": "Vit",
            "email": "VithushoneOn1e@example.com",
            "password": "TestPassword56"
        })
        owner_id = json.loads(owner.text)
        user = self.client.post('/api/v1/users/', json={
            "first_name": "VithushTwo",
            "last_name": "Vit",
            "email": "Vithushtwo2@example.com",
            "password": "TestPassword56"
        })
        user_id = json.loads(user.text)
        amenity = self.client.post('/api/v1/amenities/', json={
            "name": "lavabo",
            "description": "un très joli lavabo",
        })
        amenity_id = json.loads(amenity.text)
        place = self.client.post('/api/v1/places/', json={
            'title': 'maison',
            'description': "Cest une belle maison",
            'price': 99,
            'latitude': 45,
            'longitude': 65,
            'owner_id': owner_id['id'],
            'amenities': [amenity_id['id']]
        })
        place_id = json.loads(place.text)
        review = self.client.post('/api/v1/reviews/', json={
            "rating": 6,
            "comment": "En effet elle est belle",
            "user_id": user_id['id'],
            "place_id": place_id['id']
        })
        self.assertEqual(review.status_code, 400)
    
    def test9_liste_all_reviews(self):
        response = self.client.get('/api/v1/reviews/')
        self.assertEqual(response.status_code, 200)
    
    def test0_liste_all_reviews_with_empty_list(self):
        response = self.client.get('/api/v1/reviews/')
        self.assertEqual(response.status_code, 404)
    

    def test9_get_review_by_id(self):
        owner = self.client.post('/api/v1/users/', json={
            "first_name": "VithushOne",
            "last_name": "Vit",
            "email": "Vithushoneted@example.com",
            "password": "TestPassword56"
        })
        owner_id = json.loads(owner.text)
        user = self.client.post('/api/v1/users/', json={
            "first_name": "VithushTwo",
            "last_name": "Vit",
            "email": "Vithushtwos@example.com",
            "password": "TestPassword56"
        })
        user_id = json.loads(user.text)
        amenity = self.client.post('/api/v1/amenities/', json={
            "name": "lavabo",
            "description": "un très joli lavabo",
        })
        amenity_id = json.loads(amenity.text)
        place = self.client.post('/api/v1/places/', json={
            'title': 'maison',
            'description': "Cest une belle maison",
            'price': 99,
            'latitude': 45,
            'longitude': 65,
            'owner_id': owner_id['id'],
            'amenities': [amenity_id['id']]
        })
        place_id = json.loads(place.text)
        review = self.client.post('/api/v1/reviews/', json={
            "rating": 5,
            "comment": "En effet elle est belle",
            "user_id": user_id['id'],
            "place_id": place_id['id']
        })
        review_id = json.loads(review.text)
        response = self.client.get(f'/api/v1/reviews/{review_id['id']}')
        self.assertEqual(response.status_code, 200)

    def test9_update_review(self):
        owner = self.client.post('/api/v1/users/', json={
            "first_name": "VithushOne",
            "last_name": "Vit",
            "email": "Vithushonxeted@example.com",
            "password": "TestPassword56"
        })
        owner_id = json.loads(owner.text)
        user = self.client.post('/api/v1/users/', json={
            "first_name": "VithushTwo",
            "last_name": "Vit",
            "email": "Vithushtwoxs@example.com",
            "password": "TestPassword56"
        })
        user_id = json.loads(user.text)
        amenity = self.client.post('/api/v1/amenities/', json={
            "name": "lavabo",
            "description": "un très joli lavabo",
        })
        amenity_id = json.loads(amenity.text)
        place = self.client.post('/api/v1/places/', json={
            'title': 'maison',
            'description': "Cest une belle maison",
            'price': 99,
            'latitude': 45,
            'longitude': 65,
            'owner_id': owner_id['id'],
            'amenities': [amenity_id['id']]
        })
        place_id = json.loads(place.text)
        review = self.client.post('/api/v1/reviews/', json={
            "rating": 5,
            "comment": "En effet elle est belle",
            "user_id": user_id['id'],
            "place_id": place_id['id']
        })
        review_id = json.loads(review.text)
        response = self.client.put(f"/api/v1/reviews/{review_id['id']}", json={
            "rating": 1,
            "comment": "je savais que Vitushan habitait la meme maison, mais je ne m'attendais pas à partager la chambre",
            "user_id": user_id['id'],
            "place_id": place_id['id']
        })
        self.assertEqual(response.status_code, 200)

    def test9_delete_review(self):
        owner = self.client.post('/api/v1/users/', json={
            "first_name": "VithushOne",
            "last_name": "Vit",
            "email": "Vithushonxkqeted@example.com",
            "password": "TestPassword56"
        })
        owner_id = json.loads(owner.text)
        user = self.client.post('/api/v1/users/', json={
            "first_name": "VithushTwo",
            "last_name": "Vit",
            "email": "Vithushtwoxkzs@example.com",
            "password": "TestPassword56"
        })
        user_id = json.loads(user.text)
        amenity = self.client.post('/api/v1/amenities/', json={
            "name": "lavabo",
            "description": "un très joli lavabo",
        })
        amenity_id = json.loads(amenity.text)
        place = self.client.post('/api/v1/places/', json={
            'title': 'maison',
            'description': "Cest une belle maison",
            'price': 99,
            'latitude': 45,
            'longitude': 65,
            'owner_id': owner_id['id'],
            'amenities': [amenity_id['id']]
        })
        place_id = json.loads(place.text)
        review = self.client.post('/api/v1/reviews/', json={
            "rating": 5,
            "comment": "En effet elle est belle",
            "user_id": user_id['id'],
            "place_id": place_id['id']
        })
        review_id = json.loads(review.text)
        response = self.client.delete(f"/api/v1/reviews/{review_id['id']}")
        self.assertEqual(response.status_code, 200)

    def test9_list_reviews_by_place(self):
        owner = self.client.post('/api/v1/users/', json={
            "first_name": "VithushOne",
            "last_name": "Vit",
            "email": "Vithushonxkqested@example.com",
            "password": "TestPassword56"
        })
        owner_id = json.loads(owner.text)
        user = self.client.post('/api/v1/users/', json={
            "first_name": "VithushTwo",
            "last_name": "Vit",
            "email": "Vithushtwoxkzss@example.com",
            "password": "TestPassword56"
        })
        user_id = json.loads(user.text)
        amenity = self.client.post('/api/v1/amenities/', json={
            "name": "lavabo",
            "description": "un très joli lavabo",
        })
        amenity_id = json.loads(amenity.text)
        place = self.client.post('/api/v1/places/', json={
            'title': 'maison',
            'description': "Cest une belle maison",
            'price': 99,
            'latitude': 45,
            'longitude': 65,
            'owner_id': owner_id['id'],
            'amenities': [amenity_id['id']]
        })
        place_id = json.loads(place.text)
        response = self.client.post('/api/v1/reviews/', json={
            "rating": 5,
            "comment": "En effet elle est belle",
            "user_id": user_id['id'],
            "place_id": place_id['id']
        })
        response = self.client.get(f"/api/v1/reviews/places/{place_id['id']}/reviews")
        self.assertEqual(response.status_code, 200)
