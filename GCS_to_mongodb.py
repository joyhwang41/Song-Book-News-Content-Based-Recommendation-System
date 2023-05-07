from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
from google.cloud import storage
from mongodb import *
import json
from user_def import *


def add_json_data_to_rdd(rdd, json_data, json_field_name):
    rdd_dict = rdd.asDict()
    rdd_dict[json_field_name] = json_data
    # id = rdd_dict['id']
    # rdd_dict['_id'] = id
    # rdd_dict.pop('id', None)

    return rdd_dict

def add(x, obj, name):
    x[name] = obj
    return x

def return_json(service_account_key_file,
                bucket_name,
                blob_name):
    storage_client = storage.Client.from_service_account_json(service_account_key_file)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    json_str = blob.download_as_string().decode("utf8")
    json_data = json.loads(json_str)
    return json_data

def make_rdd(Penguin_json_object, New_York_json_object, Spotify_json_object):


    conf = SparkConf().setAppName("projectName")#.setMaster("local[*]")
    sc = SparkContext.getOrCreate(conf)
    spark = SparkSession.builder.appName('Empty_Dataframe').getOrCreate()


    data = [{"API": 'data from Penguin Random House, New York Times and Spotify',}]

    rdd = sc.parallelize(data)

    df = rdd.toDF()

    if Penguin_json_object is not None:
        json_object_p = Penguin_json_object

    if New_York_json_object is not None:
        json_object_n = New_York_json_object

    if Spotify_json_object is not None:
        json_object_s = Spotify_json_object

    if Penguin_json_object is not None:
        aggregates = df.rdd.map(
                lambda x: add_json_data_to_rdd(x, json_object_p, 'Penguin Random House')
            )
    # if New_York_json_object is not None:
    #     aggregates = df.rdd.map(
    #             lambda x: add_json_data_to_rdd(x, json_object_n, 'New York Times')
    #         )
    if New_York_json_object is not None:
        aggregates = aggregates.map(
                lambda x: add(x, json_object_n, 'New York Times')
            )
    # if Spotify_json_object is not None:
    #     aggregates = aggregates.map(
    #             lambda x: add_json_data_to_rdd(x, json_object_s, 'Spotify')
    #         )
    # if Spotify_json_object is not None:
    #     aggregates = df.rdd.map(
    #             lambda x: add_json_data_to_rdd(x, json_object_s, 'Spotify')
    #         )
    if Spotify_json_object is not None:
        aggregates = aggregates.map(
                lambda x: add(x, json_object_s, 'Spotify')
            )

    return aggregates

def insert_to_mongodb(aggregates, mongo_username, mongo_password, mongo_ip_address, database_name, collection_name):

    mongodb = MongoDBCollection(mongo_username,
                                mongo_password,
                                mongo_ip_address,
                                database_name,
                                collection_name)

    for aggregate in aggregates.collect():
        #print(aggregate)
        mongodb.insert_one(aggregate)

def insert_aggregate_to_mongo(service_account_key_file,bucket_name,blob_name, mongo_username, mongo_password, mongo_ip_address, database_name, collection_name):
    bookjsonfile = return_json(service_account_key_file,bucket_name,blob_name[0])
    spotifyfile = return_json(service_account_key_file,bucket_name,blob_name[1])
    nytimesfile = return_json(service_account_key_file,bucket_name,blob_name[2])
    bookjsonfile = json.loads(bookjsonfile)
    spotifyfile = json.loads(spotifyfile)
    nytimesfile = json.loads(nytimesfile)
    test = make_rdd(bookjsonfile, nytimesfile, spotifyfile)
    insert_to_mongodb(test, mongo_username, mongo_password, mongo_ip_address, database_name, collection_name)



if __name__=="__main__":

    insert_aggregate_to_mongo(service_account_key_file,bucket_name,blob_name, mongo_username, mongo_password, mongo_ip_address, database_name, collection_name)