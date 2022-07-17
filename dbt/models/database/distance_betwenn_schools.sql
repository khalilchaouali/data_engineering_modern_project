{{ config(materialized='view', schema='DATA_WAREHOUSE' ,alias= 'geo_distance_school') }}
SELECT a._airbyte_data:fields:libelle AS from_school, 
b._airbyte_data:fields:libelle AS to_school,
     Max(111.111 *
    DEGREES(ACOS(LEAST(1.0, COS(RADIANS(a._airbyte_data:geometry:coordinates[0]))
         * COS(RADIANS(b. _airbyte_data:geometry:coordinates[0]))
         * COS(RADIANS(a._airbyte_data:geometry:coordinates[1] - b._airbyte_data:geometry:coordinates[1]))
         + SIN(RADIANS(a. _airbyte_data:geometry:coordinates[0]))
         * SIN(RADIANS(b. _airbyte_data:geometry:coordinates[0])))))) AS distance_in_km
  FROM SCHOOL._AIRBYTE_RAW_SCHOOL AS a
  JOIN SCHOOL._AIRBYTE_RAW_SCHOOL AS b ON a._airbyte_data:fields:libelle <>b._airbyte_data:fields:libelle
  group  by from_school, to_school
