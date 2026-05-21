from django.urls import path

from . import views

app_name = 'finance'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('expense/new/', views.expense_create, name='expense_create'),
    path('revenue/new/', views.revenue_create, name='revenue_create'),
]
