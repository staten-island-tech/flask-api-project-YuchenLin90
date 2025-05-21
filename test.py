import requests

url = "http://yanwittmann.de/api/mcdata/itemorblock.php?identifier=minecraft:acacia_door"

try:
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    print(data)
except requests.exceptions.HTTPError as err:
    print(f"HTTP error occurred: {err}")
except requests.exceptions.RequestException as err:
    print(f"Error occurred: {err}")
except ValueError:
    print("Response content is not valid JSON")

# try:
#     image_data = requests.get(f"http://yanwittmann.de/api/mcdata/item.php?name={name}", timeout=10).json()
    
#     # Check if the 'item' key exists and if there are any items in the list
#     if image_data.get("count", 0) > 0 and "item" in image_data:
#         image_url = image_data["item"][0]["image"]
#     else:
#         image_url = "/static/img/placeholder.png"
# except requests.exceptions.Timeout:
#     image_url = "/static/img/placeholder.png"
# except requests.exceptions.RequestException as e:
#     image_url = "/static/img/placeholder.png"
#     print(f"Error fetching image for {name}: {e}")


# import requests
# response = requests.get()
# data = response.json()
# big_cards=[]
# for card in data['dars':]:
#     if card['cmc' > 5:]:
#         print(card['name', card['cmc']])

