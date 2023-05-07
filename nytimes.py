import requests
import json
from google.cloud import storage


def get_data():
    # meta data
    api_key = "your api key"
    url = f"https://api.nytimes.com/svc/news/v3/content/all/all.json?limit=500&api-key={api_key}"

    response = requests.get(url)
    data = response.json()
    divider = '-------------------------------------------------------------\n'
    return data

def convert_data(data):

    titles = []
    abstracts = []
    captions = []
    articles = []
    for i in range(len(data['results'])):
        titles.append(data['results'][i]['title'])
        abstracts.append(data['results'][i]['abstract'])

        caption = data['results'][i]['multimedia']
        if not caption:
            captions.append('')
        else:
            captions.append(data['results'][i]['multimedia'][0]['caption'])

    data = {}

    # Iterate through the lists and add the values to the dictionary
    for i in range(len(titles)):
        data[i] = {
            "title": titles[i],
            "caption": captions[i],
            "abstract": abstracts[i]
        }

    # Convert the dictionary to a JSON formatted string
    json_string = json.dumps(data, indent=4)
    return json_string

def write_json_to_gcs(bucket_name, blob_name, service_account_key_file, data):
    """Write and read a blob from GCS using file-like IO"""
    storage_client = storage.Client.from_service_account_json(service_account_key_file)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    with blob.open("w") as f:
        json.dump(data, f)