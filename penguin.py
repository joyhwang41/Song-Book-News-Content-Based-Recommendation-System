import numpy as np
import requests
import json
from google.cloud import storage

def getdata(r):
    dic = dict()
    for i in np.arange(0, r, 10):
        response = requests.get(f"https://api.penguinrandomhouse.com/resources/v2/title/domains/PRH.US/works?api_key={your_api_key}e&start={i}")
        d = response.json()
        works = d['data']['works']
        for work in works:
            workId = work['workId']
            data = dict()
            data['title'] = work['title']
            data['author'] = work['author']
            data['onsale'] = work['onsale']
            data['language'] = work['language']
            dic[workId] = data
    for i in dic.keys():
        response = requests.get(f'https://api.penguinrandomhouse.com/resources/v2/title/domains/PRH.US/works/{i}/views/product-display?api_key={your_api_key}}')
        doc = response.json()
        d = doc['data']
        wid = d['workId']
        if wid == i:
            praises = d['praises']
            authorBio = d['frontlistiestTitle']['authorBio']
            aboutTheBook = d['frontlistiestTitle']['aboutTheBook']
            keynote = d['frontlistiestTitle']['keynote']

            dic[wid]['praises'] = praises
            dic[wid]['authorBio'] = authorBio
            dic[wid]['aboutTheBook'] = aboutTheBook
            dic[wid]['keynote'] = keynote

        re2 = requests.get(f'https://api.penguinrandomhouse.com/resources/v2/title/domains/PRH.US/works/{i}/categories?api_key={your_api_key}')
        cat = re2.json()['data']['categories']
        # wid = re2.json()['data']['workId']
        if wid == i:
            categories = []
            for c in cat:
                categories.append({c['catId']: c['description']})
            dic[wid]['categories'] = categories

    return json.dumps(dic)

def write_json_to_gcs(bucket_name, blob_name, service_account_key_file, data):
    """Write and read a blob from GCS using file-like IO"""
    storage_client = storage.Client.from_service_account_json(service_account_key_file)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    with blob.open("w") as f:
        json.dump(data, f)
