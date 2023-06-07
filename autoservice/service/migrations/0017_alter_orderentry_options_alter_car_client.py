# Generated by Django 4.2.1 on 2023-06-06 05:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('service', '0016_alter_orderentry_options_remove_car_customer_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='orderentry',
            options={'verbose_name': 'order entry', 'verbose_name_plural': 'order entries'},
        ),
        migrations.AlterField(
            model_name='car',
            name='client',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='car', to=settings.AUTH_USER_MODEL, verbose_name='client'),
        ),
    ]