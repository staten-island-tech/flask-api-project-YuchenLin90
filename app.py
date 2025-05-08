from flask import Flask, render_template
import requests
import json

app = Flask(__name__)

# Home page route
@app.route("/")
def index():
    response = requests.get("https://www.dnd5eapi.co/api/2014/ability-scores/cha")  
    pokemon_list = data['results']
    print(data)

    pokemons = []
    for pokemon in pokemon_list:
        url = pokemon['url']
        parts = url.strip("/").split("/")
        id = parts[-1]
        image_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{id}.png"

        pokemons.append({
            'name': pokemon['name'].capitalize(),
            'id': id,
            'image': image_url
        })

    return render_template("index.html", pokemons=pokemons)

# Pokémon detail page route
@app.route("/pokemon/<int:id>")
def pokemon_detail(id):
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{id}")
    data = response.json()

    types = [t['type']['name'] for t in data['types']]
    height = data.get('height')
    weight = data.get('weight')
    name = data.get('name').capitalize()
    image_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{id}.png"

    stat_names = [stat['stat']['name'].capitalize() for stat in data['stats']]
    stat_values = [stat['base_stat'] for stat in data['stats']]

    # Convert to JS-friendly strings
    stat_names_str = json.dumps(stat_names)
    stat_values_str = json.dumps(stat_values)

    return render_template("pokemon.html",
        pokemon={
            'name': name,
            'id': id,
            'image': image_url,
            'types': types,
            'height': height,
            'weight': weight
        },
        stat_names_str=stat_names_str,
        stat_values_str=stat_values_str
    )

if __name__ == '__main__':
    app.run(debug=True)
