# Generated by Django 4.2.1 on 2023-06-02 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0009_alter_orderentry_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='cover',
            field=models.ImageField(blank=True, null=True, upload_to='service/car_covers', verbose_name='cover'),
        ),
    ]