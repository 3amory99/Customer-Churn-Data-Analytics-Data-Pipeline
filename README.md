# Customer Churn Data Analytics Data Pipeline

Welcome to the Customer Churn Data Analytics Data Pipeline project! This comprehensive Python ETL (Extract, Transform, Load) data engineering endeavor utilizes the power of Apache Airflow and various AWS services, including Glue, S3, and Redshift, to create an end-to-end solution for analyzing customer churn data. The project also seamlessly integrates PowerBI for insightful data visualization.

## Project Overview

In this hands-on project, we delve into the intricacies of building and automating a robust ETL pipeline. The key components of our pipeline include:

- **Apache Airflow:**
  - Open-source orchestration and scheduling platform.
  - Task automation for seamless workflow execution.

- **AWS Glue:**
  - Utilizes Glue Crawler to infer schemas from an AWS S3 bucket.
  - Creates a comprehensive data catalog for efficient data management.
  - Facilitates data loading into an Amazon Redshift data warehouse.

- **AWS S3:**
  - Serves as the source for our data, housing the information to be analyzed.

- **Amazon Redshift:**
  - Acts as the central data warehouse for storing and managing our processed data.

- **PowerBI:**
  - Connects seamlessly to the Redshift cluster for dynamic and interactive data visualization.
  - Provides valuable insights into customer churn patterns.

## Project Workflow

1. **Data Extraction:**
   - AWS Glue Crawler extracts data from the AWS S3 bucket.
   - Schemas are inferred, and a data catalog is created for easy reference.

2. **Data Transformation:**
   - Utilizes Apache Airflow to orchestrate the ETL workflow.
   - Cleansing and transforming data to prepare it for analysis.

3. **Data Loading:**
   - AWS Glue loads the processed data into the Amazon Redshift data warehouse.

4. **Data Visualization:**
   - PowerBI connects to the Redshift cluster for interactive data visualization.
   - Gain valuable insights and detect patterns related to customer churn.

## Project Highlights

- **AWS Cloud Platform:**
  - The entire project is executed on the AWS cloud platform, ensuring scalability and reliability.

- **End-to-End Automation:**
  - Apache Airflow is employed for the orchestration and automation of the entire ETL pipeline.

- **Comprehensive Data Analysis:**
  - Leverage Amazon Athena to write SQL queries on the data catalog for in-depth analysis.

## Getting Started

To dive into the project, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/3amory99/Customer-Churn-Data-Analytics-Data-Pipeline.git
