import airflow
from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from google.cloud import storage
from user_def import *

import nytimes as ny
import penguin as pen
import spotify as spt

def download_nytimes():
    blob_name = f'{yesterday}/nytimes.json'
    data = ny.get_data()
    json = ny.convert_data(data)
    ny.write_json_to_gcs(bucket_name, blob_name, service_account_key_file, json)

def download_penguin():
    blob_name = f'{yesterday}/penguin.json'
    data = pen.getdata(10)
    pen.write_json_to_gcs(bucket_name, blob_name, service_account_key_file, data)

def download_spotify():

    cid = 'your cid'
    secret = 'your secret'
    blob_name = f'{yesterday}/spotify.json'
    user = 'your user'
    playlists = spt.retrieve_playlists(cid,secret,user)
    data = spt.call_playlists(playlists, cid,secret)
    spt.write_json_to_gcs(bucket_name, blob_name, service_account_key_file, data)


with DAG(
    dag_id="your dag_id",
    schedule="@daily",
    start_date=datetime(2023, 5, 6),
    catchup=False
) as dag:

    create_insert_aggregate = SparkSubmitOperator(
        task_id="your task_id",
        packages="your gcs url",
        exclude_packages="javax.jms:jms,com.sun.jdmk:jmxtools,com.sun.jmx:jmxri",
        conf={"spark.driver.userClassPathFirst":True,
             "spark.executor.userClassPathFirst":True
             },
        verbose=True,
        application='./aggregates_to_mongodb.py'
    )

    download_nytimes_data = PythonOperator(task_id = "download_nytimes_data",
                                                  python_callable = download_nytimes,
                                                  dag=dag)

    download_penguin_data = PythonOperator(task_id = "download_penguin_data",
                                                  python_callable = download_penguin,
                                                  dag=dag)

    download_spotify_data = PythonOperator(task_id = "download_spotify_data",
                                                  python_callable = download_spotify,
                                                  dag=dag)




    [download_spotify_data,download_penguin_data,download_nytimes_data] >> create_insert_aggregate
