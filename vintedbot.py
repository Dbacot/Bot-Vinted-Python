import requests
import time
from PIL import Image
from io import BytesIO
sent_items = set()
def fetch_items():
    url = "https://www.vinted.fr/api/v2/catalog/items"
    params = {
        "search_text": "carte graphique",  
        "price_to": 450,  
        "status_ids[]": 1, 
        "order": "newest_first", 
    }

    cookies = {
        "access_token_web": "va sur le lien api et colle ton token",
        "refresh_token_web": "va sur le lien api et colle ton token",
    }

    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, params=params, headers=headers, cookies=cookies)
    if response.status_code != 200:
        print(f"Erreur de la requête API: {response.status_code}")
        return []

    items = response.json().get("items", [])
    return items
def send_to_discord(item):
    webhook_url = ""  # Remplace avec ton  webhook

    img_url = item['photo']['url']
    img_data = requests.get(img_url).content
    img = Image.open(BytesIO(img_data))
    img = img.resize((200, 200))
    img.save("temp_image.jpg")
    message = {
        "content": f"**{item['title']}**\nPrix: {item['price']['amount']} {item['price']['currency_code']}\nVendeur: {item['user']['login']}\n[Voir le produit]({item['url']})",
    }
    with open("temp_image.jpg", "rb") as image_file:
        files = {
            "file": ("image.jpg", image_file, "image/jpeg")
        }
        requests.post(webhook_url, data=message, files=files)
def main_loop():
    while True:
        items = fetch_items()
        if items:
            new_items = []
            for item in items[:3]:
                if item['id'] not in sent_items:  
                    new_items.append(item)
                    sent_items.add(item['id'])
            for item in new_items:
                send_to_discord(item)

        print("Attente de 10 sec avant la prochaine vérification...")
        time.sleep(10) 

main_loop()
