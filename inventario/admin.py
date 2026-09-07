from django.contrib import admin
from .models import Categoria, Producto, Movimiento


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'descripcion')
    search_fields = ('nombre', 'descripcion')
    ordering = ('nombre',)


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'categoria', 'precio', 'stock', 'activo')
    list_filter = ('categoria', 'activo')
    search_fields = ('nombre',)
    ordering = ('nombre',)


@admin.register(Movimiento)
class MovimientoAdmin(admin.ModelAdmin):
    list_display = ('id', 'fecha', 'producto', 'tipo', 'cantidad', 'motivo')
    list_filter = ('tipo', 'fecha')
    search_fields = ('producto__nombre', 'motivo')
    ordering = ('-fecha',)
    readonly_fields = ('fecha',)
