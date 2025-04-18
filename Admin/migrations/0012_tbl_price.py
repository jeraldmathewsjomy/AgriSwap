# Generated by Django 5.1.2 on 2024-12-18 15:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin', '0011_remove_tbl_product_product_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='tbl_price',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price_date', models.DateField(auto_now_add=True)),
                ('price_amount', models.CharField(max_length=50)),
                ('district_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Admin.tbl_district')),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Admin.tbl_product')),
            ],
        ),
    ]
