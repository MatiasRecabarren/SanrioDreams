"""
Script para ejecutar en Django shell:
python manage.py shell < initialize_stock.py

O importar directamente:
from web.initialize_stock import populate_stock
populate_stock()
"""

from web.models import Producto, Stock

def populate_stock():
    """Crea registros de Stock para cada producto"""
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
    
    created_count = 0
    updated_count = 0
    
    for id_producto, cantidad, ubicacion in STOCK_DATA:
        try:
            producto = Producto.objects.get(id_producto=id_producto)
            stock, created = Stock.objects.get_or_create(
                producto=producto,
                defaults={
                    'cantidad': cantidad,
                    'ubicacion_detalle': ubicacion
                }
            )
            
            if created:
                print(f"✅ Creado: {producto.nombre} - Cantidad: {cantidad} en {ubicacion}")
                created_count += 1
            else:
                if stock.cantidad != cantidad:
                    stock.cantidad = cantidad
                    stock.ubicacion_detalle = ubicacion
                    stock.save()
                    print(f"🔄 Actualizado: {producto.nombre} - Cantidad: {cantidad}")
                    updated_count += 1
                else:
                    print(f"⏭️  Sin cambios: {producto.nombre}")
                    
        except Producto.DoesNotExist:
            print(f"⚠️  Producto no encontrado: ID {id_producto}")
    
    print(f"\n{'='*60}")
    print(f"Resumen: {created_count} creados, {updated_count} actualizados")
    print(f"{'='*60}")
    
    return created_count, updated_count

if __name__ == '__main__':
    populate_stock()
