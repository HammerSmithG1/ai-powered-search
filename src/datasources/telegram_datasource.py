import json
import time
from ..utils.database import get_collection
from pathlib import Path

def full_upload():
  dialogs = [x for x in json.loads(Path('dev_data/telegram_chats_nochanell.json').read_text())]
  dialogs = [
    {**obj, "messages": [msg for msg in obj["messages"] if msg['text'] and len(msg["text"]) > 0]}
    for obj in dialogs
  ]
  dialogs = [
    x for x in dialogs if len(x['messages']) > 0
  ]

  documents = get_collection('documents')
  doc = documents.insert_one({
    "source": "telegram",
    "createdAt": int(time.time()),
    "description": "telegram messages of user 2"
  })

  return (doc.inserted_id, dialogs)

# TODO: 
#   - Load new messages