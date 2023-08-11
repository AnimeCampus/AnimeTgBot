import requests
from pyrogram import Client, filters
from pyrogram.types import InputFile, InlineQuery, InlineQueryResultPhoto

# Replace with your own API_ID, API_HASH, and BOT_TOKEN
API_ID = "your_api_id"
API_HASH = "your_api_hash"
BOT_TOKEN = "your_bot_token"
RAPIDAPI_KEY = "your_rapidapi_key"

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
        await message.reply_photo(InputFile(cartoon_image_path))
    else:
        await message.reply_text("Failed to cartoonize the image. Please try again.")

@Client.on_inline_query()
async def inline_query(client, query: InlineQuery):
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
            id="1",
            photo_url=cartoon_image_path,
            thumb_url=cartoon_image_path,
            caption=caption
        )
        await query.answer([photo_result])

# Start the Pyrogram client
app.run()
