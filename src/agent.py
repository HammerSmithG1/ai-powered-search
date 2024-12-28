from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from .utils.database import get_collection
from bson import ObjectId

def answer_the_question(question):
  gen_search_query_prompt = ChatPromptTemplate.from_template(
  """Входной вопрос: {question}

# Задача 
Напиши поисковый запрос, который извлечёт релевантные фрагменты из архива переписок. Помни: ответ на вопрос пользователя не указан явно в переписках. Поэтому поисковый запрос должен быть составлен так, чтобы извлечь ключевые фрагменты, связанные с темой разговора, вопросами или проблемами, обсуждаемыми в переписке, а не просто переформулировать исходный вопрос.

#Требования
1. Поисковый запрос должен быть максимально тематическим и включать ключевые слова, связанные с контекстом вопроса.
2. Используй используй понятные слова, которые помогут в semantic search
3. Старайся учитывать возможные варианты формулировок и синонимы, которые могли быть использованы в архиве.

#Примеры
Вопрос: в каком ресторане я отмечал день рождения в прошлом году?
Поисковый запрос: подготовка к деню рождения, выбор ресторана, организация праздника

Вопрос: какого цвета забор я установил на даче? 
Поисковый запрос: установка забора,  благоустройство дачного участка, ремонт

В ответ пришли только короткий поисковый запрос и ничего больше"""
  )

  chunks_collection = get_collection('chunks')

  vectorstore = Chroma(
    collection_name="dialogs",
    embedding_function=OpenAIEmbeddings(),
    persist_directory="app_data"  # Directory to save data
  )

  llm = ChatOpenAI(model="gpt-4o-mini")

  # делаем промпт из шаблона, просим llm написать поисковый запрос
  prompt = gen_search_query_prompt.invoke({'question': question })
  searchQuery = llm.invoke(prompt)

  # retreive top-4 neighbours
  retreivedData = vectorstore.similarity_search_with_score(
    searchQuery.content
  )

  # собираем контекст для нейросети
  retreivedChunks = chunks_collection.find({"_id": {"$in": list(set([ObjectId(res.metadata.get('chunk_id')) for res, score in retreivedData]))}}).to_list()
  context = '\n\n'.join([x.get('plain_text') for x in retreivedChunks])

  # собираем финальный QA промпт
  qa_query_prompt = ChatPromptTemplate.from_template(
  """Входной вопрос пользователя: {question}

# Фрагменты перписки для контекста
{context}

Ты - полезный ассистент, который умеет анализировать информацию и отвечать на вопросы пользователя. Используя представленные фрагменты переписок пользователя, ответь на вопрос который он задал. Отвечай кратко и по существу. В ответ пришли только ответ на вопрос и ничего больше.
"""
  )
  prompt = qa_query_prompt.invoke({'question': question, 'context': context })
  searchQuery = llm.invoke(prompt)
  return searchQuery.content