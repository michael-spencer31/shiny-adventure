import requests
import random
from flask import Flask
import openai

messages = [ {"role": "system", "content": "You are a intelligent assistant."} ]

STARTER = 400
LEGEND = 600

app = Flask(__name__)

# Initialize the user's team
user_team = []


def battle():
    female_class = ["Air Hostess", "Ballerina", "Bride", "Bridesmaid", "Maid", "Model", "Nurse", "Princess", "Therapist", "Waitress"]
    female_names = ["Caitlin", "Emma", "Kenzie", "Shawne", "Sierra", "Victoria", "Megan", "Jordyn", "Violet"]
    selected_class = random.choice(female_class)
    selected_name = random.choice(female_names)
    trainer = selected_class + " " + selected_name
    print(trainer + " would like to battle!")

def get_starter_pokemon():
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
    print("Please choose your starter Pokémon by typing the number corresponding to the Pokémon:")
    for index, pokemon in enumerate(starter_pokemon, start=1):
        print(f"{index}: {pokemon}")

    user_choice = int(input("Enter the number of your choice: ")) - 1
    while True:
        if 0 <= user_choice < 3:
            chosen_pokemon = starter_pokemon[user_choice]
            user_team.append(chosen_pokemon)
            print(f"You have chosen: {chosen_pokemon}")
            break
        else:
            print("Invalid choice. Please try again")
            user_choice = int(input("Enter the number of your choice: ")) - 1

    return user_choice

starter_pokemon = get_starter_pokemon()



# Print the user's team
print("Your team:", user_team)
battle()

# Uncomment the following lines if you want to run this code as a Flask application
# if __name__ == '__main__':
#     app.run()
