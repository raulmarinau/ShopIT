# Generated by Django 3.0.5 on 2020-06-14 19:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shopper', '0006_delete_searched_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='saved_product_info',
            name='product_base',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='infos', to='shopper.Saved_Product'),
        ),
    ]
