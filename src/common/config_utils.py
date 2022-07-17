import os
import codecs
import json
import src.common.os_utils as os_utils
from pymongo import MongoClient
from pymongo import errors
from sqlalchemy import create_engine


def get_config_json(config_name, directory_name):
    try:
        json_file = os.path.join(os_utils.get_root_folder(), directory_name, config_name + '.json')
        with codecs.open(json_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def get_uri():
    mongo_config = get_config_json('globals', 'config')['mongo_credentials']
    full_uri = str("mongodb://" +
                   mongo_config["mongo_username"] +
                   ":" + mongo_config["mongo_password"] +
                   "@" + mongo_config["mongo_uri"] +
                   ":" + str(mongo_config["mongo_port"]) +
                   "/" + "?authSource=" +
                   mongo_config["mongo_auth_source"]
                   )

    return full_uri


def get_snowflake_uri():
    snowflake_config = get_config_json('globals', 'config')['snowflake_credentials']
    full_uri = str("snowflake://" +
                   snowflake_config["user_login_name"] +
                   ":" + snowflake_config["password"] +
                   "@" + snowflake_config["account_identifier"] +
                   "/" + str(snowflake_config["database_name"]) +
                   "/" + str(snowflake_config["schema_name"]) +
                   "?" + "warehouse=" + str(snowflake_config["warehouse_name"]) +
                   "&role=" + str(snowflake_config["role_name"])
                   )

    return full_uri


def connect_staging_database():
    try:
        uri = get_uri()
        client = MongoClient(uri)
        staging = client.school
    except errors.ConnectionFailure as e:
        print('Could not connect to server: %s' % e)
    return staging


def connect_snowflake_DW():
    try:
        engine = create_engine(get_snowflake_uri())
        connection = engine.connect()
    except errors.ConnectionFailure as e:
        print('Could not connect to Snowflake database: %s' % e)
    return connection
