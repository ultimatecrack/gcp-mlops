# pip install google-cloud-storage
from google.cloud import storage

# Initialize GCS client
client = storage.Client.from_service_account_json('path/to/your/service_account_key.json')

# Upload file
def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the GCS bucket."""
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(f'File {source_file_name} uploaded to {destination_blob_name} in bucket {bucket_name}.')


bucket_name = 'your_bucket_name'
source_file_name = 'local_file.txt'
destination_blob_name = 'uploaded_file.txt'

upload_blob(bucket_name, source_file_name, destination_blob_name)


# Download file
def download_blob(bucket_name, source_blob_name, destination_file_name):
    """Downloads a file from the GCS bucket."""
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)

    blob.download_to_filename(destination_file_name)

    print(f'File {source_blob_name} downloaded to {destination_file_name}.')
bucket_name = 'your_bucket_name'
source_blob_name = 'uploaded_file.txt'
destination_file_name = 'downloaded_file.txt'

download_blob(bucket_name, source_blob_name, destination_file_name)


# Listing of files
def list_blobs(bucket_name):
    """Lists all the blobs in the GCS bucket."""
    bucket = client.bucket(bucket_name)
    blobs = bucket.list_blobs()

    print(f'Blobs in bucket {bucket_name}:')
    for blob in blobs:
        print(f'- {blob.name}')

# Example usage
bucket_name = 'your_bucket_name'
list_blobs(bucket_name)

# Deleting object
def delete_blob(bucket_name, blob_name):
    """Deletes a blob from the GCS bucket."""
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    blob.delete()

    print(f'Blob {blob_name} deleted from bucket {bucket_name}.')

# Example usage
bucket_name = 'your_bucket_name'
blob_name = 'uploaded_file.txt'
delete_blob(bucket_name, blob_name)
