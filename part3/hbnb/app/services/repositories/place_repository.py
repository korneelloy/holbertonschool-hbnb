from app.persistence.repository import SQLAlchemyRepository

class PlaceRepository(SQLAlchemyRepository):
    def __init__(self, model):
        super().__init__(model)

    def create_place(self, place_data):
        place = Place(**place_data)
        self.place_repo.add(place)
        return place
