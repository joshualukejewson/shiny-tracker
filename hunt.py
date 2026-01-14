from user import db

CONST_DEFAULT_ENCOUNTERS = 0
CONST_DEFAULT_ODDS = 4096


class Hunt(db.Model):

    __tablename__ = "huntdetails"
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    pokemon_id = db.Column(
        db.Integer, db.ForeignKey("userpokemon.id_no"), nullable=False
    )
    hunt_id = db.Column(db.Integer, primary_key=True, nullable=False)
    method = db.Column(db.String(15))
    shiny_charm = db.Column(db.Boolean, nullable=False, default=False)
    encounters = db.Column(db.Integer, nullable=False, default=CONST_DEFAULT_ENCOUNTERS)
    is_completed = db.Column(db.Boolean, nullable=False, default=False)

    def increment(self):
        self.encounters += 1

    def get_count(self):
        return self.encounters

    def reset_count(self):
        self.encounters = CONST_DEFAULT_ENCOUNTERS


def setup_hunt(user_id: int, pokemon_id: int):
    return {
        "user_id": user_id,
        "pokemon_id": pokemon_id,
    }
