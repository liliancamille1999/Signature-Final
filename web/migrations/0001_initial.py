# Generated by Django 4.1.2 on 2022-10-19 10:28

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
            name='entreprise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('NomE', models.CharField(max_length=255, verbose_name='NomE')),
                ('Secteur', models.CharField(max_length=255, verbose_name='Secteur')),
                ('Region', models.CharField(max_length=255, verbose_name='Region')),
                ('Ville', models.CharField(max_length=255, verbose_name='Ville')),
                ('Unit_name', models.CharField(max_length=255, verbose_name='Unit_name')),
                ('Date_de_creation', models.DateField()),
                ('emailE', models.EmailField(max_length=254)),
                ('telE', models.CharField(max_length=255, verbose_name='TelE')),
            ],
            options={
                'verbose_name': 'Entreprise',
                'ordering': ['-NomE'],
            },
        ),
        migrations.CreateModel(
            name='Personne',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nom', models.CharField(max_length=255, verbose_name='Nom')),
                ('Prenom', models.CharField(max_length=255, verbose_name='Prenom')),
                ('Sexe', models.CharField(max_length=255, verbose_name='Sexe')),
                ('Date_naissance', models.CharField(max_length=255, verbose_name='date')),
                ('email', models.EmailField(max_length=254)),
                ('tel', models.CharField(max_length=255, verbose_name='Tel')),
                ('Entreprise', models.ForeignKey(default=0, on_delete=django.db.models.deletion.SET_DEFAULT, to='web.entreprise')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Personne',
                'ordering': ['-Nom'],
            },
        ),
    ]
