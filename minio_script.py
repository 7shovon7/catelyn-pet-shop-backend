import os
import boto3
import django
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

# Set up the Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'catelyn_pet_shop.settings')
django.setup()

def migrate_files_to_minio():
    # Initialize S3 client
    s3_client = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        endpoint_url=settings.AWS_S3_ENDPOINT_URL
    )

    local_media_path = os.path.join(settings.BASE_DIR, 'media')
    for root, dirs, files in os.walk(local_media_path):
        for filename in files:
            local_file_path = os.path.join(root, filename)
            relative_path = os.path.relpath(local_file_path, local_media_path)
            with open(local_file_path, 'rb') as file_data:
                file_content = ContentFile(file_data.read())
                default_storage.save(relative_path, file_content)
                print(f'Uploaded {relative_path} to MinIO')

if __name__ == '__main__':
    migrate_files_to_minio()
