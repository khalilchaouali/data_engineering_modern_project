from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.airbyte.sensors.airbyte import AirbyteJobSensor
from airflow.utils.dates import days_ago, parse_execution_date
from airflow.providers.airbyte.operators.airbyte import AirbyteTriggerSyncOperator
from airflow.models import Variable
from src.ELT_ETL.get_data_from_end_point import extract_data_source, load_raw_data, transform_load_records_data
from src.common.config_utils import get_config_json

airbyte_connection_id = Variable.get("AIRBYTE_CONNECTION_ID")
dbtConfig = get_config_json('globals', 'config')
with DAG(dag_id='trigger_airbyte_dbt_job',
         default_args={'owner': 'airflow'},
         schedule_interval='@daily',
         start_date=days_ago(1),
         render_template_as_native_obj=True
         ) as dag:
    airbyte_sync = AirbyteTriggerSyncOperator(
        task_id='Update_snowflake_database',
        airbyte_conn_id='Update_snowflake_database',
        connection_id=airbyte_connection_id,
        asynchronous=False,
        timeout=3600,
        wait_seconds=3
    )
    extract_data_source = PythonOperator(
        task_id='extract_data_source',
        python_callable=extract_data_source,
        op_kwargs={"date": "{{execution_date}}"},
    )

    load_raw_data = PythonOperator(
        task_id='load_raw_data',
        python_callable=load_raw_data,
        op_kwargs={"date": parse_execution_date},
    )

    transform_load_records_data = PythonOperator(
        task_id='transform_load_records_data',
        python_callable=transform_load_records_data,
        op_kwargs={"date": parse_execution_date},
    )

    airbyte_sensor = AirbyteJobSensor(
        task_id='airbyte_sensor_money_json_example',
        airbyte_conn_id='Update_snowflake_database',
        airbyte_job_id=airbyte_sync.output
    )

    increment_DW_data = BashOperator(
        task_id="incriment_DW_data",
        bash_command=f"""
                cd {dbtConfig["DBT_DIR"]} &&
                dbt run {dbtConfig["GLOBAL_CLI_FLAGS"]} ./
                """,
    )
extract_data_source >> load_raw_data >> transform_load_records_data >> airbyte_sync >> airbyte_sensor \
>> increment_DW_data
