from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
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
    def post(self):
        """Register a new review"""
        review_data = api.payload
        try:
            print (review_data)
            new_review = facade.create_review(review_data)
        except:
            return "Invalid Input Data", 400
        return {'id': new_review.id, 'rating': new_review.rating, 'comment': new_review.comment, 'user_id': new_review.user_id, 'place_id': new_review.place_id}, 201
    

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
        return {'id': review.id, 'rating': review.rating, 'comment': review.comment, 'user_id': review.user_id, 'place_id': review.place_id}, 200

    @api.expect(review_model, validate=True)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review's information"""
        review_data = api.payload
        # Simulate email uniqueness check (to be replaced by real validation with persistence)
        existing_review = facade.get_review(review_id)
        if not existing_review:
            return {'error': 'Review not found'}, 404
        try:
            updated_review = facade.update_review(review_id, review_data)
        except:
            return "Invalid Input Data", 400
        return {'id': review_id, 'rating': updated_review.rating, 'comment': updated_review.comment, 'user_id': updated_review.user_id, 'place_id': updated_review.place_id}, 201


    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        # Placeholder for the logic to delete a review
        pass

@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        try:
            facade.get_place_id(place_id)
        except:
            return {'error': 'Place not found'}, 404
        reviews = facade.get_reviews_by_place(place_id)
        if not reviews:
            return {'error': 'Reviews not found'}, 404
        return reviews, 200
