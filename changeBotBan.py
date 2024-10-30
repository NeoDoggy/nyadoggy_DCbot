import requests
import base64
 
DISCORD_BOT_TOKEN = input("Enter your bot's TOKEN: ").strip()
BANNER_IMAGE_URL = input("Enter the image URL: ")
 
banner_image_response = requests.get(BANNER_IMAGE_URL)
 
if banner_image_response.status_code == 200:
    banner_image_base64 = base64.b64encode(banner_image_response.content).decode('utf-8')
 
    payload = {
        "banner": f"data:image/gif;base64,{banner_image_base64}"
    }
 
    headers = {
        "Authorization": f"Bot {DISCORD_BOT_TOKEN}",
        "Content-Type": "application/json"
    }
 
    response = requests.patch('https://discord.com/api/v10/users/@me', headers=headers, json=payload)
 
    if response.status_code == 200:
        print("The banner has been successfully uploaded!")
    else:
        print("Failed to change the banner:", response.text)
 
else:
    print("Failed to download profile banner.")