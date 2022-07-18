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
 
-Install docker and docker compose.

-pull the images of mongo source connector and snowflake destination connector via:

```bash
docker pull airbyte/destination-snowflake:0.4.31
```

```bash
docker pull airbyte/source-mongodb-v2:0.1.15
```


#### Environment Variables

- Signup with Snowflake (Free trial).

- We need to add the following environment variables to your .env file.

Snowflake:

`SNOWFLAKE_ACCOUNT=lv44893.europe-west4.gcp`

`SNOWFLAKE_WAREHOUSE=AIRBYTE_WAREHOUSE`

`SNOWFLAKE_DATABASE=AIRBYTE_DATABASE`

`SNOWFLAKE_SCHEMA=SCHOOL`

`SNOWFLAKE_USERNAME=AIRBYTE_USER`

`SNOWFLAKE_PASSWORD=password`

`SNOWFLAKE_ROLE=AIRBYTE_ROLE`

#### Run Locally

Clone the project

```bash
  git clone https://github.com/khalilchaouali/data_engineering_modern_project
```

Go to the project directory

```bash
  cd my-project
```

Run the whole data stack using ./tools/start.sh. This will install local requirements (PyYAML) and run everything though Docker. The script will exit when complete, but the Docker containers will remain running.

```bash
  ./setup.sh up
```
In your browser:

- Visit http://localhost:8080/ to see the Airflow UI (user: `airflow`, password: `airflow`) and to see your DAG.
- Visit http://localhost:8000/ to see the Airbyte UI and your completed Sync.
- Visit your local MongoDB database (`localhost:5432`) with the `username=admin` and `password=admin` to see the staged and transformed data.

- Visit your Snowflake account to see the structered tabels and views.

-Without all of them you can check you dashboard via this link [Google Data Studio dashboard](https://datastudio.google.com/reporting/b77d69fd-552d-43b7-a0ba-165329766245/page/Xg0xC)

**Shut it down**

Run `./setup.sh down` to stop the Docker containers.






