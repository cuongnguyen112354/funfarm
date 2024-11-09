from django.shortcuts import render
from .models import Device, TempHumidSensorData, RainSensorData
from django.http import JsonResponse

# Create your views here.
def home(request):
   devices = Device.objects.all().values('name', 'status')
   return render(request, 'index.html', { 'devices': devices })

def get_device_status(request):
   devices = Device.objects.all().values('name','status')
   return JsonResponse(list(devices), safe=False)

def get_sensor_data(request):
   temp_humid_sensor = TempHumidSensorData.objects.latest('timestamp')
   rain_sensor = RainSensorData.objects.latest('timestamp')
   return JsonResponse({
      'temperature': temp_humid_sensor.temperature,
      'humidity': temp_humid_sensor.humidity,
      'is_raining': rain_sensor.is_raining
   })

def toggle_device(request):
   if request.method == 'POST':
      device_name = request.POST.get('device')
      device = Device.objects.filter(name=device_name).first()
      if device:
         device.status = 'inactive' if device.status == 'active' else 'active'
         device.save()
         return JsonResponse({'status': device.status})
   return JsonResponse({'error': 'Invalid request'}, status=400)