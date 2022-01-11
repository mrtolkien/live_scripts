import requests
import pandas
from bs4 import BeautifulSoup

raw_data = requests.get(
    "https://ddragon.leagueoflegends.com/cdn/12.1.1/data/en_US/item.json"
).json()

data = []

for item_id, raw_item in raw_data["data"].items():
    # Removes non-SR items
    if not raw_item["maps"]["11"]:
        continue

    icon_folder = "https://ddragon.leagueoflegends.com/cdn/12.1.1/img/item/"

    raw_description = raw_item["description"]
    raw_description: str
    raw_description = raw_description.replace("<br>", "\n")

    description = BeautifulSoup(raw_description).text

    item_dict = {
        "name": raw_item["name"],
        "depth": raw_item.get("depth"),
        "description": description,
        "icon_url": icon_folder + raw_item["image"]["full"],
        "cost": raw_item["gold"]["total"],
        **raw_item["stats"],
    }

    data.append(item_dict)

df = pandas.DataFrame(data=data)

df.to_clipboard()
