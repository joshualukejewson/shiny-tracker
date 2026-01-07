import requests

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