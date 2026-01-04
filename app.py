# shiny tracker with PokiApi integration, animated sprites,
# pokemon search functionality and interactive GUI.
# Made by Joshua Luke.

import requests
from flask import Flask, render_template_string

app = Flask(__name__)

class Pokemon:
    def __init__(self, name : str, sprite : str):
        self.name = name
        self.sprite = sprite

    def __str__(self):
        return f"{self.name} - {self.sprite}"
    
def fetch_pokemon_data(pokemon_name : str) -> Pokemon:
    url = "https://pokeapi.co/api/v2/pokemon/{name}".format(name = pokemon_name)
    print(url)
    response = requests.get(url)
    raw_data = response.json()

    return Pokemon(raw_data["name"].capitalize(), raw_data["sprites"]["front_shiny"] )

@app.route("/")
def home():
    pokemon = fetch_pokemon_data("bulbasaur")
    return render_template_string("""
        <h1>{{ pokemon.name }}</h1>
        <img src="{{ pokemon.sprite }}">
        """, pokemon=pokemon)

if __name__ == '__main__':
    app.run(debug=True)