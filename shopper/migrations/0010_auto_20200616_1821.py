# Generated by Django 3.0.5 on 2020-06-16 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopper', '0009_auto_20200614_2310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='saved_product',
            name='link',
            field=models.TextField(),
        ),
    ]
