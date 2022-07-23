{{ config(materialized='incremental', schema='DATA_WAREHOUSE', alias= 'dim_location', unique_key='adresse') }}
select distinct(_airbyte_data:fields:adresse) as adresse, _airbyte_data:fields:libelle as libelle,
 _airbyte_data:fields:arr_insee as arr_insee,  _airbyte_data:fields:arr_libelle as arr_libelle,
 _airbyte_data:geometry:coordinates[0] as latitude, _airbyte_data:geometry:coordinates[1] as longitude
from _AIRBYTE_RAW_SCHOOL