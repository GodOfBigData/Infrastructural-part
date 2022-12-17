FROM apache/airflow:2.5.0 as builder

RUN pip install pandas
