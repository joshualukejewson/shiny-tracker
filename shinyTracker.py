# shiny tracker with PokiApi integration, animated sprites,
# pokemon search functionality and interactive GUI.
# Made by Joshua Luke.

import requests
from PIL import Image

class Pokemon:
    def __init__(self, name, sprite):
        self.name = name
        self.sprite = sprite

    def __str__(self):
        return f"{self.name} - {self.sprite}"
    
def fetch_pokemon_data(pokemon_name):
    url = "https://pokeapi.co/api/v2/pokemon/{name}".format(name = pokemon_name)
    print(url)
    response = requests.get(url)
    raw_data = response.json()

    target_pokemon = Pokemon(raw_data["name"], raw_data["sprites"]["front_shiny"] )

    #print(target_pokemon)

def main():
    fetch_pokemon_data("bulbasaur")

if __name__ == '__main__':
    main()