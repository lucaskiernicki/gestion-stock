from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib import messages
from django.db import transaction
from .models import Producto, Categoria, Movimiento


# VISTA PRINCIPAL - DASHBOARD
def home_admin(request):
    productos = Producto.objects.filter(activo=True).select_related('categoria')
    total_productos = productos.count()
    alertas_stock_bajo = productos.filter(stock__lte=2).count()
    movimientos_hoy = Movimiento.objects.filter(fecha__date=timezone.now().date()).count()
    recent_movements = Movimiento.objects.select_related('producto').order_by('-fecha')[:5]
    movimientos_recientes = recent_movements

    contexto = {
        'productos': productos,
        'total_productos': total_productos,
        'alertas_stock_bajo': alertas_stock_bajo,
        'movimientos_hoy': movimientos_hoy,
        'recent_movements': recent_movements,
        'movimientos_recientes': movimientos_recientes,
    }
    return render(request, 'inventario/dashboard.html', contexto)


# LOGICA PARA CREAR ARTICULOS (ALTA)
def crear_producto(request):
    categorias_disponibles = Categoria.objects.all()

    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        categoria_id = request.POST.get('categoria')
        categoria_objeto = get_object_or_404(Categoria, id=categoria_id)

        precio_raw = request.POST.get('precio', '0')
        stock_raw = request.POST.get('stock', '0')
        try:
            precio_val = float(precio_raw)
        except (TypeError, ValueError):
            precio_val = 0.0
        try:
            stock_val = int(stock_raw)
        except (TypeError, ValueError):
            stock_val = 0

        with transaction.atomic():
            nuevo_producto = Producto.objects.create(
                nombre=nombre,
                categoria=categoria_objeto,
                precio=precio_val,
                stock=stock_val,
                activo=True,
            )

            # Si se inicia con stock, se registra el movimiento de ALTA
            if stock_val > 0:
                Movimiento.objects.create(
                    producto=nuevo_producto,
                    tipo='ALTA',
                    cantidad=stock_val,
                    motivo='Carga inicial de producto en inventario'
                )

        messages.success(request, f'¡Producto "{nuevo_producto.nombre}" registrado exitosamente!')
        return redirect('home_admin')

    return render(request, 'inventario/crear_producto.html', {
        'categorias': categorias_disponibles,
        'producto': None,
    })


# LOGICA PARA EDITAR ARTICULOS (MODIFICACION)
def editar_producto(request, id):
    producto = get_object_or_404(Producto, id=id, activo=True)

    if request.method == 'POST':
        try:
            stock_nuevo = int(request.POST.get('stock', 0))
        except (TypeError, ValueError):
            stock_nuevo = producto.stock

        stock_viejo = producto.stock

        producto.nombre = request.POST.get('nombre')
        producto.categoria = get_object_or_404(Categoria, id=request.POST.get('categoria'))
        producto.precio = request.POST.get('precio')

        with transaction.atomic():
            # Si el usuario modificó manualmente el stock en la edición, registramos el ajuste
            if stock_nuevo > stock_viejo:
                diferencia = stock_nuevo - stock_viejo
                Movimiento.objects.create(
                    producto=producto,
                    tipo='AJUSTE',
                    cantidad=diferencia,
                    motivo=f'Ajuste manual (+{diferencia}) desde edición de producto'
                )
            elif stock_nuevo < stock_viejo:
                diferencia = stock_viejo - stock_nuevo
                Movimiento.objects.create(
                    producto=producto,
                    tipo='AJUSTE',
                    cantidad=diferencia,
                    motivo=f'Ajuste manual (-{diferencia}) desde edición de producto'
                )

            producto.stock = stock_nuevo
            producto.save()

        messages.warning(request, f'Los datos del producto "{producto.nombre}" fueron actualizados.')
        return redirect('home_admin')

    categorias = Categoria.objects.all()
    contexto = {'producto': producto, 'categorias': categorias}
    return render(request, 'inventario/crear_producto.html', contexto)


# LOGICA PARA ELIMINAR ARTICULOS (BAJA LOGICA)
def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    # Baja lógica: no borramos el registro físicamente para preservar el historial de movimientos
    producto.activo = False
    producto.save()
    messages.error(request, f'El producto "{producto.nombre}" fue dado de baja del sistema.')
    return redirect('home_admin')


# VISTA DE HISTORIAL Y REGISTRO DE MOVIMIENTOS
def movimientos(request):
    if request.method == 'POST':
        producto_id = request.POST.get('producto')
        tipo = request.POST.get('tipo')
        cantidad_raw = request.POST.get('cantidad', '0')
        motivo = request.POST.get('motivo', '').strip()

        try:
            cantidad = int(cantidad_raw)
        except (TypeError, ValueError):
            cantidad = 0

        if not producto_id or cantidad <= 0:
            messages.error(request, 'Debe seleccionar un producto e ingresar una cantidad mayor a 0.')
            return redirect('movimientos')

        if tipo not in ['ENTRADA', 'SALIDA']:
            messages.error(request, 'Tipo de movimiento inválido.')
            return redirect('movimientos')

        producto = get_object_or_404(Producto, id=producto_id, activo=True)

        with transaction.atomic():
            # Bloqueamos la fila del producto para actualizar de forma segura
            producto = Producto.objects.select_for_update().get(id=producto.id)

            if tipo == 'SALIDA':
                if cantidad > producto.stock:
                    messages.error(
                        request,
                        f'Stock insuficiente para "{producto.nombre}". Stock disponible: {producto.stock} unidades.'
                    )
                    return redirect('movimientos')
                producto.stock -= cantidad
                if not motivo:
                    motivo = 'Salida / Consumo'
            elif tipo == 'ENTRADA':
                producto.stock += cantidad
                if not motivo:
                    motivo = 'Entrada / Reposición'

            producto.save()

            Movimiento.objects.create(
                producto=producto,
                tipo=tipo,
                cantidad=cantidad,
                motivo=motivo
            )

        messages.success(
            request,
            f'¡Movimiento registrado con éxito! Nuevo stock de "{producto.nombre}": {producto.stock} unidades.'
        )
        return redirect('movimientos')

    # Solicitud GET: listado completo y productos disponibles para el formulario
    lista_movimientos = Movimiento.objects.select_related('producto').order_by('-fecha')
    productos_disponibles = Producto.objects.filter(activo=True).order_by('nombre')

    return render(request, 'inventario/movimientos.html', {
        'movimientos': lista_movimientos,
        'productos': productos_disponibles,
    })


# FUNCIONALIDAD PARA CATEGORÍAS
def listar_categorias(request):
    """Lista todas las categorías con el conteo de productos activos en cada una"""
    categorias = Categoria.objects.all()
    categorias_con_conteo = []
    for categoria in categorias:
        conteo = Producto.objects.filter(categoria=categoria, activo=True).count()
        categorias_con_conteo.append({
            'id': categoria.id,
            'nombre': categoria.nombre,
            'descripcion': categoria.descripcion or '-',
            'productos': conteo
        })

    return render(request, 'inventario/categorias.html', {'categorias': categorias_con_conteo})


def crear_categoria(request):
    """Crear una nueva categoría"""
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        descripcion = request.POST.get('descripcion', '').strip()
        if nombre:
            Categoria.objects.create(nombre=nombre, descripcion=descripcion)
            messages.success(request, f'Categoría "{nombre}" creada con éxito.')
            return redirect('listar_categorias')

    return render(request, 'inventario/formulario_categoria.html', {'categoria': None})


def editar_categoria(request, id):
    """Editar una categoría existente"""
    categoria = get_object_or_404(Categoria, id=id)

    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        descripcion = request.POST.get('descripcion', '').strip()
        if nombre:
            categoria.nombre = nombre
            categoria.descripcion = descripcion
            categoria.save()
            messages.warning(request, f'Categoría "{nombre}" actualizada.')
            return redirect('listar_categorias')

    return render(request, 'inventario/formulario_categoria.html', {'categoria': categoria})


def eliminar_categoria(request, id):
    """Eliminar una categoría"""
    categoria = get_object_or_404(Categoria, id=id)
    nombre = categoria.nombre
    categoria.delete()
    messages.error(request, f'Categoría "{nombre}" eliminada.')
    return redirect('listar_categorias')
