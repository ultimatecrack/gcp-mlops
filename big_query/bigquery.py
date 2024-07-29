# pip install google-cloud-bigquery

from google.cloud import bigquery

# Authenticate using service account key file (recommended for production)
# Replace 'path/to/your/service_account_key.json' with your actual path
client = bigquery.Client.from_service_account_json('path/to/your/service_account_key.json')

# Alternatively, authenticate using default credentials (used in local development if Google Cloud SDK is installed)
# client = bigquery.Client()

# Define your SQL query
query = """
    SELECT *
    FROM `your_project.your_dataset.your_table`
    LIMIT 10
"""

# Execute the query
query_job = client.query(query)

# Fetch results
results = query_job.result()

# Print results
for row in results:
    print(row)


# Listing Datasets
datasets = list(client.list_datasets())  # List all datasets in the project

for dataset in datasets:
    print(dataset.dataset_id)


# Creating datasets
dataset_id = 'new_dataset'

dataset = bigquery.Dataset(client.dataset(dataset_id))
dataset.location = 'US'  # Specify the location for the dataset (e.g., US)

try:
    dataset = client.create_dataset(dataset)  # Creates the new dataset
    print(f'Dataset {dataset.dataset_id} created.')
except Exception as e:
    print(f'Error creating dataset: {e}')


# Deleting dataset
dataset_id = 'dataset_to_delete'

try:
    client.delete_dataset(dataset_id, delete_contents=True, not_found_ok=True)  # Delete the dataset
    print(f'Dataset {dataset_id} deleted.')
except Exception as e:
    print(f'Error deleting dataset: {e}')

# Handling large results
# Execute a query with large results and save to a destination table
query = """
    SELECT *
    FROM `your_project.your_dataset.your_large_table`
"""

job_config = bigquery.QueryJobConfig(destination='your_project.your_dataset.destination_table')

query_job = client.query(query, job_config=job_config)
query_job.result()  # Wait for the query to finish

# Big query ML
from google.cloud import bigquery

client = bigquery.Client()

# SQL query to create a model
query = """
    CREATE OR REPLACE MODEL `your_project.your_dataset.your_model`
    OPTIONS(model_type='linear_reg') AS
    SELECT
        feature1,
        feature2,
        target
    FROM
        `your_project.your_dataset.training_data`
"""

# Execute the query
query_job = client.query(query)
query_job.result()  # Wait for the query to finish

print('Model created.')


# Overwrite table
external_table_id = 'your_project.your_dataset.your_external_table'
source_table_id = 'your_project.your_dataset.source_table'

external_config = bigquery.ExternalConfig('CSV')
external_config.source_uris = ['gs://your_bucket/path/to/file.csv']
external_config.schema = schema
external_config.skip_leading_rows = 1  # Skip header row if applicable

job_config = bigquery.QueryJobConfig()
job_config.external_config = external_config

# Construct the query to create or replace the external table
query = f"""
    CREATE OR REPLACE TABLE {external_table_id}
    OPTIONS (
        description="Your external table description"
    )
    AS SELECT * FROM {source_table_id}
"""

# Submit the job
query_job = client.query(query, job_config=job_config)

# Wait for the job to complete
query_job.result()

print(f'External table {external_table_id} created or replaced.')


# get data in pandas dataframe
from google.cloud import bigquery
import pandas as pd

# Initialize BigQuery client
client = bigquery.Client.from_service_account_json('path/to/your/service_account_key.json')

# Construct a reference to the dataset and table
dataset_ref = client.dataset('your_dataset')
table_ref = dataset_ref.table('your_table')

# Optionally, you can also directly reference a table using its full path:
# table_ref = client.table('your_project.your_dataset.your_table')

# Construct a query to fetch the data
query = f"""
    SELECT *
    FROM `{table_ref.project}.{table_ref.dataset_id}.{table_ref.table_id}`
"""

# Execute the query and fetch results into a Pandas DataFrame
df = client.query(query).to_dataframe()

# Print the first few rows of the DataFrame to verify
print(df.head())


# Push data from to external table
from google.cloud import bigquery
import pandas as pd

# Initialize BigQuery client
client = bigquery.Client.from_service_account_json('path/to/your/service_account_key.json')

# Example DataFrame (replace with your actual DataFrame)
data = {
    'column1': [1, 2, 3],
    'column2': ['A', 'B', 'C'],
}
df = pd.DataFrame(data)


# Define schema for the external table
schema = [
    bigquery.SchemaField('column1', 'INTEGER'),
    bigquery.SchemaField('column2', 'STRING'),
    # Add more fields as needed
]

# Define external table configuration (CSV format in this example)
external_config = bigquery.ExternalConfig('CSV')
external_config.source_uris = ['gs://your_bucket/path/to/file.csv']
external_config.schema = schema
external_config.skip_leading_rows = 1  # Skip header row if applicable

# Specify job configuration
job_config = bigquery.LoadJobConfig(
    schema=schema,
    source_format=bigquery.SourceFormat.CSV,
    skip_leading_rows=1,
)

# Define the external table ID
external_table_id = 'your_project.your_dataset.your_external_table'

# Load DataFrame into external table
job = client.load_table_from_dataframe(
    df, external_table_id, job_config=job_config
)

# Wait for the job to complete
job.result()  # Waits for the job to complete

print(f'DataFrame successfully loaded into external table {external_table_id}.')


# Creating external table from gcp storage
# Define schema for the external table
schema = [
    bigquery.SchemaField('column1', 'STRING'),
    bigquery.SchemaField('column2', 'INTEGER'),
    # Add more fields as needed
]

# Define external table configuration (CSV format in this example)
external_config = bigquery.ExternalConfig('CSV')
external_config.source_uris = ['gs://your_bucket/path/to/file.csv']
external_config.schema = schema
external_config.skip_leading_rows = 1  # Skip header row if applicable

# Define the external table ID
external_table_id = 'your_project.your_dataset.your_external_table'

# Construct the query to create or replace the external table
query = f"""
    CREATE OR REPLACE TABLE {external_table_id}
    OPTIONS (
        description="Your external table description"
    )
    {external_config.to_api_repr()}
"""

# Submit the job
query_job = client.query(query)

# Wait for the job to complete
query_job.result()

print(f'External table {external_table_id} created or replaced.')