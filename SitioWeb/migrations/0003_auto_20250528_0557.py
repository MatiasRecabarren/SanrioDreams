# Generated by Django 3.1.14 on 2025-05-28 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SitioWeb', '0002_auto_20250528_0554'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='id_producto',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
