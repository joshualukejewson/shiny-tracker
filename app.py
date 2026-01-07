""" 
shiny tracker with PokiApi integration, animated sprites,
pokemon search functionality and interactive GUI.
Made by Joshua Luke. 
"""

import requests
from flask import Flask, render_template, request

app = Flask(__name__)

class Pokemon: 
    def __init__(self, name : str, sprite : str, shiny: str):
        self.name = name
        self.sprite = sprite
        self.shimy = shiny
        self.count = 0

    def increment(self):
        self.count += 1

    def get_count(self):
        return self.count
    
    def reser_count(self):
        self.count = 0
        
    def __str__(self):
        return f"{self.name} - {self.sprite}"
    
def fetch_pokemon_data(pokemon_name : str) -> Pokemon:
    url = "https://pokeapi.co/api/v2/pokemon/{name}".format(name = pokemon_name)
    print(url)
    response = requests.get(url)
    raw_data = response.json()

    return Pokemon(raw_data["name"].capitalize(), raw_data["sprites"]["front_default"], raw_data["sprites"]["front_shiny"])

@app.route("/", methods=["GET", "POST"])
def index():

    pokemon_search = ""
    pokemon = None
    if request.method == "POST":
        pokemon_search = request.form.get('pokemon_search')
        if pokemon_search:
            pokemon = fetch_pokemon_data(str(pokemon_search).lower())
    return render_template("index.html", pokemon=pokemon)

if __name__ == '__main__':
    app.run(debug=True)