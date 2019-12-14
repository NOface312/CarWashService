# Generated by Django 3.0 on 2019-12-12 20:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(blank=True, max_length=40, null=True, unique=True)),
                ('firstname', models.CharField(blank=True, max_length=40, null=True)),
                ('secondname', models.CharField(blank=True, max_length=40, null=True)),
                ('city', models.CharField(blank=True, max_length=40, null=True)),
                ('type', models.CharField(blank=True, choices=[('Client', 'Client'), ('Company', 'Company')], max_length=40, null=True)),
                ('active', models.BooleanField(default=True)),
                ('staff', models.BooleanField(default=False)),
                ('admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=255, unique=True)),
                ('location', models.CharField(max_length=255)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('car_type', models.CharField(choices=[('Passenger', 'Passenger'), ('Small jeep', 'Small jeep'), ('Big jeep', 'Big jeep'), ('Gazel(before 1.5t)', 'Gazel(before 1.5t)')], max_length=255)),
                ('price', models.IntegerField()),
                ('example', models.BooleanField(default=False)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.Company')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('statenumber', models.CharField(max_length=255)),
                ('mark', models.CharField(max_length=255)),
                ('model', models.CharField(max_length=255)),
                ('region', models.CharField(max_length=255)),
                ('car_type', models.CharField(choices=[('Passenger', 'Passenger'), ('Small jeep', 'Small jeep'), ('Big jeep', 'Big jeep'), ('Gazel(before 1.5t)', 'Gazel(before 1.5t)')], max_length=255)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]