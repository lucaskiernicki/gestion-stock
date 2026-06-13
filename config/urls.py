from django.contrib import admin
from django.urls import path
from inventario import views  # <-- Importamos tus vistas

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_admin, name='home_admin'),
    path('crear_producto/', views.crear_producto, name='crear_producto'),
    path('editar_producto/<int:id>/', views.editar_producto, name='editar_producto'),
    path('eliminar_producto/<int:id>/', views.eliminar_producto, name='eliminar_producto'),
    path('movimientos/', views.movimientos, name='movimientos'),
    path('registrar_movimiento/', views.movimientos, name='registrar_movimiento'),
]