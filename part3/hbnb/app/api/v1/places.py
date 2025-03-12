from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity


api = Namespace('places', description='Place operations')

"""Define the models for related entities"""
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity'),
    'description': fields.String(description='Description of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'amenities': fields.List(fields.String(), required=True, description="List of amenities ID's")
})


@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @api.doc(security="Bearer Auth")
    @jwt_required()
    def post(self):
        """Register a new place"""
        place_data = api.payload
        # Getting the ID of the logged in user
        current_user = get_jwt_identity()
        if current_user:
            place_data['owner_id'] = current_user
        else:
            return {"error": "Invalid Input Data"}
        # Ensuring that the user exist
        if facade.get_user(place_data['owner_id']) is None:
            return {"error": "Invalid Input Data"}, 400
        # Ensuring that place got amenity
        for amenity in place_data['amenities']:
            if facade.get_amenity(amenity) is None:
                return {"error": "Invalid Input Data"}, 400
        # Creating the place
        try:
            new_place = facade.create_place(place_data)
        except:
            return {"error": "Invalid Input Data"}, 400
        return {
            'id': new_place.id,
            'title': new_place.title,
            'description': new_place.description,
            'price': new_place.price,
            'latitude': new_place.latitude,
            'longitude': new_place.longitude,
            'owner_id': new_place.owner_id,
            'reviews': new_place.reviews, 
            'amenities': new_place.amenities
            }, 201


    @api.response(200, 'List of places retrieved successfully')
    @api.response(404, 'Places not found')
    def get(self):
        """Retrieve a list of all places"""
        places = facade.get_all_places()
        if not places:
            return {'error': 'Places not found'}, 404
        return places, 200


@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return {
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'price': place.price, 
            'latitude': place.latitude,
            'longitude': place.longitude,
            'owner_id': place.owner_id,
            'reviews': place.reviews,
            'amenities': place.amenities
            }, 200


    @api.expect(place_model, validate=True)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    @api.doc(security="Bearer Auth")
    @jwt_required()
    def put(self, place_id):
        """Update a place's information"""
        place_data = api.payload
        current_user = get_jwt_identity()
        # Ensuring that the place exist
        existing_place = facade.get_place(place_id)
        if not existing_place:
            return {'error': 'Place not found'}, 404
        # Checking the owner/user existence
        if facade.get_user(existing_place.owner_id) is None:
            return {"error": "Invalid Input Data"}, 400
        # Ensuring that the owner is the user logged in
        if existing_place.owner_id != current_user:
            return {'error': 'Unauthorized action'}, 403
        # Ensuring that the place amenity exist
        for amenity in place_data['amenities']:
            if facade.get_amenity(amenity) is None:
                return {"error": "Invalid Input Data"}, 400
        # Updating informations of the place
        try:
            updated_place = facade.update_place(place_id, place_data)
        except:
            return {"error": "Invalid Input Data"}, 400
        return {
            'id': place_id,
            'title': updated_place.title,
            'description': updated_place.description,
            'price': updated_place.price,
            'latitude': updated_place.latitude,
            'longitude': updated_place.longitude,
            'owner_id': updated_place.owner_id,
            'reviews': updated_place.reviews, 
            'amenities': updated_place.amenities
            }, 200
