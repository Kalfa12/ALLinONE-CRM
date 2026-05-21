from django.urls import path

from . import views

app_name = 'pipeline'

urlpatterns = [
    path('', views.kanban, name='kanban'),
    path('product/new/', views.product_create, name='product_create'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('product/<int:pk>/move/', views.product_move, name='product_move'),
]
