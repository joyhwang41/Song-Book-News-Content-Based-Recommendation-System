from datetime import date, datetime, timedelta
import os

yesterday = date.today() - timedelta(days=1)

mongo_username = os.environ.get("MONGO_USERNAME")
mongo_password = os.environ.get("MONGO_PASSWORD")
mongo_ip_address = os.environ.get("MONGO_IP")
database_name = os.environ.get("MONGO_DB_NAME")
collection_name = os.environ.get("MONGO_COLLECTION_NAME")

service_account_key_file=os.environ.get("GS_SERVICE_ACCOUNT_KEY_FILE")
bucket_name = os.environ.get("GS_BUCKET_NAME")
blob_name= [f'{yesterday}/penguin.json', f'{yesterday}/spotify.json', f'{yesterday}/nytimes.json']
