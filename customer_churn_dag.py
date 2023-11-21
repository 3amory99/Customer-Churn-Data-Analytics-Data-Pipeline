from airflow import DAG
from datetime import timedelta, datetime
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.hooks.base_aws import AwsGenericHook
from airflow.providers.amazon.aws.sensors.glue import GlueJobSensor
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.hooks.S3_hook import S3Hook
import time
import pandas as pd
import psycopg2


con = psycopg2.connect(database='Customer_Churn', user='postgres', password='1299',
                       host='127.0.0.1', port='5432')
print('Database opened successfully')
cur = con.cursor()


def glue_job_s3_redshift_transfer(job_name, **kwargs):
    session = AwsGenericHook(aws_conn_id='aws_s3_conn')                                                            
    boto3_session = session.get_session(region_name='us-east-1')  # Get a client in the same region as the Glue job

    client = boto3_session.client('glue')   # Trigger the job using its name
    client.start_job_run(
        JobName=job_name,
    )

def get_run_id():
    time.sleep(8)
    session = AwsGenericHook(aws_conn_id='aws_s3_conn')
    boto3_session = session.get_session(region_name='us-east-1')
    glue_client = boto3_session.client('glue')
    response = glue_client.get_job_runs(JobName="s3_upload_to_redshift_glue_job")
    job_run_id = response["JobRuns"][0]["Id"]
    return job_run_id 


def upload_to_s3(**kwargs):
    s3_bucket_name = 'customer-churn-input-bucket'
    s3_key = 'Telco_customer_churn2.csv'  # Replace with your desired path and file name
    local_file_path = '/home/omar/airflow/dags/Course Project/out.csv'  # Replace with your local file path
    s3_hook = S3Hook(aws_conn_id='aws_s3_conn')  # Replace with your AWS connection ID
    
    s3_hook.load_file(                       # Upload the file to S3
        filename=local_file_path,
        key=s3_key,
        bucket_name=s3_bucket_name,
        replace=True                         # Set to True if you want to overwrite an existing file
    )
    time.sleep(5)


def ingestDataDB(cur, **kwargs):
    cur.execute('SELECT * FROM public."Customer"')
    rows = cur.fetchall()
    column_names = [desc[0] for desc in cur.description]
    df = pd.DataFrame(data=rows, columns=column_names)
    df.head()
    df.to_csv('/home/omar/airflow/dags/Course Project/out.csv',index=False)
    con.commit()
    con.close()
    time.sleep(5)
     


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 11, 20),
    'email': ['omarmahmoud91999@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(seconds=15)
}

with DAG('Customer_Churn_Dag',
        default_args=default_args,
        schedule = '@daily',
        catchup=False) as dag:

        database_task = PostgresOperator(
        task_id='tsk_database_ingestion',
        postgres_conn_id="customer_churn_conn",
        sql="""
            SELECT * FROM public."Customer"

            """
        )

        database_task_call = PythonOperator(
        task_id='tsk_get_files',
        python_callable=ingestDataDB,
        op_kwargs={
            'cur': cur
        },
        )

        upload_s3_task = PythonOperator(
        task_id='tsk_upload_s3_storage',
        python_callable=upload_to_s3,
        provide_context=True,
        dag=dag,
        )


        glue_job_trigger = PythonOperator(
        task_id='tsk_glue_job_trigger',
        python_callable=glue_job_s3_redshift_transfer,
        op_kwargs={
            'job_name': 's3_upload_to_redshift_glue_job'
        },
        )

        grab_glue_job_run_id = PythonOperator(
        task_id='tsk_grab_glue_job_run_id',
        python_callable=get_run_id,
        )

        is_glue_job_finish_running = GlueJobSensor(
        task_id="tsk_is_glue_job_finish_running",      
        job_name='s3_upload_to_redshift_glue_job',
        run_id='{{task_instance.xcom_pull("tsk_grab_glue_job_run_id")}}',
        verbose=True,  # prints glue job logs in airflow logs
        aws_conn_id='aws_s3_conn',
        poke_interval=60,
        timeout=3600,
        )


        database_task_call >> upload_s3_task 
        database_task >> upload_s3_task 
        upload_s3_task >> glue_job_trigger >> grab_glue_job_run_id >> is_glue_job_finish_running