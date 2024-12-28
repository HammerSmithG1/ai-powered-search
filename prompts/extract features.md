## ////////////////////////////////// Оригинал //////////////////////////////////

-Goal-
Тебе нужно обработать этот фрагмент переписки из мессенджера, выделив из него все семантически занчимые признаки (Named Entity Recognition, high-level and low-level keywords, main themes and meaningfull tags) для дальнейшего использования этих данных в semantic search и RAG.
В Metadata перечислены Entities, themes, keywords и tags, которые ты выделил при обработке предыдущих фрагментов. Ты можешь использовать их, чтобы не создавать дубликаты (если уверен, что упоминается именно this feature), либо создавать новые.

-Steps-

1. Очистка текста от лишнего шума.

- Игнорируй неинформативные сообщения:
  • стоп-слова, если они не добавляют смысла;
  • Приветствия, прощания, фразы вроде “ок”, “да”, “понял”;
  • Эмодзи, HTML-теги, специальные символы (если они не важны для анализа);
- Ты можешь переформулировать текст для устранения неоднозначностей, упрощать сложные фразы, сохраняя их смысл;

2. Анализ диалога, выявление неявных связей и контекста

- Проанализируй фрагмент диалога, выдели ключевые идеи, важные факты и смысловые связи;
- Определи скрытые взаимосвязи между репликами (например, упоминания событий, людей или задач);
- Определи хронологию и структуру;
- Убедись что не упустил важную для поиска информацию;
- Не придумывай факты, опирайся на информацию из переписки и контекст.

2. Named Entity Recognition (NER):

- Выдели ключевые сущности из диалога: например, люди, компании, места, события, сайты, продукты, собеседники, даты, etc;
- Используй сущности из EntitiesList и Metadata, чтобы не создавать дубликатов, если ты уверен, что упоминается именно эта сущность;
- Если нужно, ты можешь добавить новые Enitites в list или дополнять данные существующие;
- Для каждой новой сущности необходимо заполнить:
  • id: уникальный идетификатор сущности, используй числа
  • name: название сущности
  • synonyms: список альтернативных названий этой сущност, встречающихся в тексте. Нужен для улучшения узнаваемости этой сущности в дальнейшем
  • type: тип сущености, например
  [
  "person", # people, including fictional characters
  "fac", # buildings, airports, highways, bridges
  "org", # organizations, companies, agencies, institutions
  "gpe", # geopolitical entities like countries, cities, states
  "loc", # non-gpe locations
  "product", # vehicles, foods, appareal, appliances, software, toys
  "event", # named sports, scientific milestones, historical events
  "work_of_art", # titles of books, songs, movies
  "law", # named laws, acts, or legislations
  "language", # any named language
  "date", # absolute or relative dates or periods
  "time", # time units smaller than a day
  "percent", # percentage (e.g., "twenty percent", "18%")
  "money", # monetary values, including unit
  "quantity", # measurements, e.g., weight or distance
  ]. Можешь добавить свой тип сущности если необходимо
  • description: короткое описание этой сущности и ее значение в контексте диалога
- Дополни информацию о существующих Entities, если видишь новые важные данные;

3. Выделение смыслов и Темы:

- Проанализировав содержание и контекст диалога, выдели из него смыслы и Темы.
- Темы должны быть точными и конкретными, сформулированными коротко. Выделай Темы так, чтобы точно и подробно описать смысл всех фрагментов диалога и чтобы обеспечить максимальное качетсво поиска в дальнейшем. Например, "запуск стартапа", "оформление страховки в путешествие", "найм водителя в компанию".
- Можешь использовать несколько Тем для каждого фрагмента, чтобы лучше описать контекст;
- Используй Темы из ThemesList и Metadata, чтобы не создавать дубликатов, если ты уверен, что эта Тема отражает смысл разговора. Ты можешь добавлять новые Темы в list и использовать их;

4. Выделение Ключевых Слов и Тегов

- Выдели из диалога важные Ключевые Слова, которые помогут при поиске по keyword search и full-text search, Выделяй как low-level так и high-level Keywords. В отличие от Тем, Ключевые Слова нужно выбирать строго из текста, а не формалировать по смыслу. Лемматизируй Ключевые Слова.
- Подбери и выдели теги, которые помогут описать контекст диалога. В тегах можно добавить любые важные пометки которые не явлюятся Темой или Ключевым словом: эмоциональныю окраску, контекст разговора, обстоятельства. Например: "конфликт", "планерка", "заметки", т.д.

-Dialog Chunk-
{dialog_chunk as text}

-Metadata-
{metadata as json}

## ////////////////////////////////// Улучшено ChatGPT //////////////////////////////////

== Goal ==
Your task is to process a chat fragment from a messenger (this is a conversations of a user with ID {id}) to extract semantically significant elements for embedding, semantic search and Retrieval-Augmented Generation (RAG). These elements include Named Entities, high-level and low-level keywords, main themes, and meaningful tags.

Analyze the dialogues and extract semantically significant elements from the perspective of the user with ID {id}, as this is an archive of their conversations, and they will later perform searches on it. Call him "Superuser".

== Steps ==

1. Text Cleanup.
   Objective: Ignore irrelevant noise.

Instructions:

- Ignore non-informative messages, such as:
  - Greetings, farewells, and filler phrases like "да," "ок" or "понял"
  - Emojis, HTML tags, and special symbols (unless critical for meaning).
- Rephrase text to:
  - Eliminate ambiguities.
  - Simplify complex phrases while retaining their meaning.

2. Dialogue Analysis and Context Identification
   Objective: Extract key ideas, facts, and semantic connections from the dialogue.

Instructions:

- Identify important facts and events, ensuring no critical information is overlooked.
- Recognize relationships between messages (e.g., mentions of people, events, or tasks).
- Determine the chronology and structure of the conversation.
- Base your analysis strictly on the dialogue content—do not fabricate details.

3. Named Entity Recognition (NER)
   Objective: Extract and classify key entities from the dialogue.

Instructions:

- Use the provided Metadata to avoid duplicate entities when confident of a match.
- For new entities, provide the following details:
  - id: A unique identifier (e.g., numbers);
  - name: The entity's name
  - synonyms: Alternative names or references for the entity.
  - type: here is the list on predefined types. Add new types if needed.
    {
    "person": "people, including fictional characters",
    "fac": "buildings, airports, highways, bridges",
    "org": "organizations, companies, agencies, institutions",
    "gpe": "geopolitical entities like countries, cities, states",
    "loc": "non-gpe locations",
    "product": "vehicles, foods, apparel, appliances, software, toys",
    "event": "named sports, scientific milestones, historical events",
    "work_of_art": "titles of books, songs, movies",
    "law": "named laws, acts, or legislations",
    "language": "any named language",
    "date": "absolute or relative dates or periods",
    "time": "time units smaller than a day",
    "percent": "percentage (e.g., 'twenty percent', '18%')",
    "money": "monetary values, including unit",
    "quantity": "measurements, e.g., weight or distance"
    }
  - description: Briefly describe the entity's relevance to the dialogue.

Example:
{
"id": 1,
"name": "John Smith",
"synonyms": ["John", "Mr. Smith"],
"type": "person",
"description": "Superusers businsess parther, baseball teammate"
}

1. Themes and Meanings Extraction
   Objective: Identify the main themes and meanings in the dialogue.

Instructions:

- Capture the essence of the dialogue in precise, concise themes.
- Reuse themes from the Metadata or create new ones.
- Assign multiple themes if necessary for better context.

Example:
Themes: ["запуск стартапа", "оформление страховки в путешествие", "найм водителя в компанию"]

5. Keyword and Tag Extraction
   Objective: Extract significant Keywords and Tags to describe the dialogue context.

Instructions:

- Extract both high-level and low-level keywords, lemmatized for consistency.
- Assign Tags to capture additional context, such as emotional tone or situational details.

If the dialogue contains ambiguous or incomplete information:
Flag it with a note in the Tag "unclear context"

Provide the best possible extraction based on the available data.

Metadata
{metadata}

Chat Fragment
{chat_fragment}
