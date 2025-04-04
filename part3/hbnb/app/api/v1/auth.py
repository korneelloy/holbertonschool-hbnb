from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_cors import cross_origin  # Import cross_origin for per-route CORS control
from flask import make_response, jsonify



api = Namespace('auth', description='Authentication operations')

# Model for input validation
login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

@api.route('/login', methods=['POST', 'OPTIONS'])
class Login(Resource):
    @api.expect(login_model)
    @cross_origin(origins="http://localhost:8000", allow_credentials=True)  # Allow CORS on POST
    def post(self):
        """Authenticate user and return a JWT token"""
        credentials = api.payload  
        user = facade.get_user_by_email(credentials['email'])
        if not user or not user.verify_password(credentials['password']):
            response = make_response(jsonify({'error': 'Invalid credentials'}), 401)
            response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
            response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
            response.headers.add("Access-Control-Allow-Credentials", "true")
            return response
        
        access_token = create_access_token(identity=str(user.id), additional_claims={'is_admin': user.is_admin})
        response = make_response(jsonify({'access_token': access_token}), 200)
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
        response.headers.add("Access-Control-Allow-Credentials", "true")
        return response

    def options(self):
        """Handles CORS preflight requests"""
        response = make_response("", 204)
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
        return response

@api.route('/protected')
class ProtectedResource(Resource):
    @jwt_required()
    @cross_origin(origins="http://localhost:8000", allow_credentials=True)  # Allow CORS for this route
    def get(self):
        """A protected endpoint that requires a valid JWT token"""
        current_user = get_jwt_identity()  # Retrieve the user's identity from the token
        return {'message': f'Hello, user {current_user}'}, 200