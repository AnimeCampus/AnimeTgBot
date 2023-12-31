import requests
from pyrogram import Client, filters
from pyrogram.types import InlineQueryResultPhoto

# Replace with your own API_ID, API_HASH, and BOT_TOKEN
API_ID = "19099900"
API_HASH = "2b445de78e5baf012a0793e60bd4fbf5"
BOT_TOKEN = "6206599982:AAGELlIUapiHd88l5z4YuVwXp1h3tHMfotY"
RAPIDAPI_KEY = "e738a41537msh518a25cf253209fp13958fjsn07ed13e97c48"


# Initialize the Pyrogram client
app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@Client.on_message(filters.command("start"))
async def start_command(client, message):
    await message.reply_text("Hello! I am your bot. Send me an image to cartoonize.")

@Client.on_message(filters.command("help"))
async def help_command(client, message):
    help_text = "Send me a photo to cartoonize it!\n\nCommands:\n/start - Start the bot\n/help - Display this help message"
    await message.reply_text(help_text)

@Client.on_message(filters.photo)
async def cartoonize_image(client, message):
    url = "https://cartoon-yourself.p.rapidapi.com/facebody/api/portrait-animation/portrait-animation"
    
    # Get the largest photo (highest resolution) sent by the user
    photo = message.photo[-1]
    file_id = photo.file_id
    file_path = await client.download_media(file_id)
    
    payload = {
        "image": open(file_path, "rb"),
        "type": "anime"
    }
    
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "cartoon-yourself.p.rapidapi.com"
    }
    
    response = requests.post(url, files=payload, headers=headers)
    result = response.json()
    
    if result.get("success"):
        cartoon_image_path = result["url"]
        await message.reply_photo(photo=cartoon_image_path, quote=True)
    else:
        await message.reply_text("Failed to cartoonize the image. Please try again.")

@Client.on_inline_query()
async def inline_query(client, query):
    if query.query == "":
        return
    
    url = "https://cartoon-yourself.p.rapidapi.com/facebody/api/portrait-animation/portrait-animation"
    
    file_id = query.from_user.id
    file_path = await client.download_media(query.from_user.photo.big_file_id)
    
    payload = {
        "image": open(file_path, "rb"),
        "type": "anime"
    }
    
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "cartoon-yourself.p.rapidapi.com"
    }
    
    response = requests.post(url, files=payload, headers=headers)
    result = response.json()
    
    if result.get("success"):
        cartoon_image_path = result["url"]
        caption = "Cartoonized by your bot!"
        photo_result = InlineQueryResultPhoto(
            photo_url=cartoon_image_path,
            thumb_url=cartoon_image_path,
            caption=caption
        )
        await query.answer([photo_result])

print("started") 
# Start the Pyrogram client
app.run()
