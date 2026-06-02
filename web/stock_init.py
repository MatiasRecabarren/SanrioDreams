"""
Auto-populate Stock data if it doesn't exist
This module ensures Stock records are created on first load
"""

from web.models import Producto, Stock


def ensure_stock_data():
    """Create Stock records if they don't exist"""
    
    STOCK_DATA = [
        (1, 12, "Estante A - Peluches"),
        (2, 8, "Estante A - Peluches"),
        (3, 5, "Estante A - Peluches"),
        (4, 14, "Estante A - Peluches"),
        (5, 9, "Estante A - Peluches"),
        (6, 20, "Estante B - Botellas"),
        (7, 15, "Estante B - Botellas"),
        (8, 11, "Estante B - Botellas"),
        (9, 7, "Estante B - Botellas"),
        (10, 6, "Estante C - Termos"),
        (11, 8, "Estante C - Termos"),
        (12, 10, "Estante C - Termos"),
        (13, 30, "Estante D - Pines"),
        (14, 25, "Estante D - Pines"),
        (15, 18, "Estante D - Pines"),
        (16, 22, "Estante D - Pines"),
        (17, 4, "Estante E - Llaveros"),
        (18, 3, "Estante E - Llaveros"),
    ]
    
    # Only populate if Stock is empty
    if Stock.objects.count() == 0:
        for id_producto, cantidad, ubicacion in STOCK_DATA:
            try:
                producto = Producto.objects.get(id_producto=id_producto)
                Stock.objects.create(
                    producto=producto,
                    cantidad=cantidad,
                    ubicacion_detalle=ubicacion
                )
            except Producto.DoesNotExist:
                pass


class StockInitializationMiddleware:
    """Middleware to ensure Stock data is populated on first request"""
    
    def __init__(self, get_response):
        self.get_response = get_response
        self._initialized = False

    def __call__(self, request):
        if not self._initialized:
            try:
                ensure_stock_data()
                self._initialized = True
            except Exception:
                pass
        
        response = self.get_response(request)
        return response
