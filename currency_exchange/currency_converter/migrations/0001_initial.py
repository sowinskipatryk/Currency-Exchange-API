# Generated by Django 4.2.6 on 2023-11-01 08:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=3, unique=True)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ExchangeRate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.DecimalField(decimal_places=4, max_digits=10)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('from_currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_rates', to='currency_converter.currency')),
                ('to_currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_rates', to='currency_converter.currency')),
            ],
        ),
    ]
