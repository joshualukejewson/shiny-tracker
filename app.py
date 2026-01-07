""" 
Shiny tracker with Pokeapi integration, animated sprites,
pokemon search functionality and interactive GUI.
Made by Joshua Luke. 
"""

import requests
from flask import Flask, render_template, request
import poketrack

app = Flask(__name__)

"""
Index Route that loads the main page, takes pokemon search input and displays the pokemon to the screen.

@param: None
@return: flask.render_template() function.
"""
@app.route("/", methods=["GET", "POST"])
def index():

    pokemon_search = ""
    pokemon = None

    if request.method == "POST":
        pokemon_search = request.form.get('pokemon_search')
        if pokemon_search:
            pokemon = poketrack.fetch_pokemon_data(str(pokemon_search).lower())

    return render_template("index.html", pokemon=pokemon)

if __name__ == '__main__':
    app.run(debug=True)