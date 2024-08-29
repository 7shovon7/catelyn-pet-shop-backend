import os
import datetime
import boto3
from django.core.management.base import BaseCommand
from django.conf import settings
from botocore.exceptions import NoCredentialsError

class Command(BaseCommand):
    help = 'Backup the database and media files'

    def handle(self, *args, **kwargs):
        # Check if the backup dir exists
        backup_dir = settings.DB_BACKUP_DIR
        if backup_dir is None or not os.path.exists(backup_dir):
            self.stdout.write(self.style.ERROR(f'Error: "{backup_dir}" directory doesn\'t exist!'))
            return
        
        # Database Backup
        today = datetime.date.today().strftime('%Y%m%d')
        db_name = settings.DATABASES['default']['NAME']
        db_user = settings.DATABASES['default']['USER']
        db_pass = settings.DATABASES['default']['PASSWORD']
        db_host = settings.DATABASES['default']['HOST'] or 'localhost'
        db_port = settings.DATABASES['default']['PORT'] or '5432'

        db_backup_file = os.path.join(backup_dir, f'{db_name}_{today}.sql')

        command = f"pg_dump -h {db_host} -p {db_port} -U {db_user} -F c -b -v -f {db_backup_file} {db_name}"
        os.environ['PGPASSWORD'] = db_pass

        try:
            os.system(command)
            self.stdout.write(self.style.SUCCESS(f'Successfully backed up database to {db_backup_file}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))

        # Files Backup
        media_backup_dir = os.path.join(backup_dir, f'media_{today}')
        print(settings.DEFAULT_FILE_STORAGE == 'storages.backends.s3boto3.S3Boto3Storage')

        if settings.DEFAULT_FILE_STORAGE == 'storages.backends.s3boto3.S3Boto3Storage':
            self.backup_s3_media_files(media_backup_dir)
        else:
            os.system(f'cp -r {settings.MEDIA_ROOT} {media_backup_dir}')
            self.stdout.write(self.style.SUCCESS(f'Successfully backed up media files to {media_backup_dir}'))

    def backup_s3_media_files(self, media_backup_dir):
        if not os.path.exists(media_backup_dir):
            os.makedirs(media_backup_dir)

        s3_client = boto3.client('s3')
        bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        media_prefix = settings.MEDIA_URL.lstrip('/')
        
        try:
            paginator = s3_client.get_paginator('list_objects_v2')
            for page in paginator.paginate(Bucket=bucket_name, Prefix=media_prefix):
                print(page)
                if 'Contents' in page:
                    for obj in page['Contents']:
                        file_key = obj['Key']
                        relative_path = file_key[len(media_prefix):].lstrip('/')
                        local_file_path = os.path.join(media_backup_dir, relative_path)
                        local_dir = os.path.dirname(local_file_path)
                        
                        self.stdout.write(self.style.SUCCESS(f'media_prefix: {media_prefix}'))
                        self.stdout.write(self.style.SUCCESS(f'relative_path: {relative_path}'))
                        self.stdout.write(self.style.SUCCESS(f'local_file_path: {local_file_path}'))
                        
                        self.stdout.write(self.style.SUCCESS(f'Processing S3 key: {file_key}'))

                        if not os.path.exists(local_dir):
                            os.makedirs(local_dir)
                        
                        s3_client.download_file(bucket_name, file_key, local_file_path)
                        self.stdout.write(self.style.SUCCESS(f'Downloaded {file_key} to {local_file_path}'))
            self.stdout.write(self.style.SUCCESS(f'Successfully backed up S3 media files to {media_backup_dir}'))
        except NoCredentialsError:
            self.stdout.write(self.style.ERROR(f'Error: AWS credentials not found.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))
