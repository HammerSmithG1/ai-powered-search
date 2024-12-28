import json
import re
from datetime import datetime, timedelta
from ..utils.database import get_collection


"""
  - dialog_messages: массив объектов сообщений
  - chunk_size: длинна в символах
"""
def chunk_dialog(dialog_messages, chunk_size):
  chunks = []
  current_chunk = []
  current_length = 0

  for message in dialog_messages:
    message_length = len(message['text'])

    if current_length + message_length > chunk_size:
      if current_chunk:
        chunks.append(current_chunk)
      current_chunk = [message]
      current_length = message_length
    else:
      current_chunk.append(message)
      current_length += message_length
      
  if current_chunk:
    chunks.append(current_chunk)

  return chunks


# Pipelins stages

def chunk_document(doc_id, data):
  chunks = get_collection('chunks')

  inserted_ids = []

  for dialog in data: 
    #Делим массив сообщений на куски
    chunked_dialog = chunk_dialog(dialog['messages'], 4000)
    if(len(chunked_dialog) == 0):
      print(dialog)
   
    
    #Итерируемся по кусками массивов и формируем объекты чанков
    chunks_to_insert = []
    for i, chunk in enumerate(chunked_dialog): 
      chunks_to_insert.append({
        "chunk_id": '{0}_{1}'.format(dialog['id'], i),
        "document_id": doc_id, 
        "chunk_index": i, 
        "processing_log": [],
        "chunk_metadata": {
          "dialogId": dialog['id'],
          "name": dialog.get('name') or dialog['id'],
          "dialogType": dialog['type'],
          "timestampFrom": chunk[0]['date'],
          "timestampTo": chunk[-1]['date'] 
        },
        "original_data": json.dumps(chunk, ensure_ascii=False)
      })
    result = chunks.insert_many(chunks_to_insert)
    inserted_ids.extend(result.inserted_ids)
    
  return inserted_ids

def to_plain_text(chunks_ids):
  log_str = '{timestamp}|to_plain_text|v1.0.1'.format(timestamp=datetime.now())
  chunks_collection = get_collection('chunks')

  chunks = chunks_collection.find({"_id": {"$in": chunks_ids}})
  
  for chunk in chunks: 
    chat = ""
    # склеиваем диалог так чтобы старое сообщение было сверху
    for msg in json.loads(chunk.get("original_data")):
      # text = re.sub(r'\s+', ' ', msg['text'].replace('"', '\\"').replace('\n', ' ')).strip()
      text = re.sub(r'\s+', ' ', msg['text'].replace('\n', ' ')).strip()
      chat = '{author}({timestamp}):{message}\n'.format(
        author=msg['sender_id'], 
        timestamp=(datetime.fromisoformat(msg['date'][:-6]) + timedelta(hours=3)).strftime("%Y.%m.%d %H:%M"), 
        message=text
      ) + chat

    
    result = chunks_collection.update_one(
        {"_id": chunk["_id"]}, 
        {
          "$set": {
            "plain_text":chat, 
            "processing_log": [log_str] + chunk["processing_log"]
          },
        }
    )




def process_data(doc_id, data):
  print('[Messenger Pipeline]: Running processing pipeline...')
  
  print('[Messenger Pipeline]: Chunking document...')
  chunks_ids = chunk_document(doc_id, data)
  print('[Messenger Pipeline]: {0} chunks created...'.format(len(chunks_ids)))

  print('[Messenger Pipeline]: Format to plain text...')
  chunks_ids = to_plain_text(chunks_ids)
  print('[Messenger Pipeline]: All chunks formated')

  print('[Messenger Pipeline]: Done.')
