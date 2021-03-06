# Generated by Django 3.2.4 on 2021-06-08 13:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EffetSecondaire',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nomLot', models.CharField(max_length=75)),
            ],
        ),
        migrations.CreateModel(
            name='Vaccin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nomVac', models.CharField(max_length=75)),
                ('nbrDoses', models.IntegerField()),
                ('tempsEntreDoses', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Pratiquant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nom', models.CharField(max_length=75)),
                ('Prenom', models.CharField(max_length=75)),
                ('status', models.CharField(max_length=75)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nom', models.CharField(max_length=75)),
                ('Prenom', models.CharField(max_length=75)),
                ('MailPatient', models.CharField(max_length=75)),
                ('TelPatient', models.CharField(max_length=75)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Lot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('noLot', models.IntegerField()),
                ('QuantiteLot', models.IntegerField()),
                ('QteRestante', models.IntegerField()),
                ('Vaccin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Centre.vaccin')),
            ],
        ),
        migrations.CreateModel(
            name='EnregistrerEffet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('EffetSecondaire', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Centre.effetsecondaire')),
                ('Lot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Centre.lot')),
                ('Patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Centre.patient')),
            ],
        ),
        migrations.CreateModel(
            name='Creneau',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('LotUtilise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Centre.lot')),
                ('Patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Centre.patient')),
                ('Pratiquant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Centre.pratiquant')),
            ],
        ),
    ]
