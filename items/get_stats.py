import requests
import pandas
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

patch = "12.1.1"

raw_data = requests.get(
    f"https://ddragon.leagueoflegends.com/cdn/{patch}/data/en_US/item.json"
).json()

icon_folder = f"https://ddragon.leagueoflegends.com/cdn/{patch}/img/item/"

data = []

for item_id, raw_item in raw_data["data"].items():
    # Removes non-SR items
    if not raw_item["maps"]["11"]:
        continue

    raw_description = raw_item["description"]
    raw_description: str
    raw_description = raw_description.replace("<br>", "\n")

    # Parsing the html
    soup = BeautifulSoup(raw_description, "html.parser")

    # Removing the closing line jump
    clean_description = soup.text[:-1]

    item_dict = {
        "name": raw_item["name"],
        "depth": raw_item.get("depth"),
        "description": clean_description,
        "icon_url": icon_folder + raw_item["image"]["full"],
        "cost": raw_item["gold"]["total"],
        **raw_item["stats"],
    }

    if "effect" in raw_item:
        item_dict.update(**raw_item["effect"])

    data.append(item_dict)

df = pandas.DataFrame(data=data)
df = df.reindex(sorted(df.columns), axis=1)

df.to_clipboard(index=False)
