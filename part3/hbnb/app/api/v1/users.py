from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt


api = Namespace('users', description='User operations')


# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user'),
    'is_admin': fields.Boolean(required=True, description='Administrator privilege')
})


@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created') 
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""

        # Get input data
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

    @api.response(200, 'Users details retrieved successfully')
    @api.response(404, 'Users not found')
    def get(self):
        """Get users"""
        users = facade.get_all_users()
        if not users:   
            return {'error': 'Users not found'}, 404
        return users, 200


@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'password': user.password
            }, 200


    @api.expect(user_model, validate=True)
    @api.response(200, 'User details retrieved successfully')
    @api.response(400, 'Invalid Input Data')
    @api.response(404, 'User not found')
    @api.doc(security="Bearer Auth")
    @jwt_required()
    def put(self, user_id):
        """change existing user"""
        from app import bcrypt

        # Get input data
        user_data = api.payload
        current_user = get_jwt_identity()

        # Checking if the user is the one that be logged in
        if user_id != current_user:
            return {'error': 'Unauthorized action'}, 403

        # Checking if the user exist
        existing_user = facade.get_user(user_id)
        if not existing_user:
            return {'error': 'User not found'}, 404
        
        claims = get_jwt()
        is_admin = claims.get("is_admin", False)

        # Ensuring that the user don't modify his email
        if not is_admin and existing_user.email != user_data["email"]:
            return {'error': 'You cannot modify email or password'}, 400

        # Ensuring that the user don't modify his password
        if not is_admin and not (bcrypt.check_password_hash(existing_user.password, user_data["password"])):
            return {'error': 'You cannot modify email or password'}, 400
        
        # Checking existence of the user's email
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user and existing_user["id"] != user_id:
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


@api.route('/mail/<user_mail>')
class UserResource(Resource): 
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    @api.doc(security="Bearer Auth")
    def get(self, user_mail):
        """Get user details by email"""
        user = facade.get_user_by_email(user_mail)
        if not user:
            return {'error': 'User not found'}, 404
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'password': user.password
            }, 200

