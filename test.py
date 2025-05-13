import requests

url = "https://www.gamergeeks.net/apps/minecraft/web-developer-tools/css-blocks-and-entities"

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