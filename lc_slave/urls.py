from django.urls import path

from . import views

urlpatterns = [
    path('stop_instance/', views.stop_instance, name='stop_instance'),
    path('start_instance/', views.start_instance, name='start_instance'),
    path('get_system_resource/', views.get_system_resource, name='get_system_resource'),
    path('get_instance_resource/<str:instance_id>', views.get_instance_resource, name='get_instance_resource')
]
