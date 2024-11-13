from django.contrib import admin
from .models import Land, Device, TempHumidSensorData, RainSensorData

admin.site.register(Land)
admin.site.register(Device)
admin.site.register(TempHumidSensorData)
admin.site.register(RainSensorData)