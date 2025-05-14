from flask import Flask, render_template
import requests


app = Flask(__name__)

# Home page route
@app.route("/")
def index():
    response = requests.get("http://minecraft-ids.grahamedgecombe.com/items.json")  
    data = response.json()
    print(data)



    items = []
    for item in data:
        id = item['type']
        name = item['name'].capitalize()

        image_data = requests.get(f"http://yanwittmann.de/api/mcdata/item.php?name={name}").json()
        image_url = image_data['item'][0]['image'] if image_data['count'] > 0 else "/static/img/placeholder.png"
        items.append({
            'name': name,
            'id': id,
            'image': image_url
        })

    return render_template("index.html", items=items)

# Pokémon detail page route
@app.route("/item/<int:id>")
def item_detail(id):
    response = requests.get(f"http://minecraft-ids.grahamedgecombe.com/items.json")
    data = response.json()

    try:
        item =next(item for item in data if item['type'] == id)
    except IndexError:
        print('404')
    except StopIteration:
        print('404')

    name = item['name'].capitalized()
    type_name = item.get('type', 'unknown').capitalize()
    image_data = requests.get(f"http://yanwittmann.de/api/mcdata/item.php?name={name}").json()
    image_url = image_data['items'][0]['image'] if image_data['count'] > 0 else "/static/img/placeholder.png"

    return render_template("item.html", item={
            'name': name, 
            'id' : id, 
            'type' : type_name, 
            'image' : image_url

        },
    )

if __name__ == '__main__':
    app.run(debug=True)
