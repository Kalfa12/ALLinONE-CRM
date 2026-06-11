from django.urls import path

from . import views

app_name = 'finance'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('expense/new/', views.expense_create, name='expense_create'),
    path('expense/<int:pk>/edit/', views.expense_update, name='expense_update'),
    path('expense/<int:pk>/delete/', views.expense_delete, name='expense_delete'),
    path('revenue/new/', views.revenue_create, name='revenue_create'),
    path('revenue/<int:pk>/edit/', views.revenue_update, name='revenue_update'),
    path('revenue/<int:pk>/delete/', views.revenue_delete, name='revenue_delete'),
]
