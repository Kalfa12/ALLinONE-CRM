from django.urls import path

from . import views

app_name = 'assets'

urlpatterns = [
    path('', views.index, name='index'),
    path('angles/new/', views.angle_create, name='angle_create'),
    path('angles/<int:pk>/edit/', views.angle_update, name='angle_update'),
    path('angles/<int:pk>/delete/', views.angle_delete, name='angle_delete'),
    path('creatives/new/', views.creative_create, name='creative_create'),
    path('creatives/<int:pk>/edit/', views.creative_update, name='creative_update'),
    path('creatives/<int:pk>/delete/', views.creative_delete, name='creative_delete'),
    path('hooks/new/', views.hook_create, name='hook_create'),
    path('hooks/<int:pk>/edit/', views.hook_update, name='hook_update'),
    path('hooks/<int:pk>/delete/', views.hook_delete, name='hook_delete'),
]
