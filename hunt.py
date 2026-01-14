from user import db
from enum import Enum


# Hunt method options.
class HuntMethods(Enum):
    CHAIN = "chain"
    MASUDA = "masuda"
    SOFT_RESET = "soft-reset"
    SOS = "sos"
    RAND = "random-encounter"


CONST_DEFAULT_ENCOUNTERS = 0
CONST_DEFAULT_ODDS = 4096


class Hunt(db.Model):

    __tablename__ = "huntdetails"
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    pokemon_id = db.Column(
        db.Integer, db.ForeignKey("userpokemon.id_no"), nullable=False
    )
    hunt_id = db.Column(db.Integer, primary_key=True, nullable=False)
    method = db.Column(db.String(15), default=HuntMethods.SOFT_RESET.value)
    shiny_charm = db.Column(db.Boolean, nullable=False, default=False)
    encounters = db.Column(db.Integer, nullable=False, default=CONST_DEFAULT_ENCOUNTERS)
    is_completed = db.Column(db.Boolean, nullable=False, default=False)

    def increment(self):
        self.encounters += 1

    def get_count(self):
        return self.encounters

    def reset_count(self):
        self.encounters = CONST_DEFAULT_ENCOUNTERS

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "pokemon_id": self.pokemon_id,
            "method": self.method,
            "shiny_charm": self.shiny_charm,
            "encounters": self.encounters,
            "is_completed": self.is_completed,
        }


def add_hunt_for_user(user_id, pokemon_id):
    existing_hunt = Hunt.query.filter_by(user_id=user_id, pokemon_id=pokemon_id).first()
    if existing_hunt:
        return existing_hunt
    else:
        hunt_details = Hunt(user_id=user_id, pokemon_id=pokemon_id)  # type: ignore
        db.session.add(hunt_details)
        db.session.commit()
        return hunt_details
