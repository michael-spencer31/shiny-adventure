import requests
import random
from flask import Flask
import math, csv

class move:
    def __init__(self, name, power, move_type, attack_type):
        self.name = name
        self.power = power
        self.move_type = move_type 
        self.attack_type = attack_type

        def __str__(self):
            return (f"Name: {self.name}\n"
                    f"Power: {self.power}\n"
                    f"Move type: {self.move_type}\n"
                    f"Attack type: {self.attack_type}")
class Pokemon:
    def __init__(self, id, level, name, hp, attack, defense, special_attack, special_defense, speed, type, attack_one=None, attack_two=None, attack_three=None, attack_four=None):
        self.name = name
        self.id = id
        self.level = level
        self.hp = hp
        self.attack = attack
        self.defense = defense 
        self.special_attack = special_attack
        self.special_defense = special_defense
        self.speed = speed
        self.type = type
        self.attack_one = attack_one
        self.attack_two = attack_two
        self.attack_three = attack_three
        self.attack_four = attack_four

    def __str__(self):
        return (f"Pokemon ID: {self.id}\n"
                f"Name: {self.name}\n"
                f"Level: {self.level}\n"
                f"HP: {self.hp}\n"
                f"Attack: {self.attack}\n"
                f"Defense: {self.defense}\n"
                f"Special Attack: {self.special_attack}\n"
                f"Special Defense: {self.special_defense}\n"
                f"Speed: {self.speed}\n"
                f"Type: {self.type}\n"
                f"Attack: {self.attack_one}\n"
                f"Attack: {self.attack_two}\n"
                f"Attack: {self.attack_three}\n"
                f"Attack: {self.attack_four}")
    def get_attack(self):
        return self.attack
    
    def get_type(self):
        return self.type


messages = [ {"role": "system", "content": "You are a intelligent assistant."} ]

STARTER = 400
LEGEND = 600

app = Flask(__name__)

# Initialize the user's team
user_team = []

def get_stats(name, level):

    url = f"https://pokeapi.co/api/v2/pokemon/{name}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        # base/100 * base + level
        m = move("Ember", 40, "Fire", "Special")

        id = data["id"]
        hp = math.ceil(data["stats"][0]["base_stat"] / 1000 * data["stats"][0]["base_stat"] + level + 10)
        attack = math.ceil(data["stats"][1]["base_stat"] / 1000 * data["stats"][1]["base_stat"] + level)
        defense = math.ceil(data["stats"][2]["base_stat"] / 1000 * data["stats"][2]["base_stat"] + level)
        special_attack = math.ceil(data["stats"][3]["base_stat"] / 1000 * data["stats"][3]["base_stat"] + level)
        special_defense = math.ceil(data["stats"][4]["base_stat"] / 1000 * data["stats"][4]["base_stat"] + level)
        speed = math.ceil(data["stats"][5]["base_stat"] / 1000 * data["stats"][5]["base_stat"] + level)
        p = Pokemon(id, level, name.capitalize(), hp, attack, defense, special_attack, special_defense, speed, "Water", m)
        return p
    else:
        print(f"Error: Unable to fetch data for Pokémon '{name}' (status code: {response.status_code})")


def battle():
    female_class = ["Air Hostess", "Ballerina", "Bride", "Bridesmaid", "Maid", "Model", "Nurse", "Princess", "Therapist", "Waitress"]
    female_names = ["Caitlin", "Emma", "Kenzie", "Shawne", "Sierra", "Victoria", "Megan", "Jordyn", "Violet"]
    selected_class = random.choice(female_class)
    selected_name = random.choice(female_names)
    trainer = selected_class + " " + selected_name
    print(trainer + " would like to battle!")

def get_pokemon(type):
    species_url = 'https://pokeapi.co/api/v2/pokemon-species/?limit=10000'
    base_url = "https://pokeapi.co/api/v2/pokemon/"

    species_response = requests.get(species_url)
    species_data = species_response.json()['results']

    starter_pokemon = []
    while len(starter_pokemon) < 3:
        random_number = random.randint(1, len(species_data))
        response = requests.get(f"{base_url}{random_number}")

        if response.status_code == 200:
            pokemon_data = response.json()
            base_stats = pokemon_data['stats']
            base_stat_total = sum(stat['base_stat'] for stat in base_stats)

            if base_stat_total > STARTER:
                continue

            pokemon_name = pokemon_data['name']
            starter_pokemon.append(pokemon_name.capitalize())
        else:
            print(f"Failed to retrieve data for Pokémon number {random_number}")
    
    # Prompt the user to pick a Pokémon
    print(f"Please choose your {type} Pokémon by typing the number corresponding to the Pokémon:")
    for index, pokemon in enumerate(starter_pokemon, start=1):
        print(f"{index}: {pokemon}")

    user_choice = int(input("Enter the number of your choice: ")) - 1
    while True:
        if 0 <= user_choice < 3:
            chosen_pokemon = starter_pokemon[user_choice]
            user_team.append(chosen_pokemon)
            print(f"You have chosen: {chosen_pokemon}")
            p = get_stats(chosen_pokemon.lower(), 50)
            return p
        else:
            print("Invalid choice. Please try again")
            user_choice = int(input("Enter the number of your choice: ")) - 1


user_pokemon = []
user_pokemon.append(get_pokemon("starter"))


print(user_pokemon[0])
# get_stats(party_pokemon)
# party_pokemon = get_pokemon("next")

pokemon_type = str(user_pokemon[0].get_type())

# Print the user's team
print("Your team:", user_team)
battle()

moves_learned = 0
with open('moves.csv', 'r') as file:
    reader = csv.reader(file)

    header = next(reader)
    print("Header (keys): " , header)

    for row in reader:
        print(row)
    
    
# Uncomment the following lines if you want to run this code as a Flask application
# if __name__ == '__main__':
#     app.run()
