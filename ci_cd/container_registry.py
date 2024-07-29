from google.cloud import containerregistry_v1 as cr_v1

###########################List Images#####################################
# Initialize the Container Registry client
client = cr_v1.ContainerAnalysisClient()

# Project ID where the repository exists
project_id = 'your-project-id'

# Repository name (e.g., 'my-app')
repository = 'your-repository-name'

# List images in the repository
parent = f'projects/{project_id}/locations/global/repositories/{repository}'
response = client.list_tags(request={"parent": parent})

# Print the list of tags (image versions)
for tag in response.tags:
    print(tag)


###########################Delete Image#####################################
from google.cloud import containerregistry_v1 as cr_v1

# Initialize the Container Registry client
client = cr_v1.ContainerAnalysisClient()

# Project ID where the repository exists
project_id = 'your-project-id'

# Repository name (e.g., 'my-app')
repository = 'your-repository-name'

# Digest of the image to delete (you can also use tag name)
image_digest = 'sha256:1234567890abcdef'

# Construct the image resource name
image_name = f'projects/{project_id}/locations/global/repositories/{repository}/tags/{image_digest}'

# Delete the image
client.delete_tag(name=image_name)
print(f'Image {image_digest} deleted from repository {repository}.')

########################Pushing Docker Image to GCR########################################
from google.auth import impersonated_credentials
from google.auth import default
from google.auth.transport import requests
import google.auth
from google.cloud import containerregistry_v1 as cr_v1
import google

# Initialize the Container Registry client
client = cr_v1.ContainerAnalysisClient()

# Project ID where the repository exists
project_id = 'your-project-id'

# Repository name (e.g., 'my-app')
repository = 'your-repository-name'

# Tag for the Docker image
tag = 'latest'

# Path to the Docker image tarball
image_path = 'path/to/your/docker-image.tar'

# Authenticate using default credentials
# credentials, _ = default()
# client = cr_v1.Client(credentials=credentials)

# Push the Docker image to GCR
parent = f'projects/{project_id}/locations/global/repositories/{repository}'
client.create_tag(parent=parent, tag=tag, tagResource=google.auth)
