import asyncio
import os
import logging
from pyrogram import Client

api_id = 0
api_hash = ''
phone_number = ""
client_app = Client("my_account", api_id, api_hash, phone_code="", phone_number=phone_number)
logging.basicConfig(level=logging.INFO)


async def downloading_protects(target_chat_id: int, target_message_id: int):
    async with Client("my_account", api_id, api_hash, phone_code="+998", phone_number=phone_number) as app:
        app: Client
        message = await app.get_messages(chat_id=target_chat_id, message_ids=target_message_id)
        if not message.empty and not message.text:
            file_downloading = (
                    message.audio or message.video or message.document or message.photo
            )
            if file_downloading:
                file_path = file_downloading.file_name
                with open(file_downloading.file_name, "wb") as file:
                    async for chunk in app.stream_media(file_downloading.file_id):
                        file.write(chunk)
                media_method = {
                    "Audio": app.send_audio,
                    "Video": app.send_video,
                    "Document": app.send_document,
                    "Photo": app.send_photo
                }.get(type(file_downloading).__name__)

                if media_method:
                    try:
                        await media_method(chat_id='me', **{type(file_downloading).__name__.lower(): file_path},
                                           duration=file_downloading.duration)
                    except AttributeError:
                        await media_method(chat_id='me', **{type(file_downloading).__name__.lower(): file_path})
                    os.remove(file_path)
        elif message.text:
            await app.send_message(chat_id='me', text=message.text)


def private_link(post_link: str):
    data = post_link.split('/')
    return int('-100' + data[4]), int(data[5])


post_link = 'https://t.me/c/2105735152/9'
asyncio.run(downloading_protects(*private_link(post_link)))
