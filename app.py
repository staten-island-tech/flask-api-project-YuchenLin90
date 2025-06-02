from flask import Flask, render_template, request
import requests


app = Flask(__name__)

# Home page route
@app.route("/")
def index():
    search = request.args.get("search", "").strip().lower()
    response = requests.get("http://yanwittmann.de/api/mcdata/item.php")
    data = response.json()

    item_data = data.get("items", [])
  
    items = []
    for item in item_data:

        name_raw = item.get("name")
        name_display = name_raw.replace("_", " ").title()

        if search and search not in name_raw.lower():
            continue

        image_url = item.get('image')
        if not image_url:
            image_url =  f"https://www.minecraftitemids.com/item/32/{name_raw}.png"
        
        


        items.append({
            'name_display': name_display,
            'name_raw' : name_raw,
            'image': image_url
        })
   


    return render_template("index.html", items=items, search=search)



#  detail page route
@app.route("/item/<name>")
def item_detail(name):




    # item = next((item for item in data if item['name'].lower() == name.lower()), None)
    # if not item:
    #     abort(404, description="Item not found.")

    name = name.strip().lower()
 

    try:
        response = requests.get(f"http://yanwittmann.de/api/mcdata/item.php?name={name}")
        response.raise_for_status()
        data = response.json()
    except requests.RequestException :
        print("Error, cannot connect")
        
    items = data.get("items", [])
    if not items:
        print("Error, no item")

    item = items[0]

    name_display = item.get("name", "").replace("_", " ").title()
    description = item.get("description", "no description available")

    image_url = item.get("image")
    if not image_url:
        image_url = f"https://www.minecraftitemids.com/item/32/{name}.png"


    return render_template("detail.html", item={
        'name_display': name_display,
   

        'image': image_url,
        'description': description
            })






if __name__ == '__main__':
    app.run(debug=True)

