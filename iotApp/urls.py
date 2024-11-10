from django.urls import path
from . import views

urlpatterns = [
   path('', views.home, name='home'),
   path('device-status/', views.get_device_status, name='device-status'),
   path('get-sensor-data/', views.get_sensor_data, name='get_sensor_data'),
   path('toggle-device/', views.toggle_device, name='toggle_device'),
   path("update_data/", views.update_data, name="update_data"),
]