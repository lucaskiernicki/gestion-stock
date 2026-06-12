from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto, Categoria, Movimiento

# 1. VISTA PRINCIPAL - DASHBOARD
def home_admin(request):
    productos = Producto.objects.all()
    contexto = {'productos': productos}
    return render(request, 'inventario/dashboard.html', contexto)

# 2. LOGICA PARA CREAR ARTICULOS (ALTA)
def crear_producto(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        categoria_id = request.POST.get('categoria')
        precio = request.POST.get('precio')
        stock = int(request.POST.get('stock', 0))
        
        # Validamos que no esté vacío
        if nombre and categoria_id and precio:
            categoria = Categoria.objects.get(id=categoria_id)
            # Guardamos el producto nuevo en la base de datos
            nuevo_prod = Producto.objects.create(
                nombre=nombre,
                categoria=categoria,
                precio=precio,
                stock=stock
            )
            
            # AUTOMATIZAR HISTORIAL: Como es nuevo, si entra con stock > 0 genera un registro
            if stock > 0:
                Movimiento.objects.create(
                    producto=nuevo_prod,
                    tipo='ENTRADA',
                    cantidad=stock
                )
            return redirect('home_admin')
            
    # Si entran por primera vez, les mandamos las categorías para que elija el desplegable
    categorias = Categoria.objects.all()
    return render(request, 'inventario/formulario_producto.html', {'categorias': categorias})

# 3. LOGICA PARA EDITAR ARTICULOS (MODIFICACION)
def editar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    
    if request.method == 'POST':
        stock_nuevo = int(request.POST.get('stock', 0))
        stock_viejo = producto.stock
        
        # Actualizamos los datos base
        producto.nombre = request.POST.get('nombre')
        producto.categoria = Categoria.objects.get(id=request.POST.get('categoria'))
        producto.precio = request.POST.get('precio')
        
        # AUTOMATIZAR HISTORIAL: Evaluamos si sumó o restó stock real
        if stock_nuevo > stock_viejo:
            diferencia = stock_nuevo - stock_viejo
            Movimiento.objects.create(producto=producto, tipo='ENTRADA', cantidad=diferencia)
        elif stock_nuevo < stock_viejo:
            diferencia = stock_viejo - stock_nuevo
            Movimiento.objects.create(producto=producto, tipo='SALIDA', cantidad=diferencia)
        
        producto.stock = stock_nuevo
        producto.save()
        return redirect('home_admin')
    
    # Si es GET, mostramos el formulario pre-llenado
    categorias = Categoria.objects.all()
    contexto = {'producto': producto, 'categorias': categorias}
    return render(request, 'inventario/formulario_producto.html', contexto)

# 4. LOGICA PARA ELIMINAR ARTICULOS (BAJA)
def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    producto.delete()
    return redirect('home_admin')
