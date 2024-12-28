import json
import time
from env import *
from telethon import TelegramClient
from telethon.errors import FloodWaitError
from telethon.tl.types import Channel, Chat

client = TelegramClient('aipoweredsearch', API_ID, API_HASH).start()
output_file = 'telegram_chats_nochanell.json'

async def main():
  try:
    # Connect to Telegram
    await client.start()

    print("Fetching chats...")
    chats_data = []

    dialogs = await client.get_dialogs()

    # Iterate over all dialogs (chats)
    for dialog in dialogs:
      if isinstance(dialog.entity, (Channel)):
        continue

      chat_info = {
        'id': dialog.id,
        'name': dialog.name,
        'type': type(dialog.entity).__name__,
        'messages': []
      }

      print(f"Fetching messages for chat: {dialog.name} (ID: {dialog.id})")

      # Fetch messages from the chat
      try:
        messages = await client.get_messages(dialog.id, None)
        for message in messages:
          chat_info['messages'].append({
              'id': message.id,
              'date': message.date.isoformat(),
              'sender_id': message.sender_id,
              'text': message.message,
              'reply_to': message.reply_to.reply_to_msg_id if message.reply_to else None
          })
      except FloodWaitError as e:
        print(f"Flood wait error: Sleeping for {e.seconds} seconds")
        time.sleep(e.seconds)

      chats_data.append(chat_info)

    # Save the data to a JSON file
    with open(output_file, 'w', encoding='utf-8') as f:
      json.dump(chats_data, f, ensure_ascii=False, indent=4)

    print(f"All chats and messages have been saved to {output_file}")

  finally:
    await client.disconnect()

if __name__ == '__main__':
  with client:
    client.loop.run_until_complete(main())