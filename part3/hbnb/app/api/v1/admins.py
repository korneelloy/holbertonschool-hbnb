from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt


api = Namespace('admin', description='Admin operations')


# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
})


"""Define the amenity model for input validation and documentation"""
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity'),
    'description': fields.String(required=True, description='Description of the amenity')
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

        # Ensuring that the user is admin
        claims = get_jwt()
        is_admin = claims.get("is_admin", False)
        if not is_admin :
            return {'error': 'Admin privileges required'}, 403
        
        """Register a new user"""
        user_data = api.payload

        # Checking existence of the user's email
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400
        # Creating the user if not already exist
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
    
    """
    @api.response(200, 'Users details retrieved successfully')
    @api.response(404, 'Users not found')
    def get(self):
        Get users
        users = facade.get_all_users()
        if not users:   
            return {'error': 'Users not found'}, 404
        return users, 200
    """

@api.route('/users/<user_id>')
class AdminUserModify(Resource):
    """
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        Get user details by ID
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
            }, 200
    """

    @api.expect(user_model, validate=True)
    @api.response(200, 'User details retrieved successfully')
    @api.response(400, 'Invalid Input Data')
    @api.response(404, 'User not found')
    @api.doc(security="Bearer Auth")
    @jwt_required()
    def put(self, user_id):

        # Ensuring that the user is admin
        claims = get_jwt()
        is_admin = claims.get("is_admin", False)
        if not is_admin :
            return {'error': 'Admin privileges required'}, 403

        """change existing user"""
        from app import bcrypt
        user_data = api.payload
        current_user = get_jwt_identity()
        # Checking if the user is the one that be logged in
        if user_id != current_user:
            return {'error': 'Unauthorized action'}, 403
        # Checking if the user exist
        existing_user = facade.get_user(user_id)
        if not existing_user:
            return {'error': 'User not found'}, 404

        # Checking existence of the user's email
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
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
class AmenityList(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    @api.doc(security="Bearer Auth")
    @jwt_required()
    def post(self):
        # Ensuring that the user is admin
        claims = get_jwt()
        is_admin = claims.get("is_admin", False)
        if not is_admin :
            return {'error': 'Admin privileges required'}, 403

        """Register a new amenity"""
        amenity_data = api.payload
        try:
            new_amenity = facade.create_amenity(amenity_data)
        except:
            return {"error": "Invalid Input Data"}, 400
        return {
            'id': new_amenity.id,
            'name': new_amenity.name,
            'description': new_amenity.description
            }, 201

    """ 
    @api.response(200, 'List of amenities retrieved successfully')
    @api.response(404, 'Amenities not found')
    def get(self):
        Retrieve a list of all amenities
        amenities = facade.get_all_amenities()
        if not amenities:
            return {'error': 'Amenities not found'}, 404
        return amenities, 200
    """

@api.route('/amenities/<amenity_id>')
class AmenityResource(Resource):
    """
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        Get amenity details by ID
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return {
            'id': amenity.id,
            'name': amenity.name,
            'description': amenity.description,
            'places': amenity.places
            }, 200
    """

    @api.expect(amenity_model, validate=True)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    @api.doc(security="Bearer Auth")
    @jwt_required()
    def put(self, amenity_id):
         # Ensuring that the user is admin
        claims = get_jwt()
        is_admin = claims.get("is_admin", False)
        if not is_admin :
            return {'error': 'Admin privileges required'}, 403

        """Update an amenity's information"""
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

