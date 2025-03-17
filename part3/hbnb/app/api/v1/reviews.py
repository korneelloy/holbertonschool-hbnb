from flask_restx import Namespace, Resource, fields
from app.services import facade
from app.models.place import Place
from app.models.user import User
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import text
from app import db

api = Namespace('reviews', description='Review operations')

"""Define the review model for input validation and documentation"""
review_model = api.model('Review', {
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'comment': fields.String(required=True, description='Text of the review'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})


@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model, validate=True)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Unauthorized')
    @api.doc(security="Bearer Auth")
    @jwt_required()
    def post(self):
        """Register a new review"""

        # Get input data
        review_data = api.payload

        # Ensuring that the user exist
        if facade.get_user(review_data['user_id']) is None:
            return {"error": "Invalid Input Data"}, 400

        current_user = get_jwt_identity()

        # Ensuring that the user is logged in to post a review
        if review_data['user_id'] != current_user:
            return {'error': 'Unauthorized action, you must be logged in to review a place'}, 403

        # Ensuring that the place exist
        if facade.get_place(review_data['place_id']) is None:
            return {"error": "Invalid Input Data"}, 400

        # Ensuring that the user do not post multiple review on a place
        reviews = facade.get_reviews_by_place(review_data['place_id'])
        if reviews != []:
            for review in reviews:
                if review['user_id'] == current_user:
                    return {'error': 'Unauthorized action, you have already reviewed this place'}, 400
        var_place = facade.get_place(review_data['place_id'])
        var_user = facade.get_user(review_data['user_id'])
        owner_id = var_place.owner_id
        owner_id_in_review_data = review_data['user_id']

        # Ensuring that review belongs to a place the user does not own
        if owner_id == owner_id_in_review_data:
            return {"error": "You cannot review your own place"}, 400

        # Creating the review
        try:
            new_review = facade.create_review(review_data)
        except:
            return {"error": "Invalid Input Data"}, 400

        return {
            'id': new_review.id,
            'rating': new_review.rating,
            'comment': new_review.comment,
            'user_id': new_review.user_id,
            'place_id': new_review.place_id
            }, 201
    

    @api.response(200, 'List of reviews retrieved successfully')
    @api.response(404, 'Reviews not found')
    def get(self):
        """Retrieve a list of all reviews"""
        reviews = facade.get_all_reviews()
        if not reviews:   
            return {'error': 'Reviews not found'}, 404
        return reviews, 200


@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return {
            'id': review.id,
            'rating': review.rating,
            'comment': review.comment,
            'user_id': review.user_id,
            'place_id': review.place_id
            }, 200


    @api.expect(review_model, validate=True)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    @api.doc(security="Bearer Auth")
    @jwt_required()
    def put(self, review_id):
        """Update a review's information"""
        review_data = api.payload
        current_user = get_jwt_identity()

        # Ensuring that the user exist
        if facade.get_user(review_data['user_id']) is None:
            return {"error": "Invalid Input Data"}, 400

        # Verifying if the user that reviewing the place is not the owner of that place
        if review_data['user_id'] != current_user:
            return {'error': 'Unauthorized action'}, 403

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
        current_user = get_jwt_identity()

        # Ensuring that the targeted review exist
        try:
            review = facade.get_review(review_id)
        except:
            return {"error": "Not found"}, 404

        # Ensuring that the user is the owner of the review before deleting it
        if review.user_id != current_user:
            return {'error': 'Unauthorized action'}, 403

        facade.delete_review(review_id)

        return {"message": "Review deleted successfully"}, 200


@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""

        # Ensuring that the place exist
        try:
            facade.get_place(place_id)
        except:
            return {'error': 'Place not found'}, 404

        # Getting the review
        reviews = facade.get_reviews_by_place(place_id)
        if not reviews:
            return {'error': 'Reviews not found'}, 404
        return reviews, 200
