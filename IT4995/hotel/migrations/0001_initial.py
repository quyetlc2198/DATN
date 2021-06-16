# Generated by Django 3.2 on 2021-06-16 03:36

import datetime
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
            name='Categories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('description', models.CharField(default='', max_length=1500)),
                ('description_home', models.CharField(default='', max_length=500)),
                ('image', models.ImageField(default='', upload_to='static/images/categories')),
                ('price_randian', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='images/service')),
                ('link_url', models.CharField(max_length=40)),
                ('description', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Voucher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('discount', models.FloatField(default=0)),
                ('qty', models.IntegerField(default=0)),
                ('description', models.CharField(max_length=100, null=True)),
                ('create_date', models.DateField(default=datetime.date(2021, 6, 16))),
                ('end_date', models.DateField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Rooms',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('status', models.IntegerField(default=0)),
                ('description', models.CharField(default='', max_length=200)),
                ('image', models.ImageField(upload_to='static/images/rooms')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.categories')),
            ],
        ),
        migrations.AddField(
            model_name='categories',
            name='service_list',
            field=models.ManyToManyField(to='hotel.service'),
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_adults', models.IntegerField(default=0)),
                ('number_children', models.IntegerField(default=0)),
                ('arival_date', models.DateField()),
                ('departure_date', models.DateField()),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('CONFIRM', 'Confirm'), ('OCCUPIED', 'Occupied'), ('RETURNED', 'Returned'), ('CANCEL', 'Cancel')], default='PENDING', max_length=10)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.rooms')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('voucher', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hotel.voucher')),
            ],
        ),
    ]
