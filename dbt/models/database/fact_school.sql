{{ config(materialized='incremental', schema='DATA_WAREHOUSE' ,alias= 'fact_record_school', unique_key='record_id') }}
select _airbyte_data:fields:libelle as libelle, _airbyte_data:fields:id_projet as id_project,
 _airbyte_data:recordid as record_id, _airbyte_data:fields:adresse as adresse
from _AIRBYTE_RAW_SCHOOL