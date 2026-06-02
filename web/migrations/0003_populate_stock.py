# Generated migration to populate Stock data

from django.db import migrations


def populate_stock_data(apps, schema_editor):
    """Populate Stock table with initial data"""
    Producto = apps.get_model('web', 'Producto')
    Stock = apps.get_model('web', 'Stock')
    
    STOCK_DATA = [
        (1, 12, "Estante A - Peluches"),      # Peluche Hello Kitty
        (2, 8, "Estante A - Peluches"),       # Peluche My Melody
        (3, 5, "Estante A - Peluches"),       # Peluche Cinnamoroll
        (4, 14, "Estante A - Peluches"),      # Peluche Kuromi
        (5, 9, "Estante A - Peluches"),       # Peluche Pompompurin
        (6, 20, "Estante B - Botellas"),      # Botella Pompompurin
        (7, 15, "Estante B - Botellas"),      # Botella Pochacco
        (8, 11, "Estante B - Botellas"),      # Botella Hello Kitty
        (9, 7, "Estante B - Botellas"),       # Botella My Melody
        (10, 6, "Estante C - Termos"),        # Termo Cinnamoroll
        (11, 8, "Estante C - Termos"),        # Termo Pompompurin
        (12, 10, "Estante C - Termos"),       # Termo Kuromi
        (13, 30, "Estante D - Pines"),        # Pin Cinnamoroll
        (14, 25, "Estante D - Pines"),        # Pin Pompompurin
        (15, 18, "Estante D - Pines"),        # Pin Kuromi
        (16, 22, "Estante D - Pines"),        # Pin My Melody
        (17, 4, "Estante E - Llaveros"),      # Llavero Cinnamoroll
        (18, 3, "Estante E - Llaveros"),      # Llavero Pompompurin
    ]
    
    for id_producto, cantidad, ubicacion in STOCK_DATA:
        try:
            producto = Producto.objects.get(id_producto=id_producto)
            Stock.objects.get_or_create(
                producto=producto,
                defaults={
                    'cantidad': cantidad,
                    'ubicacion_detalle': ubicacion
                }
            )
        except Producto.DoesNotExist:
            pass


def reverse_populate_stock(apps, schema_editor):
    """Remove populated Stock data"""
    Stock = apps.get_model('web', 'Stock')
    Stock.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_producto_categoria_alter_producto_table'),
    ]

    operations = [
        migrations.RunPython(populate_stock_data, reverse_populate_stock),
    ]
