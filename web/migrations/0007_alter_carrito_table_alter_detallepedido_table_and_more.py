# Generated by Django 5.2.1 on 2025-05-30 04:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0006_alter_carrito_options_alter_detallepedido_options_and_more'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='carrito',
            table='carrito',
        ),
        migrations.AlterModelTable(
            name='detallepedido',
            table='detallepedido',
        ),
        migrations.AlterModelTable(
            name='empleado',
            table='empleado',
        ),
        migrations.AlterModelTable(
            name='metodopago',
            table='metodopago',
        ),
        migrations.AlterModelTable(
            name='notificacion',
            table='notificacion',
        ),
        migrations.AlterModelTable(
            name='pago',
            table='pago',
        ),
        migrations.AlterModelTable(
            name='pedido',
            table='pedido',
        ),
        migrations.AlterModelTable(
            name='producto',
            table='producto',
        ),
        migrations.AlterModelTable(
            name='resenna',
            table='resenna',
        ),
        migrations.AlterModelTable(
            name='stock',
            table='stock',
        ),
        migrations.AlterModelTable(
            name='tipoempleado',
            table='tipoempleado',
        ),
    ]
