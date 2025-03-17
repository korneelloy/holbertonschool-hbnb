from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt
from app import db
from sqlalchemy import text


api = Namespace('admin', description='Admin operations')


# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user'),
    'is_admin': fields.Boolean(required=True, description='Administrator privilege')
})


"""Define the amenity model for input validation and documentation"""
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity'),
    'description': fields.String(required=True, description='Description of the amenity')
})


place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'amenities': fields.List(fields.String(), required=True, description="List of amenities ID's")
})


review_model = api.model('Review', {
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'comment': fields.String(required=True, description='Text of the review'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})


@api.route('/users/')
class AdminUserCreate(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created') 
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    @api.doc(security="Bearer Auth")
    @jwt_required()
    def post(self):
        """Register a new user"""

        # Ensuring that the user is admin
        claims = get_jwt()
        is_admin = claims.get("is_admin", False)
        if not is_admin :
            return {'error': 'Admin privileges required'}, 403
        
        # Get input data
        user_data = api.payload

        # Checking existence of the user's email
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400
        
        # Creating the user
        try:
            new_user = facade.create_user(user_data)
        except:
            return {"error": "Invalid Input Data"}, 400
        return {
            'id': new_user.id,
            'first_name': new_user.first_name,
            'last_name': new_user.last_name,
            'email': new_user.email
            }, 201


@api.route('/users/<user_id>')
class AdminUserModify(Resource):
    @api.expect(user_model, validate=True)
    @api.response(200, 'User details retrieved successfully')
    @api.response(400, 'Invalid Input Data')
    @api.response(404, 'User not found')
    @api.doc(security="Bearer Auth")
    @jwt_required()
    def put(self, user_id):
        """change existing user"""

        # Ensuring that the user is admin
        claims = get_jwt()
        is_admin = claims.get("is_admin", False)
        if not is_admin :
            return {'error': 'Admin privileges required'}, 403

        # Get input data
        user_data = api.payload
  
        # Checking if the user exist
        existing_user = facade.get_user(user_id)
        if not existing_user:
            return {'error': 'User not found'}, 404

        # Checking existence of the user's email
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user and existing_user.id != user_id:
            return {'error': 'Email already registered'}, 400

        # Updating user informations
        try:
            updated_user = facade.update_user(user_id, user_data)
        except:
            return {"error": "Invalid Input Data"}, 400
        return {
            'id': user_id,
            'first_name': updated_user.first_name,
            'last_name': updated_user.last_name,
            'email': updated_user.email
            }, 200


@api.route('/amenities/')
class AdminAmenityCreate(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    @api.doc(security="Bearer Auth")
    @jwt_required()
    def post(self):
        """Register a new amenity"""
        
        # Ensuring that the user is admin
        claims = get_jwt()
        is_admin = claims.get("is_admin", False)
        if not is_admin :
            return {'error': 'Admin privileges required'}, 403

        # Get input data
        amenity_data = api.payload

        # Creating new amenity
        try:
            new_amenity = facade.create_amenity(amenity_data)
        except:
            return {"error": "Invalid Input Data"}, 400
        return {
            'id': new_amenity.id,
            'name': new_amenity.name,
            'description': new_amenity.description
            }, 201


@api.route('/amenities/<amenity_id>')
class AdminAmenityModify(Resource):
    @api.expect(amenity_model, validate=True)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    @api.doc(security="Bearer Auth")
    @jwt_required()
    def put(self, amenity_id):
        """Update an amenity's information"""
        
         # Ensuring that the user is admin
        claims = get_jwt()
        is_admin = claims.get("is_admin", False)
        if not is_admin :
            return {'error': 'Admin privileges required'}, 403

        # Get input data
        amenity_data = api.payload

        # Ensuring that the amenity exist
        existing_amenity = facade.get_amenity(amenity_id)
        if not existing_amenity:
            return {'error': 'Amenity not found'}, 404

        # Updating the amenity informations
        try:
            updated_amenity = facade.update_amenity(amenity_id, amenity_data)
        except:
            return {"error": "Invalid Input Data"}, 400
        return {
            'id': amenity_id,
            'name': updated_amenity.name,
            'description': updated_amenity.description
            }, 200


@api.route('/places/<place_id>')
class AdminPlaceModify(Resource):
    @api.expect(place_model, validate=True)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    @api.doc(security="Bearer Auth")
    @jwt_required()
    def put(self, place_id):
        """Update a place's information"""

        # Ensuring that the user is admin
        claims = get_jwt()
        is_admin = claims.get("is_admin", False)
        if not is_admin :
            return {'error': 'Admin privileges required'}, 403

        place_data = api.payload

        # Ensuring that the place exist
        existing_place = facade.get_place(place_id)
        if not existing_place:
            return {'error': 'Place not found'}, 404

        # Ensuring that the amenity or amenities exist
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

    @api.response(200, 'Place deleted successfully')
    @api.response(404, 'Place not found')
    @api.doc(security="Bearer Auth")
    @jwt_required()
    def delete(self, place_id):
        """Delete a place"""

        # Ensuring that the user is admin
        claims = get_jwt()
        is_admin = claims.get("is_admin", False)
        if not is_admin :
            return {'error': 'Admin privileges required'}, 403

        # Ensuring that the targeted place exist
        try:
            facade.get_place(place_id)
        except:
            return {"error": "Not found"}, 404

        # Deleting all reviews attached to the place
        all_reviews = facade.get_reviews_by_place(place_id)
        for review in all_reviews:
            facade.delete_review(review['id'])

        # Deleting the place
        facade.delete_place(place_id)
        return {"message": "Place deleted successfully"}, 200


@api.route('/reviews/<review_id>')
class AdminReviewModify(Resource):
    @api.expect(review_model, validate=True)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    @api.doc(security="Bearer Auth")
    @jwt_required()
    def put(self, review_id):
        """Update a review's information"""

        # Get input data
        review_data = api.payload

        # Ensuring that the user is admin
        claims = get_jwt()
        is_admin = claims.get("is_admin", False)
        if not is_admin :
            return {'error': 'Admin privileges required'}, 403

        # Ensuring that the user exist
        if facade.get_user(review_data['user_id']) is None:
            return {"error": "Invalid Input Data"}, 400

        # Ensuring that the place exist
        if facade.get_place(review_data['place_id']) is None:
            return {"error": "Invalid Input Data"}, 400
        
        # Ensuring that the review to modify exist
        existing_review = facade.get_review(review_id)
        if not existing_review:
            return {'error': 'Review not found'}, 404
        
        # Modifying content of the review
        try:
            updated_review = facade.update_review(review_id, review_data)
        except:
            return {"error": "Invalid Input Data"}, 400
        return {
            'id': review_id,
            'rating': updated_review.rating,
            'comment': updated_review.comment,
            'user_id': updated_review.user_id,
            'place_id': updated_review.place_id
            }, 200


    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @api.doc(security="Bearer Auth")
    @jwt_required()
    def delete(self, review_id):
        """Delete a review"""
        
        # Ensuring that the user is admin
        claims = get_jwt()
        is_admin = claims.get("is_admin", False)
        if not is_admin :
            return {'error': 'Admin privileges required'}, 403
        
        # Ensuring that the targeted review exist
        try:
            facade.get_review(review_id)
        except:
            return {"error": "Not found"}, 404

        # Deleting the rerview
        facade.delete_review(review_id)
        return {"message": "Review deleted successfully"}, 200
