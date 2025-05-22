from flask import Flask, render_template, abort
import requests


app = Flask(__name__)


# Home page route
@app.route("/")
def index():
    response = requests.get("http://minecraft-ids.grahamedgecombe.com/items.json")
    data = response.json()
  
    items = []
    for item in data:
        id = item['type']
        name = item['name'].capitalize()
        
        


        image_data = requests.get(f"http://yanwittmann.de/api/mcdata/item.php?name={name}").json()
        items_list = image_data.get('items', [])
        if items_list:
            image_url = items_list[0].get('image', "static/nothing-10-5523.gif")
        else:
            image_url = "static/nothing-10-5523.gif"






        items.append({
            'name': name,
            'id': id,
            'image': image_url
        })
    print("items:", items)


    return render_template("index.html", items=items)



# # Pokémon detail page route
@app.route("/item/<int:id>")
def item_detail(id):
    response = requests.get(f"http://minecraft-ids.grahamedgecombe.com/items.json")
    data = response.json()


    try:
       item =next(item for item in data if item['type'] == id)
    except StopIteration:
       abort(404)


    name = item['name'].capitalize()

    mc_identifier = f"minecraft:{name.replace(' ', '_').lower()}"
    detail_response = requests.get(f"http://yanwittmann.de/api/mcdata/itemorblock.php?identifier={mc_identifier}")

    detail_data = detail_response.json()
    describtion = detail_data.get("describtion", "No describtion avaliable.")
    image_data = requests.get(f"http://yanwittmann.de/api/mcdata/item.php?name={name}").json()
    image_url = image_data['items'][0]['image'] if image_data['count'] > 0 else "/static/img/placeholder.png"


    return render_template("item.html", item={
           'name': name,
           'id' : id,
           'describtion' : describtion,
           'image' : image_url

        },
        
    )

if __name__ == '__main__':
    app.run(debug=True)


