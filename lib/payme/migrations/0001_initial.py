# pylint: disable=invalid-name
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    # pylint: disable=missing-class-docstring
    initial = True
    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(
                    auto_created=True, primary_key=True,
                    serialize=False, verbose_name='ID'
                )),
                ('discount', models.FloatField(blank=True, null=True)),
                ('title', models.CharField(max_length=255)),
                ('price', models.FloatField(blank=True, null=True)),
                ('count', models.IntegerField(default=1)),
                ('code', models.CharField(max_length=17)),
                ('units', models.IntegerField(blank=True, null=True)),
                ('package_code', models.CharField(max_length=255)),
                ('vat_percent', models.IntegerField(blank=True, default=0, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MerchatTransactionsModel',
            fields=[
                ('id', models.BigAutoField(
                    auto_created=True, primary_key=True,
                    serialize=False, verbose_name='ID'
                )),
                ('_id', models.CharField(max_length=255, null=True)),
                ('transaction_id', models.CharField(max_length=255, null=True)),
                ('order_id', models.BigIntegerField(blank=True, null=True)),
                ('amount', models.FloatField(blank=True, null=True)),
                ('time', models.BigIntegerField(blank=True, null=True)),
                ('perform_time', models.BigIntegerField(default=0, null=True)),
                ('cancel_time', models.BigIntegerField(default=0, null=True)),
                ('state', models.IntegerField(default=1, null=True)),
                ('reason', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at_ms', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ShippingDetail',
            fields=[
                ('id', models.BigAutoField(
                    auto_created=True, primary_key=True,
                    serialize=False, verbose_name='ID'
                )),
                ('title', models.CharField(max_length=255)),
                ('price', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('id', models.BigAutoField(
                    auto_created=True, primary_key=True,
                    serialize=False, verbose_name='ID'
                )),
                ('receipt_type', models.IntegerField(default=0)),
                ('items', models.ManyToManyField(to='payme.item')),
                ('shipping', models.ForeignKey(
                    blank=True, null=True,
                    on_delete=django.db.models.deletion.CASCADE,
                    to='payme.shippingdetail'
                )),
            ],
        ),
    ]
