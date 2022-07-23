# data_engineering_modern_project

## Acknowledgements

#### Presentation:

This projet aims to integrate data from API (Our source), automate the ELT/ETL pipeline and, visualise the data via a dashboard. Which is a good exemple 
for gathering modern data stacks(2022) together to get an end->end analytics project.

#### Architecture:

![architecture](https://github.com/khalilchaouali/data_engineering_modern_project/blob/main/image/architecture.png)

#### Pipeline Jobs:   
*Source*:\
Our source represneted as an API provided by OPEN DATA PARIS, which has a free data in different topics. Thus,
we have choose the API that works around Schools Establishments more precisly the middle schools in paris.

*ETL*: \
We have consumed our api via Python requests library in which we got semi-structered data (JSON) that'is not suitable for our analysis step. 

For that reason we have modeled and transformed this received data in way that can be used by the next step easly using Pandas, and finally we have stored in 
our document oriented datbase (MongoDB).

*EL*: \
In this step we have add it the most rescent approach in the data engineering aproach which is the ELT, in which we extracted our semi-structered raw data
and loaded it in a structered database using both AIRBYTE and SNOWFLAKE.

*T*:\
After loading the raw data in the snowflake database we have modeled a simple DataWarehouse, in which at each updating our database we detect the incrimented data\
and make some transformation to update our SNOWFLAKE DataWarehouse using SQL.

*Visualisation*: \
now our data are ready for use we have connected snowflake to the google data studio visuliase our data.

*Orchestration*:\
To ensure the automation and the monitoring of our pipeline we have added Airflow orchestration tool to build our pipeline jobs inside a DAG (Directed Acyclec Graph).

## Tech Stack Support

**Storage System:**

MongoDB:[MongoDB Documentation Link](https://www.mongodb.com/docs/)

Snowflake : [Snowflake Documentation Link](https://docs.snowflake.com/en/)

**Orchestrator:**

Airflow: [Mongo Documentation Link](https://airflow.apache.org/docs/apache-airflow/stable/)

**ETL/ELT:**\
Pandas :[Pandas Documentation Link](https://pandas.pydata.org/docs/)

Airbyte:[Airbyte Documentation Link](https://docs.airbyte.com/)

dbt: [dbt Documentation Link](https://www.getdbt.com/)

**Visualisation:**\
Google data studio: [Google data studio Documentation Link](https://developers.google.com/datastudio)

**Deployement:**\
Docker : [Docker Documentation Link](https://docs.docker.com/)

## Config and run project

To run this project we need to Setup the followeng sections.

 #### Requirements:
 
- Install docker and docker compose.

#### Run Locally

Clone the project

```bash
  git clone https://github.com/khalilchaouali/data_engineering_modern_project
```

Go to the project directory

```bash
  cd data_engineering_modern_project
```

Run the whole data stack using ./setup.sh up. This will install local requirements (PyYAML) and run everything though Docker. The script will exit when complete, but the Docker containers will remain running.

```bash
  ./setup.sh up
```
In your browser:

- Visit http://localhost:8080/ to see the Airflow UI (user: `airflow`, password: `airflow`) and to see your DAG.
- Visit http://localhost:8000/ to see the Airbyte UI and your completed Sync.
- Your local MongoDB database (`localhost:2717`) with the `username=admin` and `password=admin` to see the staged and transformed data.

- Configure mongo permissions, install mongo and snowflake connectors images for airbyte, and create mongo database via:

```bash
./setup install
```

#### Config and Variables

- Signup with Snowflake (Free trial).

- Create a new worksheet

- To create a database inside snowflake copy and past the following sql request, then select all the code and finally click on the run buttom: 

![App Screenshot](https://github.com/khalilchaouali/data_engineering_modern_project/blob/main/image/snowflake_run.png)

 ``` sql
-- set variables (these need to be uppercase)
 set airbyte_role = 'AIRBYTE_ROLE';
 set airbyte_username = 'AIRBYTE_USER';
 set airbyte_warehouse = 'AIRBYTE_WAREHOUSE';
 set airbyte_database = 'AIRBYTE_DATABASE';
 set airbyte_schema = 'AIRBYTE_SCHEMA';

 -- set user password
 set airbyte_password = 'password';

 begin;

 -- create Airbyte role
 use role securityadmin;
 create role if not exists identifier($airbyte_role);
 grant role identifier($airbyte_role) to role SYSADMIN;

 -- create Airbyte user
 create user if not exists identifier($airbyte_username)
 password = $airbyte_password
 default_role = $airbyte_role
 default_warehouse = $airbyte_warehouse;

 grant role identifier($airbyte_role) to user identifier($airbyte_username);

 -- change role to sysadmin for warehouse / database steps
 use role sysadmin;

 -- create Airbyte warehouse
 create warehouse if not exists identifier($airbyte_warehouse)
 warehouse_size = xsmall
 warehouse_type = standard
 auto_suspend = 60
 auto_resume = true
 initially_suspended = true;

 -- create Airbyte database
 create database if not exists identifier($airbyte_database);

 -- grant Airbyte warehouse access
 grant USAGE
 on warehouse identifier($airbyte_warehouse)
 to role identifier($airbyte_role);

 -- grant Airbyte database access
 grant OWNERSHIP
 on database identifier($airbyte_database)
 to role identifier($airbyte_role);

 commit;

 begin;

 USE DATABASE identifier($airbyte_database);

 -- create schema for Airbyte data
 CREATE SCHEMA IF NOT EXISTS identifier($airbyte_schema);

 commit;

 begin;

 -- grant Airbyte schema access
 grant OWNERSHIP
 on schema identifier($airbyte_schema)
 to role identifier($airbyte_role);

 commit;
 ```
- create a profiles.yml file inside `data_engineering_modern_project/dbt` directory then past the following code by changing the account value by your snowflake account id:

You can get the accountID from the snowflake home link 
for this exemple:

https://app.snowflake.com/europe-west4.gcp/sd5454/worksheets

account: sd5454.europe-west4.gcp

```yml
my-snowflake-db:
  target: dev
  outputs:
    dev:
      type: snowflake
      account: xxx.xxx.xxx

      # User/password auth
      user: AIRBYTE_USER

      password: password

      role: AIRBYTE_ROLE

      database: AIRBYTE_DATABASE

      warehouse: AIRBYTE_WAREHOUSE

      schema: SCHOOL
      threads: 1
      client_session_keep_alive: False

      # optional
      connect_retries: 0 # default 0
      connect_timeout: 10 # default: 10
      retry_on_database_errors: False # default: false 
      retry_all: False  # default: false
```


-Without all of them you can check you dashboard via this link [Google Data Studio dashboard](https://datastudio.google.com/reporting/b77d69fd-552d-43b7-a0ba-165329766245/page/Xg0xC)



## Demo
Let's start:

1 -Go to http://localhost:8000/ 

2- Create connection between source(Mongo) and Destination(Snowflake), finally get the conn_id from the link path in our case is *a1a4d9a8-3315-479b-84c6-306e994bb615*

![App Screenshot](https://github.com/khalilchaouali/data_engineering_modern_project/blob/main/image/airbyte_interface.png)

3- Rin the command below and then enter the copied conn id and automatically will be add it to airflow
```bash
  echo "Access Airbyte at http://localhost:8000 and set up a connection."
  echo "Enter your Airbyte connection ID: "
  read connection_id
  # Set connection ID for DAG.
  docker-compose -f docker-compose-airflow.yaml --env-file ./.env.airflow run airflow-webserver airflow variables set 'AIRBYTE_CONNECTION_ID' "$connection_id"
```
4- Go to  [http://127.0.0.1:8080/variable/list/](http://127.0.0.1:8080/variable/list/) to check our variable

![App Screenshot](https://github.com/khalilchaouali/data_engineering_modern_project/blob/main/image/variableList.png)

4- Go to this link  [http://127.0.0.1:8080/connection/list/](http://127.0.0.1:8080/connection/list/) to check our connection with snowflake
5[App Screenshot](https://github.com/khalilchaouali/data_engineering_modern_project/blob/main/image/connectionList.png)

6- trigger your task manualy to see you result with the scudeling but it's scheduled @daily in our work. besides, monitor your jobs status.

![App Screenshot](https://github.com/khalilchaouali/data_engineering_modern_project/blob/main/image/airflow.png)

7- check your snowflake update.

![App Screenshot](https://github.com/khalilchaouali/data_engineering_modern_project/blob/main/image/snowflake.png)

8- open your dashboard.
![App Screenshot](https://github.com/khalilchaouali/data_engineering_modern_project/blob/main/image/dashboard.png)

View [Dashboard](https://datastudio.google.com/reporting/b77d69fd-552d-43b7-a0ba-165329766245/page/Xg0xC)

IT'S WORKS!

**Shut it down**

Run `./setup.sh down` to stop the Docker containers.


