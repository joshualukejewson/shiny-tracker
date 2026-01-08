import requests


class Pokemon:
    def __init__(self, name: str, sprite: str, shiny: str, count: int):
        self.name = name
        self.sprite = sprite
        self.sprite_shiny = shiny
        self.count = count
        self.shiny = False

    def increment(self):
        self.count += 1

    def get_count(self):
        return self.count

    def reset_count(self):
        self.count = 0

    def __str__(self):
        return f"{self.name} - {self.sprite}"


def fetch_pokemon_data(pokemon_name: str, count: int) -> Pokemon:
    url = "https://pokeapi.co/api/v2/pokemon/{name}".format(name=pokemon_name)
    response = requests.get(url)
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
        raw_data["name"].lower(),
        front_default,
        front_shiny,
        count,
    )

def save_data(stored_pokemon):
    file_path = "static/storedPokemon.txt"

    with open(file_path, "w") as file:
        for pokemon in stored_pokemon.values():
            file.write("{name},{count}\n".format(name = pokemon.name, count=pokemon.count))


"""
retrieve_pokemon_data(): is run at the beggining of app launch, creates a stored txt file if it doesnt exist
and reads the data from the file and stores it in a dictionary.

@param: None
@return: Dictionary[str, Pokemon]
"""
def retrieve_pokemon_data():

    stored_pokemon = {}
    file_path = "static/storedPokemon.txt"
    
    # see if file exists, if it doesn't create one and if it does open it and read the saved pokemon data.
    try:
        with open(file_path, "x") as file:
            pass
    except FileExistsError:
        with open(file_path, "r") as file:
            for line in file:
                pokemon_name, encounters = line.split(",")
                stored_pokemon[pokemon_name] = fetch_pokemon_data(pokemon_name, int(encounters))

    return stored_pokemon

