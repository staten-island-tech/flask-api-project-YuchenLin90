from flask import Flask, render_template, abort
import requests


app = Flask(__name__)



import requests
from requests.exceptions import ConnectionError, HTTPError

try:
    response = requests.get("http://minecraft-ids.grahamedgecombe.com/items.json", timeout=5)
    response.raise_for_status()  # Raises HTTPError for bad HTTP status codes
    data = response.json()
except ConnectionError:
    print("Could not connect to the API server.")
    data = []  # fallback or empty data
except HTTPError as e:
    print(f"HTTP error occurred: {e}")
    data = []
except requests.Timeout:
    print("The request timed out.")
    data = []





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
    identifier = item['text_type']  



    detail_response = requests.get(f"http://yanwittmann.de/api/mcdata/itemorblock")
    try:
        detail_data = detail_response.json()
        description = detail_data.get("description", "No description avaliable.")
    except requests.exceptions.JSONDecodeError:
        description = "No description availble."
        
        
        image_data = requests.get(f"http://yanwittmann.de/api/mcdata/item.php?name={name}").json()
        image_url = image_data['items'][0]['image'] if image_data['count'] > 0 else "/static/img/placeholder.png"


    return render_template("item.html", item={
           'name': name,
           'id' : id,
           'description' : description,
           'image' : image_url

        },
        
    )



@app.route('/search')
def search():
    find = requests.args.get('search', '').lower()

    response = requests.get(f"http://minecraft-ids.grahamedgecombe.com/items.json")
    data = response.json()

    items = []
    for item in data:
        name = item['name']
        if find == find:
            continue
        else:
            abort('item not found')

        item_id = item['type']
        name_cap = name.capitalize()

        image_data = requests.get(f"http://yanwittmann.de/api/mcdata/item.php?name={name_cap}").json()
        items_list = image_data.get('items', [])
        image_url = items_list[0].get('image', "static/nothing-10-5523.gif") if items_list else "static/nothing-10-5523.gif"

        items.append({
            'name': name_cap,
            'id': item_id,
            'image': image_url
        })

        break
    



    return render_template('templates/search.html')

if __name__ == '__main__':
    app.run(debug=True)


