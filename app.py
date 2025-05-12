from flask import Flask, render_template
import requests
import json

app = Flask(__name__)

# Home page route
@app.route("/")
def index():
    response = requests.get("http://minecraft-ids.grahamedgecombe.com/items.json")  
    data = response.json()
    item_list = data.get('results', [])


    items = []
    for item in item_list:
        url = item['url']
        parts = url.strip("/").split("/")
        id = parts[-1]
        image_url = f"http://minecraft-ids.grahamedgecombe.com/items.zip{id}.png"

        items.append({
            'name': item['name'].capitalize(),
            'id': id,
            'image': image_url
        })

    return render_template("index.html", items=items)

# Pokémon detail page route
@app.route("/item/<int:id>")
def item_detail(id):
    response = requests.get(f"https://github.com/SpockBotMC/python-minecraft-data/{id}")
    data = response.json()

    types = [t['type']['name'] for t in data['types']]
    height = data.get('height')
    weight = data.get('weight')
    name = data.get('name').capitalize()
    image_url = f"http://minecraft-ids.grahamedgecombe.com/items.zip{id}.png"

    stat_names = [stat['stat']['name'].capitalize() for stat in data['stats']]
    stat_values = [stat['base_stat'] for stat in data['stats']]

    # Convert to JS-friendly strings
    stat_names_str = json.dumps(stat_names)
    stat_values_str = json.dumps(stat_values)

    return render_template("item.html",
        item={
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
