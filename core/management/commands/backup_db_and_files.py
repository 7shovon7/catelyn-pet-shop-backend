import os
import datetime
from django.core.management.base import BaseCommand
from django.conf import settings

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
        os.system(f'cp -r {settings.MEDIA_ROOT} {media_backup_dir}')
        self.stdout.write(self.style.SUCCESS(f'Successfully backed up media files to {media_backup_dir}'))
