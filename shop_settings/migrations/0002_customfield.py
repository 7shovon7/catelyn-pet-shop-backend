# Generated by Django 5.0.6 on 2024-08-27 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop_settings', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomField',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('key', models.CharField(editable=False, max_length=100, null=True)),
                ('is_required', models.BooleanField(default=False)),
                ('is_private', models.BooleanField(default=False)),
            ],
        ),
    ]
