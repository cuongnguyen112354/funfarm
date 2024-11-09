from django.contrib import admin
from .models import Device, TempHumidSensorData, RainSensorData

admin.site.register(Device)
admin.site.register(TempHumidSensorData)
admin.site.register(RainSensorData)