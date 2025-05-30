from flask import Flask, render_template, abort, request
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

        image_url = None
        try:
            first_api_response = requests.get(f"http://yanwittmann.de/api/mcdata/item.php?name={name_raw}").json()
            items_list=first_api_response.get("items", [])
            if items_list and items_list[0].get("image"):
                image_url = items_list[0]["image"]
        except Exception:
            pass
        if not image_url:
            image_url = f"https://www.minecraftitemids.com/item/32/{name_raw}.png"
        
        


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

    name_raw = name.lower()
    name_display = name_raw.replace("_", " ").title()
 

    try:
        detail_response = requests.get(f"http://yanwittmann.de/api/mcdata/itemorblock.php?name={name_raw}")
        detail_response.raise_for_status()
        detail_data = detail_response.json()
        description = detail_data.get("description", "No description available.")
    except Exception :
        print(f"Failed to get describtion for {name_raw}")
        description = "No description available."

    image_url = None
    try:
        first_api_response = requests.get(f"http://yanwittmann.de/api/mcdata/item.php?name={name_raw}").json()
        items_list = first_api_response.get("items", [])
        if items_list and items_list[0].get("image"):
            image_url = items_list[0]["image"]
    except Exception:
        pass
    if not image_url:
        image_url = f"https://www.minecraftitemids.com/item/32/{name_raw}.png"


    return render_template("item.html", item={
        'name_display': name_display,
        'name_raw': name_raw,

        'image': image_url,
        'description': description
            })








if __name__ == '__main__':
    app.run(debug=True)

