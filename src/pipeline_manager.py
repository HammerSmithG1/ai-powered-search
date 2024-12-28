from .datasources import telegram_datasource as TelegramDataSoure
from .pipelines import messenger_pipeline as MessengerPipeline

def import_telegram_data(): 
  doc_id, data = TelegramDataSoure.full_upload()
  MessengerPipeline.process_data(doc_id, data)
