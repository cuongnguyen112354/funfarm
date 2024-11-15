from django.urls import path
from . import views

urlpatterns = [
   # path('', views.loginPage, name='login'),
   # path('logout/', views.logoutPage, name='logout'),

   path('', views.home, name='home'),

   path('device-status/', views.get_device_status, name='device-status'),
   path('get-sensor-data/', views.get_sensor_data, name='get-sensor-data'), 
   path('toggle-device/', views.toggle_device, name='toggle-device'),

   path("update_data/", views.update_data, name="update-data"),
   path("get_data/", views.get_data, name="get-data")
]