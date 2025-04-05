from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from sqlalchemy import text
from flask import make_response



api = Namespace('places', description='Place operations')

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


@api.route('/', methods=['GET', 'POST'])
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @api.doc(security="Bearer Auth")
    @jwt_required()
    def post(self):
        """Register a new place"""
        
        # Get input data
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
        
        # Ensuring that amenity or amenities exist
        for amenity in place_data['amenities']:
            if facade.get_amenity(amenity) is None:
                return {"error": "Invalid Input Data"}, 400
        
        # putting the amenities "aside":
        amenities = place_data['amenities']
        place_data['amenities'] = []
        
        # Creating the place
        try:
            new_place = facade.create_place(place_data)
        except:
            return {"error": "Invalid Input Data"}, 400
        
        #adding amenities to amenity-place with direct sql:
        if amenities != []:
            query = text("INSERT INTO amenity_place (place_id, amenity_id) VALUES (:place_id, :amenity_id)")
            values = [{"place_id": new_place.id, "amenity_id": amenity} for amenity in amenities]
            db.session.execute(query, values)
            db.session.commit()

        return {
            'id': new_place.id,
            'title': new_place.title,
            'description': new_place.description,
            'price': new_place.price,
            'latitude': new_place.latitude,
            'longitude': new_place.longitude,
            'owner_id': new_place.owner_id
            }, 201


    @api.response(200, 'List of places retrieved successfully')
    @api.response(404, 'Places not found')
    def get(self):
        """Retrieve a list of all places"""
        places = facade.get_all_places()
        if not places:
            return {'error': 'Places not found'}, 404
        return {'places': places}, 200

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
                
        # Getting the amenities with direct sql
        query = text("SELECT amenity_id FROM amenity_place WHERE place_id = :place_id")
        result = db.session.execute(query, {"place_id": place_id})
        data = result.fetchall()
        amenities = [row[0] for row in data]

        # Getting the reviews with direct sql
        query = text("SELECT id FROM reviews WHERE _place_id = :place_id")
        result = db.session.execute(query, {"place_id": place_id})
        data = result.fetchall()
        reviews = [row[0] for row in data]

        return {
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'price': place.price, 
            'latitude': place.latitude,
            'longitude': place.longitude,
            'owner_id': place.owner_id,
            'reviews': reviews,
            'amenities': amenities
            }, 200


    @api.expect(place_model, validate=True)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    @api.doc(security="Bearer Auth")
    @jwt_required()
    def put(self, place_id):
        """Update a place's information"""

        # Get input data
        place_data = api.payload

        # Insuring current user is owner of the place
        current_user = get_jwt_identity()
        if current_user:
            place_data['owner_id'] = current_user
        else:
            return {"error": "Invalid Input Data"}, 400
         
        # Ensuring that the user exist
        if facade.get_user(place_data['owner_id']) is None:
            return {"error": "Invalid Input Data"}, 400

        # Ensuring that the place exist
        existing_place = facade.get_place(place_id)
        if not existing_place:
            return {'error': 'Place not found'}, 404

        # Ensuring that the owner is the user logged in
        if existing_place.owner_id != current_user:
            return {'error': 'Unauthorized action'}, 403

        # Ensuring that amenity/ies exist
        for amenity in place_data['amenities']:
            if facade.get_amenity(amenity) is None:
                return {"error": "Invalid Input Data"}, 400     
        
        # putting the amenities "aside":
        amenities = place_data['amenities']
        place_data['amenities'] = []

        # Updating informations of the place with direct sql:
        query = text("""
            UPDATE places 
            SET _title = :title, 
            description = :description, 
            _price = :price, 
            _latitude = :latitude, 
            _longitude = :longitude
            WHERE id = :place_id
        """)
        db.session.execute(query, {
            "title": place_data["title"], 
            "description": place_data["description"], 
            "price": place_data["price"],
            "latitude": place_data["latitude"], 
            "longitude": place_data["longitude"], 
            "place_id": place_id
        })
        db.session.commit()

        #deleting existing amenities with direct sql: 
        query = text("DELETE FROM amenity_place WHERE place_id = :place_id")
        values = {"place_id": place_id}
        db.session.execute(query, values)
        db.session.commit()

        #adding amenities to amenity-place with direct sql: 
        if amenities != []:
            query = text("INSERT INTO amenity_place (place_id, amenity_id) VALUES (:place_id, :amenity_id)")
            values = [{"place_id": place_id, "amenity_id": amenity} for amenity in amenities]
            db.session.execute(query, values)
            db.session.commit()

        #getting updated info of the place:
        updated_place = facade.get_place(place_id)

        return {
            'id': place_id,
            'title': updated_place.title,
            'description': updated_place.description,
            'price': updated_place.price,
            'latitude': updated_place.latitude,
            'longitude': updated_place.longitude,
            'owner_id': updated_place.owner_id,
            'amenities': amenities
            }, 200
