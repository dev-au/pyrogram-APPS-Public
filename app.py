from pyrogram import Client, filters
import logging
import asyncio

senior_user_id = #telegram_user_id
api_id = #api_id
group_id = #control_group_id
api_hash = #api_hash
phone_code = #country_code
phone_number = #phone_number
app = Client("my_account", api_id, api_hash, phone_code=country_code, phone_number=phone_number)
logging.basicConfig(level=logging.INFO)


async def timer_message(chat_id, text, message_id):
    await asyncio.sleep(2)
    for s in range(1, 101):
        # print(txt[s:]
        txt = f"{s}% ----- 100%"
        await app.edit_message_text(chat_id=chat_id, message_id=message_id, text=txt)
        await asyncio.sleep(0.15)
    emoji = "⌛⏳"
    for i in range(len(text)):
        new_text = f"{emoji[i % 2]}{text[:(i + 1)]}{emoji[(i + 1) % 2]}"
        await app.edit_message_text(chat_id=chat_id, message_id=message_id, text=new_text)
        await asyncio.sleep(1)
    await app.edit_message_text(chat_id=chat_id, message_id=message_id, text=text)


@app.on_message(filters=filters.private)
async def my_handler(client, message):
    if message.from_user.id != senior_user_id:
        await app.forward_messages(chat_id=group_id, from_chat_id=message.from_user.id, message_ids=[message.id])
    else:
        text = message.text
        if len(text) > 1 and text[0] == "/" or text[0] == "(":
            num = text[1:]
            try:
                new_text = await app.get_messages(chat_id=group_id, message_ids=[int(num)])
                new_text = new_text[0].text
                await message.edit_text(text="Loading...")
                await timer_message(message.chat.id, new_text, message.id)
            except Exception as error:
                print(error)
                pass


@app.on_message(filters=filters.group)
async def my_handler2(client, message):
    if message.chat.id == group_id:
        try:
            message2 = message.reply_to_message
            message2 = message2.forward_from
            msg = await app.send_message(chat_id=message2.id, text="Loading...")
            await timer_message(message2.id, message.text, msg.id)
        except:
            await message.reply(message.id)
            pass
    elif message.from_user.id == senior_user_id:
        text = message.text
        if len(text) > 1 and text[0] == "/" or text[0] == "(":
            num = text[1:]
            try:
                new_text = await app.get_messages(chat_id=group_id, message_ids=[int(num)])
                new_text = new_text[0].text
                await message.edit_text(text="Loading...")
                await timer_message(message.chat.id, new_text, message.id)
            except:
                pass


app.run()
