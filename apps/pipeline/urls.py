from django.urls import path

from . import views

app_name = 'pipeline'

urlpatterns = [
    path('', views.kanban, name='kanban'),
    path('product/new/', views.product_create, name='product_create'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('product/<int:pk>/edit/', views.product_update, name='product_update'),
    path('product/<int:pk>/delete/', views.product_delete, name='product_delete'),
    path('product/<int:pk>/move/', views.product_move, name='product_move'),
    path('campaign/new/', views.campaign_create, name='campaign_create'),
    path('product/<int:product_pk>/campaign/new/', views.campaign_create, name='campaign_create_for_product'),
    path('campaign/<int:pk>/edit/', views.campaign_update, name='campaign_update'),
    path('campaign/<int:pk>/delete/', views.campaign_delete, name='campaign_delete'),
]
