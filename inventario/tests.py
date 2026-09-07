from django.test import TestCase, Client
from django.urls import reverse
from decimal import Decimal
from inventario.models import Categoria, Producto, Movimiento


class CategoriaModelTest(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(
            nombre="Bebidas",
            descripcion="Bebidas y refrescos"
        )

    def test_creacion_categoria(self):
        self.assertEqual(self.categoria.nombre, "Bebidas")
        self.assertEqual(self.categoria.descripcion, "Bebidas y refrescos")
        self.assertEqual(str(self.categoria), "Bebidas")


class ProductoModelTest(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(nombre="Almacen")
        self.producto = Producto.objects.create(
            nombre="Arroz 1kg",
            categoria=self.categoria,
            precio=Decimal("1500.50"),
            stock=10,
            activo=True
        )

    def test_creacion_producto(self):
        self.assertEqual(self.producto.nombre, "Arroz 1kg")
        self.assertEqual(self.producto.stock, 10)
        self.assertEqual(self.producto.precio, Decimal("1500.50"))
        self.assertTrue(self.producto.activo)
        self.assertEqual(str(self.producto), "Arroz 1kg")


class MovimientoModelTest(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(nombre="Lacteos")
        self.producto = Producto.objects.create(
            nombre="Leche Entera",
            categoria=self.categoria,
            precio=Decimal("1200.00"),
            stock=20
        )

    def test_creacion_movimiento(self):
        mov = Movimiento.objects.create(
            producto=self.producto,
            tipo='ENTRADA',
            cantidad=5,
            motivo='Compra proveedor'
        )
        self.assertEqual(mov.tipo, 'ENTRADA')
        self.assertEqual(mov.cantidad, 5)
        self.assertEqual(mov.motivo, 'Compra proveedor')
        self.assertIn("Leche Entera", str(mov))

    def test_movimiento_con_producto_eliminado(self):
        mov = Movimiento.objects.create(
            producto=None,
            tipo='SALIDA',
            cantidad=3,
            motivo='Auditoria'
        )
        self.assertIn("Producto eliminado", str(mov))


class InventarioViewsIntegrationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.categoria = Categoria.objects.create(
            nombre="Limpieza",
            descripcion="Articulos de limpieza"
        )
        self.producto = Producto.objects.create(
            nombre="Detergente 500ml",
            categoria=self.categoria,
            precio=Decimal("850.00"),
            stock=15,
            activo=True
        )

    # CP01: Visualizacion del Dashboard
    def test_dashboard_status_code_y_contexto(self):
        response = self.client.get(reverse('home_admin'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventario/dashboard.html')
        self.assertEqual(response.context['total_productos'], 1)
        self.assertEqual(response.context['alertas_stock_bajo'], 0)

    # CP02: Alta de Categoria
    def test_crear_categoria(self):
        response = self.client.post(reverse('crear_categoria'), {
            'nombre': 'Golosinas',
            'descripcion': 'Chocolates y caramelos'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Categoria.objects.filter(nombre='Golosinas').exists())

    # CP03: Alta de Producto con Stock Inicial (Movimiento ALTA automatico)
    def test_crear_producto_con_stock_inicial(self):
        response = self.client.post(reverse('crear_producto'), {
            'nombre': 'Lavandina 1L',
            'categoria': self.categoria.id,
            'precio': '950.00',
            'stock': '20'
        })
        self.assertEqual(response.status_code, 302)
        prod = Producto.objects.get(nombre='Lavandina 1L')
        self.assertEqual(prod.stock, 20)
        self.assertTrue(Movimiento.objects.filter(producto=prod, tipo='ALTA', cantidad=20).exists())

    # CP04: Modificacion de Producto con Ajuste de Stock
    def test_editar_producto_ajuste_stock(self):
        response = self.client.post(reverse('editar_producto', args=[self.producto.id]), {
            'nombre': 'Detergente Concentrado',
            'categoria': self.categoria.id,
            'precio': '1100.00',
            'stock': '25'  # Subio de 15 a 25 (+10)
        })
        self.assertEqual(response.status_code, 302)
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.stock, 25)
        self.assertEqual(self.producto.nombre, 'Detergente Concentrado')
        self.assertTrue(Movimiento.objects.filter(producto=self.producto, tipo='AJUSTE', cantidad=10).exists())

    # CP05: Baja Logica de Producto (Preservando Trazabilidad)
    def test_eliminar_producto_baja_logica(self):
        # Crear un movimiento previo
        Movimiento.objects.create(
            producto=self.producto,
            tipo='ENTRADA',
            cantidad=5,
            motivo='Stock anterior'
        )
        response = self.client.get(reverse('eliminar_producto', args=[self.producto.id]))
        self.assertEqual(response.status_code, 302)
        self.producto.refresh_from_db()
        self.assertFalse(self.producto.activo)
        # El producto no debe aparecer en el dashboard
        dash_response = self.client.get(reverse('home_admin'))
        self.assertEqual(dash_response.context['total_productos'], 0)
        # El historial de movimientos debe seguir existiendo intacto
        self.assertTrue(Movimiento.objects.filter(producto=self.producto).exists())

    # CP06: Registro de Entrada de Stock
    def test_movimiento_entrada_valida(self):
        response = self.client.post(reverse('movimientos'), {
            'producto': self.producto.id,
            'tipo': 'ENTRADA',
            'cantidad': '10',
            'motivo': 'Factura A-0001'
        })
        self.assertEqual(response.status_code, 302)
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.stock, 25)  # 15 inicial + 10 = 25
        self.assertTrue(Movimiento.objects.filter(
            producto=self.producto,
            tipo='ENTRADA',
            cantidad=10,
            motivo='Factura A-0001'
        ).exists())

    # CP07: Registro de Salida con Stock Suficiente
    def test_movimiento_salida_valida(self):
        response = self.client.post(reverse('movimientos'), {
            'producto': self.producto.id,
            'tipo': 'SALIDA',
            'cantidad': '5',
            'motivo': 'Venta al publico'
        })
        self.assertEqual(response.status_code, 302)
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.stock, 10)  # 15 inicial - 5 = 10
        self.assertTrue(Movimiento.objects.filter(
            producto=self.producto,
            tipo='SALIDA',
            cantidad=5
        ).exists())

    # CP08: Bloqueo de Salida por Stock Insuficiente (REQUISITO CRITICO RF5)
    def test_bloqueo_salida_stock_insuficiente(self):
        stock_inicial = self.producto.stock  # 15
        response = self.client.post(reverse('movimientos'), {
            'producto': self.producto.id,
            'tipo': 'SALIDA',
            'cantidad': '50',  # 50 > 15
            'motivo': 'Venta excesiva rechazada'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.producto.refresh_from_db()
        # El stock NO debe cambiar
        self.assertEqual(self.producto.stock, stock_inicial)
        # NO se debe haber creado ningun movimiento
        self.assertFalse(Movimiento.objects.filter(motivo='Venta excesiva rechazada').exists())
        # El mensaje de error debe alertar stock insuficiente
        self.assertContains(response, 'Stock insuficiente')

    # CP09: Validacion de Cantidad Negativa o Cero
    def test_bloqueo_cantidad_invalida(self):
        response = self.client.post(reverse('movimientos'), {
            'producto': self.producto.id,
            'tipo': 'ENTRADA',
            'cantidad': '-5',
            'motivo': 'Dato invalido'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.stock, 15)
        self.assertContains(response, 'mayor a 0')

    # CP10: Listado de Categorias con Conteo Dinamico
    def test_listar_categorias_con_conteo(self):
        response = self.client.get(reverse('listar_categorias'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Limpieza')
        self.assertContains(response, 'Articulos de limpieza')
