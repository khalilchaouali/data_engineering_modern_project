import logging

import requests
import datetime as dt
import warnings
import locale
from airflow import exceptions
from src.common.config_utils import get_config_json, connect_staging_database
import pandas as pd
warnings.filterwarnings("ignore")

elt_config = get_config_json("ELTConfig", "./ELT_ETL")


def previous_month():
    return dt.date.today() - dt.timedelta(weeks=5)


def get_params(params, date):
    params["cat"] = params["cat"]+date.strftime("%m")+"'"
    params["db"] = params["df"] = str(date.year)+"1231"
    return params


def format_date(date):
    return str(date.year-1)+"-"+str(date.year-1)


def extract_data_source(ti, date):
    try:
        # Open Paris Data consuming

        locale.setlocale(locale.LC_TIME, '')
        print(date)
        path = elt_config["URL_SOURCE"]
        params = elt_config["PARAMS"]
        if requests.get(path, params=params, verify=False).status_code == 404:
            raise ConnectionError("Server doesn't response")
        data = requests.get(path, params=params, verify=False).json()
        if data == {"error": "Unknown dataset:"+params["dataset"]}:
            raise exceptions.AirflowNotFoundException("data not found for this dataset_id")

        # Airflow code

        ti.xcom_push(key='data',
                     value=data)
    except BaseException as err:
        logging.exception('server side error or data not found')
        raise err


def load_raw_data(ti, date):
    global db
    try:
        try:
            db = connect_staging_database()
        except Exception as err:
            print("MongoDB connexion failed. " + str(err))
            raise err

        # Airflow code

        school_data = ti.xcom_pull(key='data', task_ids='extract_data_source')

        #Injecting RawData to School database

        document_count_before_updating = db.schoolRawData.count_documents({})
        db.schoolRawData.update_one({"records": school_data["records"]}, {"$set": school_data}, upsert=True)
        existance_status =db.schoolRawData.count_documents({}) > document_count_before_updating

        # Airflow code

        ti.xcom_push(key='existance_status',
                     value=existance_status)
        ti.xcom_push(key='school_data',
                     value=school_data)
    except Exception as err:
        logging.exception("data not loaded")
        raise err
    return "Done"


def transform_load_records_data(ti, date):
    global db
    try:
        try:
            db = connect_staging_database()
        except Exception as err:
            print("MongoDB connexion failed. " + str(err))
            raise err

        # Airflow code

        school_data = ti.xcom_pull(key='school_data', task_ids='load_raw_data')

        # Transforming raw data into mongo collections
        print(school_data["records"])
        existance_status = ti.xcom_pull(key='existance_status', task_ids='load_raw_data')
        if existance_status:
            db.school.insert_many(school_data["records"])
            db.arr_libelle.insert_many(school_data["facet_groups"][1]["facets"])
            db.arr_insee.insert_many(school_data["facet_groups"][2]["facets"])
    except Exception as err:
        logging.exception("data not loaded")
        raise err
    return "Done"