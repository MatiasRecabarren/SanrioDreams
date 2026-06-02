# 🔧 Instrucciones para Poblar la Tabla Stock

El problema que teníamos es que **los registros de Stock no existían en la base de datos**, aunque los datos de cantidad estaban hardcodeados en el HTML de productos.

## ¿Por qué pasó esto?
- En `productos.html` están hardcodeadas las cantidades (Cantidad: 20, Cantidad: 15, etc.)
- Pero la tabla `Stock` en la BD estaba vacía
- Por eso en `informes_stock` mostraba todo con stock = 0

## ✅ Soluciones disponibles

### Opción 1: Ejecutar desde CMD (MÁS FÁCIL)
```bash
cd C:\Users\matia\OneDrive\Documentos\GitHub\SanrioDreams
python populate_stock.py
```

**Resultado esperado:**
```
Iniciando población de Stock...
============================================================
✅ Creado: Peluche Hello Kitty - Cantidad: 12 en Estante A - Peluches
✅ Creado: Peluche My Melody - Cantidad: 8 en Estante A - Peluches
...
============================================================
Resumen: 18 creados, 0 actualizados
============================================================

✅ Proceso completado exitosamente
```

### Opción 2: Usar Django Shell
```bash
cd C:\Users\matia\OneDrive\Documentos\GitHub\SanrioDreams
python manage.py shell
```

Luego en el shell:
```python
from web.initialize_stock import populate_stock
populate_stock()
```

### Opción 3: Ejecutar archivo batch (Windows)
```bash
populate_stock.bat
```

---

## 📊 ¿Qué hace el script?

El script `populate_stock.py` crea 18 registros de Stock con los datos:

| ID | Producto | Cantidad | Ubicación |
|----|----------|----------|-----------|
| 1 | Peluche Hello Kitty | 12 | Estante A - Peluches |
| 2 | Peluche My Melody | 8 | Estante A - Peluches |
| 3 | Peluche Cinnamoroll | 5 | Estante A - Peluches |
| 4 | Peluche Kuromi | 14 | Estante A - Peluches |
| 5 | Peluche Pompompurin | 9 | Estante A - Peluches |
| 6 | Botella Pompompurin | 20 | Estante B - Botellas |
| 7 | Botella Pochacco | 15 | Estante B - Botellas |
| 8 | Botella Hello Kitty | 11 | Estante B - Botellas |
| 9 | Botella My Melody | 7 | Estante B - Botellas |
| 10 | Termo Cinnamoroll | 6 | Estante C - Termos |
| 11 | Termo Pompompurin | 8 | Estante C - Termos |
| 12 | Termo Kuromi | 10 | Estante C - Termos |
| 13 | Pin Cinnamoroll | 30 | Estante D - Pines |
| 14 | Pin Pompompurin | 25 | Estante D - Pines |
| 15 | Pin Kuromi | 18 | Estante D - Pines |
| 16 | Pin My Melody | 22 | Estante D - Pines |
| 17 | Llavero Cinnamoroll | 4 | Estante E - Llaveros |
| 18 | Llavero Pompompurin | 3 | Estante E - Llaveros |

---

## 🎯 Después de ejecutar el script

✅ Ahora podrás:
1. Ver todos los productos en `informes_stock` con sus cantidades correctas
2. Validar que no se agreguen más items del stock disponible
3. Ver que el stock se descuenta correctamente al pagar

---

## 📝 Archivos creados/modificados

- ✅ `populate_stock.py` - Script Python standalone
- ✅ `populate_stock.bat` - Script batch para Windows
- ✅ `web/initialize_stock.py` - Módulo para importar en Django shell
- ✅ `web/views.py` - Funciones actualizadas:
  - `agregar_al_carrito()` - Valida stock máximo
  - `aumentar_cantidad_carrito()` - Valida stock máximo
  - `pago_exito()` - Descuenta el stock
  - `informes_stock()` - Muestra todos los productos

---

## ⚠️ Si tienes problemas

Si alguno de los scripts falla:
1. Verifica que estés en el directorio correcto
2. Asegúrate de que la BD (`db.sqlite3`) existe
3. Ejecuta: `python manage.py migrate` primero
4. Intenta ejecutar uno de los scripts

¿Necesitas ayuda? Déjame saber!
