# Generated by Django 3.2.4 on 2021-06-09 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Centre', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='creneau',
            name='dateCreneau',
            field=models.DateTimeField(),
            preserve_default=False,
        ),
    ]
