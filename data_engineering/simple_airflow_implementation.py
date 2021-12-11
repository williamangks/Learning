# import blocks
from datetime import timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago

# DAG Arguments block
default_args = {
    'owner': 'William Ang',
    'start_date': days_ago(0),
    'email': ['william@testemail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# DAG Definition block
dag = DAG(
    'ETL_Server_Access_Log_Processing',
    default_args=default_args,
    description='Processing ETL Server Access Log',
    schedule_interval=timedelta(days=1), #days=1 means DAG run daily
)

download = BashOperator(
    task_id='dowload',
    bash_command='wget https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0250EN-SkillsNetwork/labs/Apache%20Airflow/Build%20a%20DAG%20using%20Airflow/web-server-access-log.txt',
    dag=dag,
)

extract = BashOperator(
    task_id='extract',
    bash_command='cut -f1,4 -df"#" web-server-access-log.txt > extracted-data.txt',
    dag=dag,
)

transform = BashOperator(
    task_id='transform',
    bash_command='tr "[a-z]" "[A-Z]" < extracted.txt > capitalized.txt',
    dag=dag,
)

load = BashOperator(
    task_id='load',
    bash_command='zip log.zip capitalized.txt',
    dag=dag,
)

# Create pipeline block
download >> extract >> transform >> load


# After that you can run this below line to submit dag to airflow dags list
# cp  ETL_Server_Access_Log_Processing.py $AIRFLOW_HOME/dags
# airflow dags list # To verify if it is submitted successfully
