# Generated by Django 4.2.5 on 2023-10-04 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, default=True, max_digits=10),
            preserve_default=False,
        ),
    ]
