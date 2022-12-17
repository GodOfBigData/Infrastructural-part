import datetime
import pandas as pd
from airflow.decorators import dag, task
from airflow import DAG
from airflow.models.variable import Variable
from airflow.exceptions import AirflowException
from airflow.utils.dates import days_ago
from sqlalchemy import create_engine
from config import  username_db, password_db, addres, port, db, table_get, table_post


def proccess_data():
    try:
        last_timestamp = Variable.get("last_timestamp")
    except Exception:
        last_timestamp = 0
    engine = create_engine(f'postgresql://{username_db}:{password_db}@{addres}:{port}/{db}')
    with engine.connect() as conn:
        try:
            tables = list(conn.execute(f"SELECT table_name FROM information_schema.tables WHERE table_name='{table_post}';").fetchall())
            if len(tables) == 0:
                engine.execute(f"create table {table_post}(time_event character varying," 
                            "timestamp_event integer, id_sensor bigint, coordinates point," 
                            "temp_controller integer, id_controler bigint, name_sensor character varying) distributed by (id_sensor);")
        except Exception as exc:
            print(exc)
        df = pd.read_sql_query(f"SELECT * FROM {table_get} WHERE timestamp_event > {last_timestamp}", conn)
        df = df.loc[df["temp_controller"] >= 0]
        df.sort_values(by='timestamp_event', ascending=False)
        timestamp = df["timestamp_event"].iloc[-1]
        df.to_sql(table_post, conn, schema = "public", if_exists='append', index=False)
        Variable.set("last_timestamp", timestamp)
        


with DAG("DEVICES",
    schedule_interval="*/1 * * * *",
    description="2",
    catchup=False,
    start_date=datetime.datetime(2022, 10, 8)) as dag:
    from airflow.operators.empty import EmptyOperator
    from airflow.operators.python_operator import PythonOperator


    start_step = EmptyOperator(task_id="start_step")

    proccess_data = PythonOperator(task_id="proccess_data", python_callable=proccess_data)

    start_step >> proccess_data
