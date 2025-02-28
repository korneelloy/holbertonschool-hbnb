import unittest
from app import create_app
import json

class Test_A_UserEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test1_create_user(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com",
            "password": "TestPassword56"
        })
        message = json.loads(response.text)
        Test_A_UserEndpoints.id = message["id"]
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

    def test1_create_user_invalid_pw_sans_chiffres(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Vitushan",
            "last_name": "Dupont",
            "email": "test@test.com",
            "password": "testSansChiffres"

        })
        self.assertEqual(response.status_code, 400)

    def test2_change_user(self):
        route = f'/api/v1/users/{Test_A_UserEndpoints.id}'
        response = self.client.get(route)
        print(response)
        response = self.client.put(route, json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@exahhjmple.com",
            "password": "TestPassword56"
        })
        self.assertEqual(response.status_code, 200)

    def test2_change_user_invalid(self):
        route = f'/api/v1/users/{Test_A_UserEndpoints.id}'
        response = self.client.get(route)
        print(response)
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
        response = self.client.get(f'/api/v1/users/{Test_A_UserEndpoints.id}')
        self.assertEqual(response.status_code, 200)

    def test4_get_user_by_id_wrong(self):
        response = self.client.get('/api/v1/users/xxx')
        self.assertEqual(response.status_code, 404)

class Test_B_AmenityEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test1_create_amenity(self):
        response = self.client.post('/api/v1/amenities/', json={
            "name": "lavabo",
            "description": "un très joli lavabo",
        })
        message = json.loads(response.text)
        print(message)
        Test_B_AmenityEndpoints.id = message["id"]
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
        response = self.client.get(f'/api/v1/amenities/{Test_B_AmenityEndpoints.id}')
        self.assertEqual(response.status_code, 200)

    def test3_get_amenity_by_id_wrong(self):
        response = self.client.get('/api/v1/amenities/xxx')
        self.assertEqual(response.status_code, 404)

    def test4_change_amenity(self):
        route = f'/api/v1/amenities/{Test_B_AmenityEndpoints.id}'
        response = self.client.get(route)
        print(response)
        response = self.client.put(route, json={
            "name": "piscine",
            "description": "ca change"
        })
        self.assertEqual(response.status_code, 200)

    def test4_change_amenity_invalid(self):
        route = f'/api/v1/amenities/{Test_B_AmenityEndpoints.id}'
        response = self.client.get(route)
        print(response)
        response = self.client.put(route, json={
            "name": "",
            "description": "ca change"
        })
        self.assertEqual(response.status_code, 400)
    
    def test5_liste_all_amenities(self):
        response = self.client.get('/api/v1/amenities/')
        self.assertEqual(response.status_code, 200)

    def test0_liste_all_amenities_with_zero_amenities(self):
        response = self.client.get('/api/v1/amenities/')
        self.assertEqual(response.status_code, 404)


class Test_C_PlaceEndpoints(unittest.TestCase):

    user_id = ""
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
    
    def test1_create_user(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com",
            "password": "TestPassword56"
        })
        message = json.loads(response.text)


    def test6_create_place(self):
        response = self.client.post('/api/v1/places/', json={
            'title': 'Maison',
            'description': "Cest une belle maison",
            'price': '99',
            'latitude': '45',
            'longitude': '65',
            'owner_id': message["user_id"],
            'amenities': []
        })

        message = json.loads(response.text)
        print(message)
        Test_C_PlaceEndpoints.id = message["id"]
        self.assertEqual(response.status_code, 201)
