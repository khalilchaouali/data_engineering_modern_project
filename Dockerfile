FROM apache/airflow:latest-python3.8
USER root
COPY requirements.txt /opt/airflow/requirements.txt
WORKDIR /opt/airflow
ENV VIRTUAL_ENV=/dbt-env
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN export PIP_USER=false && pip3 install -r requirements.txt
CMD ["source", "dbt-env/bin/activate"]

