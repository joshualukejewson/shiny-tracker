"""
Shiny tracker with Pokeapi integration, animated sprites,
pokemon search functionality and interactive GUI.
Made by Joshua Luke.
"""

import requests
from flask import Flask, render_template, request
import poketrack

app = Flask(__name__)
stored_pokemon = poketrack.retrieve_pokemon_data()

"""
Index Route that loads the main page, takes pokemon search input and displays the pokemon to the screen.

@param: None
@return: flask.render_template() function.
"""

@app.route("/", methods=["GET", "POST"])
def index():

    pokemon = None  # This is what we pass to the template

    if request.method == "POST":

        # --- SEARCH BUTTON ---
        if "search_btn" in request.form:
            pokemon_search = request.form.get("pokemon_search", "").strip().lower()
            if pokemon_search:
                # Fetch Pokémon if not already stored
                if pokemon_search not in stored_pokemon:
                    fetched_pokemon = poketrack.fetch_pokemon_data(pokemon_search, 0)
                    stored_pokemon[pokemon_search] = fetched_pokemon
                # Retrieve from dictionary for rendering
                pokemon = stored_pokemon[pokemon_search]
                poketrack.save_data(stored_pokemon)

        # --- INCREMENT BUTTON ---
        elif "increment_btn" in request.form:
            pokemon_name = request.form.get("pokemon_name", "").strip().lower()
            if pokemon_name and pokemon_name in stored_pokemon:
                pokemon = stored_pokemon[pokemon_name]
                pokemon.increment()
                poketrack.save_data(stored_pokemon)
            else:
                pokemon = None

        # --- RESET BUTTON ---
        elif "reset_btn" in request.form:
            pokemon_name = request.form.get("pokemon_name", "").strip().lower()
            if pokemon_name and pokemon_name in stored_pokemon:
                pokemon = stored_pokemon[pokemon_name]
                pokemon.reset_count()
                poketrack.save_data(stored_pokemon)
            else:
                pokemon = None


    return render_template("index.html", pokemon=pokemon)

if __name__ == "__main__":
    app.run(debug=True)
