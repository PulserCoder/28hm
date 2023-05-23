import django
django.setup()

import json
from ads.models import Categories

from ads.models import Ads

with open('data/ads.json') as file:
    abs_data = json.load(file)

for item in abs_data:
    item["is_published"] = item["is_published"] == "TRUE"
    item["price"] = int(item["price"])

    abs_item = Ads(**item)
    abs_item.save()

with open('data/categories.json') as file:
    categories_data = json.load(file)

for item in categories_data:
    item["id"] = int(item["id"]) # Преобразовываем строку в целое число

    category_item = Categories(**item)
    category_item.save()