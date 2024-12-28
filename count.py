import json

def count_symbols_and_words_from_json(file_path):
  try:
      # Read JSON string from file
      with open(file_path, 'r', encoding='utf-8') as file:
          json_data = file.read()
      
      # Parse JSON to ensure it's valid
      data = json.loads(json_data)

      str = []

      for i in data:
        if i['id'] == 209950637:
          for msg in i['messages']:
            if msg['text'] is not None and len(msg['text']) > 0:
              str.append(msg['text'].replace('\n', '') + '\n')
          with open('misha.txt', 'w', encoding='utf-8') as f:
            f.writelines(str)
            # json.dump(i, f, ensure_ascii=False, indent=4)

      print(len(''.join(str)))
      
      # # # Convert JSON data back to string for counting
      # json_string = json.dumps(data, ensure_ascii=False)

      # # Count symbols (characters)
      # symbol_count = len(json_string)

      # # Count words (split by whitespace)
      # word_count = len(json_string.split())

      # print(f"Number of symbols (characters): {symbol_count}")
      # print(f"Number of words: {word_count}")

  except json.JSONDecodeError:
      print("Error: The file does not contain valid JSON.")
  except FileNotFoundError:
      print("Error: File not found.")
  except Exception as e:
      print(f"An unexpected error occurred: {e}")

# Replace 'file.json' with your file path
file_path = 'telegram_chats.json'
count_symbols_and_words_from_json(file_path)