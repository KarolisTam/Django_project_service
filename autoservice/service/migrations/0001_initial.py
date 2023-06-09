# Generated by Django 4.2.1 on 2023-05-30 07:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('licence_plate', models.CharField(max_length=20, verbose_name='Licence Plate')),
                ('vin_code', models.CharField(max_length=50, verbose_name='VIN Code')),
                ('customer', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'car',
                'verbose_name_plural': 'cars',
            },
        ),
        migrations.CreateModel(
            name='CarModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('make', models.CharField(max_length=100, verbose_name='Make')),
                ('model', models.CharField(max_length=100, verbose_name='Model')),
                ('year', models.PositiveIntegerField(verbose_name='Year')),
                ('engine', models.CharField(max_length=100, verbose_name='Engine')),
            ],
            options={
                'verbose_name': 'car model',
                'verbose_name_plural': 'car models',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=50, verbose_name='data')),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.car', verbose_name='car')),
            ],
            options={
                'verbose_name': 'order',
                'verbose_name_plural': 'orders',
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('price', models.IntegerField(verbose_name='price')),
            ],
            options={
                'verbose_name': 'service',
                'verbose_name_plural': 'services',
            },
        ),
        migrations.CreateModel(
            name='OrderList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.CharField(max_length=50, verbose_name='quantity')),
                ('price', models.CharField(max_length=50, verbose_name='price')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order', to='service.order')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='service', to='service.service')),
            ],
            options={
                'verbose_name': 'Order List',
                'verbose_name_plural': 'Order Lists',
            },
        ),
        migrations.AddField(
            model_name='car',
            name='car_model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.carmodel', verbose_name='car_model'),
        ),
    ]
