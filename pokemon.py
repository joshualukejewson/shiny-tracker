import requests
from user import db
from flask_sqlalchemy import SQLAlchemy


class Pokemon(db.Model):

    __tablename__ = "userpokemon"
    name = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    id_no = db.Column(db.Integer, primary_key=True, nullable=False)
    default_sprite = db.Column(db.String(100), nullable=False)
    shiny_sprite = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {
            "name": self.name,
            "sprite": self.default_sprite,
            "sprite_shiny": self.shiny_sprite,
        }


def fetch_pokemon_data(user_id: int, pokemon_name: str) -> Pokemon | None:
    url = "https://pokeapi.co/api/v2/pokemon/{name}".format(name=pokemon_name)
    response = requests.get(url)
    if response.status_code == 404:
        return None
    raw_data = response.json()

    front_default = ""
    front_shiny = ""

    if raw_data["sprites"]["other"]["showdown"]["front_default"]:
        front_default = raw_data["sprites"]["other"]["showdown"]["front_default"]
    else:
        front_default = raw_data["sprites"]["front_default"]

    if raw_data["sprites"]["other"]["showdown"]["front_shiny"]:
        front_shiny = raw_data["sprites"]["other"]["showdown"]["front_shiny"]
    else:
        front_shiny = raw_data["sprites"]["front_shiny"]

    return Pokemon(
        name=pokemon_name,  # type: ignore
        user_id=user_id,  # type: ignore
        default_sprite=front_default,  # type: ignore
        shiny_sprite=front_shiny,  # type: ignore
    )


def add_pokemon_for_user(user_id, pokemon_name) -> Pokemon | None:
    existing = Pokemon.query.filter_by(user_id=user_id, name=pokemon_name).first()
    if existing:
        return existing
    else:
        pokemon = fetch_pokemon_data(user_id, pokemon_name)
        if pokemon:
            db.session.add(pokemon)
            db.session.commit()
            return pokemon
        else:
            return None
