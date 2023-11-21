import pandas as pd
import psycopg2


con = psycopg2.connect(database='Customer_Churn', user='postgres', password='1299',
                       host='127.0.0.1', port='5432')
cur = con.cursor()


cur.execute('SELECT * FROM public."Customer"')
rows = cur.fetchall()
# columns = ['customerid', 'city', 'zip_code', 'gender', 'senior_citizen', 'partner', 'dependents', 'tenure_months', 'phone_service', 'multiple_lines', 'internet_service', 'online_security', 'online_backup', 'device_protection', 'tech_support', 'streaming_tv', 'streaming_movies', 'contract', 'paperless_billing', 'payment_method', 'monthly_charges', 'total_charges', 'churn_label', 'churn_Value', 'churn_score', 'churn_reason']
column_names = [desc[0] for desc in cur.description]

df = pd.DataFrame(data=rows, columns=column_names)
df.head(10)
print(column_names)
# df.to_csv('/home/omar/airflow/dags/Course Project/out.csv')
con.commit()
con.close()



   # transfer_to_s3_task = SqlToS3Operator(
        # task_id='transfer_to_s3',
        # sql='SELECT * FROM public."Customer"',  # Modify the SQL query as needed
        # postgres_conn_id='customer_churn_conn',  # Specify your PostgreSQL connection ID
        # aws_conn_id='aws_s3_conn',  # Specify your AWS connection ID
        # schema='public',  # Specify your schema
        # table='Customer',  # Specify your table
        # filename='Telco_customer_churn2.csv',  # Specify the filename
        # bucket_name='customer-churn-input-bucket',  # Specify your S3 bucket
        # key='s3://customer-churn-input-bucket/Telco_customer_churn2.csv',  # Specify the S3 key
        # delimiter=',',  # Specify the delimiter
        # aws_extra_params={'ServerSideEncryption': 'AES256'},  # Optionally, add extra AWS parameters
        # dag=dag,
        # )
