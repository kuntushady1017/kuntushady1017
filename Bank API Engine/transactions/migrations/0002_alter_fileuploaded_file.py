# Generated by Django 4.0.2 on 2022-02-21 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fileuploaded',
            name='file',
            field=models.FileField(upload_to='files'),
        ),
    ]
