# import blocks
from datetime import timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago

# Task 1.1 - Define DAG arguments # dag_args.jpg
# DAG Arguments block
default_args = {
    'owner': 'William_Ang',
    'start_date': days_ago(0),
    'email': ['william@testemail.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Task 1.2 - Define the DAG # dag_definition.jpg
# Defining DAG
dag = DAG(
    'ETL_toll_data',
    default_args=default_args,
    description='Processing Toll Data',
    schedule_interval=timedelta(days=1), #days=1 means DAG run daily
)

# Task 1.3 - Create a task to unzip data # unzip_data.jpg
# Unzip data
unzip_data = BashOperator(
    task_id='unzip_data',
    bash_command='mkdir /home/project/airflow/dags/finalassignment | tar -zxvf tolldata.tgz -C /home/project/airflow/dags/finalassignment',
    dag=dag,
)

# Task 1.4 - Create a task to extract data from csv file # extract_data_from_csv.jpg
# Extract data from csv
extract_data_from_csv = BashOperator(
    task_id='extract_csv',
    bash_command='cut -d "," -f1-4 /home/project/airflow/dags/finalassignment/vehicle-data.csv > /home/project/airflow/dags/finalassignment/staging/csv_data.csv',
    dag=dag,
)

# Task 1.5 - Create a task to extract data from tsv file # extract_data_from_tsv.jpg
# Extract data from tsv
extract_data_from_tsv = BashOperator(
    task_id='extract_tsv',
    bash_command="cut -f5-7 --output-delimiter=',' /home/project/airflow/dags/finalassignment/tollplaza-data.tsv | tr -d '\r' > /home/project/airflow/dags/finalassignment/staging/tsv_data.csv",
    dag=dag,
)

# Task 1.6 - Create a task to extract data from fized width file
# Extract data from fixed width
extract_data_from_fixed_width = BashOperator(
    task_id='extract_fixed_width',
    bash_command='cut -b 59-61,63-67 --output-delimiter="," /home/project/airflow/dags/finalassignment/payment-data.txt > /home/project/airflow/dags/finalassignment/staging/fixed_width_data.csv',
    dag=dag,
)

# Task 1.7 - Create a task to consolidate data extracted from previous tasks # consolidate_data.jpg
# Consolidate data
consolidate_data = BashOperator(
    task_id='consolidate_data',
    bash_command="paste -d, /home/project/airflow/dags/finalassignment/staging/csv_data.csv /home/project/airflow/dags/finalassignment/staging/tsv_data.csv /home/project/airflow/dags/finalassignment/staging/fixed_width_data.csv > /home/project/airflow/dags/finalassignment/staging/extracted_data.csv",
    dag=dag,
)

# Task 1.8 - Transform and load the data # transform.jpg
# Transform and load the data
transform_data = BashOperator(
    task_id='transform_data',
    bash_command='awk -F"," "{ print $1","$2","$3","toupper($4)","$5","$6","$7","$8","$9;}" < /home/project/airflow/dags/finalassignment/staging/extracted_data.csv > /home/project/airflow/dags/finalassignment/staging/transformed_data.csv',
    dag=dag,
)

# Task 1.9 - Define the task pipeline
# Tasks pipeline
unzip_data >> extract_data_from_csv >> extract_data_from_tsv >> extract_data_from_fixed_width >> consolidate_data >> transform_data
