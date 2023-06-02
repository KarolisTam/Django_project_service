# Generated by Django 4.2.1 on 2023-06-02 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0014_alter_order_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='customer',
            field=models.CharField(max_length=50, verbose_name='client'),
        ),
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateField(db_index=True, verbose_name='data'),
        ),
        migrations.AlterField(
            model_name='order',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=18, verbose_name='Price'),
        ),
    ]