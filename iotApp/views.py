from django.shortcuts import render
from .models import Land, Device, TempHumidSensorData, RainSensorData
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
# from django.shortcuts import redirect
# from django.contrib.auth import authenticate, login, logout
import json

# def loginPage(request):
#    if request.method == 'POST':
#       username = request.POST['username']
#       password = request.POST['password']
#       user = authenticate(request ,username=username, password=password)
#       if user is not None:
#          login(request, user)
#          return redirect('home')
#       return HttpResponse('Sai thông tin đăng nhập!')
#    else:
#       return render(request, 'login.html')
   
# def logoutPage(request):
#    logout(request)
#    return redirect('login')

def home(request):
   devices = Device.objects.all()
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
      'THtimestamp': temp_humid_sensor.timestamp,
      'is_raining': rain_sensor.is_raining,
      'Rtimestamp': rain_sensor.timestamp
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

@csrf_exempt
def update_data(request):
   if request.method == "POST":
      data = json.loads(request.body)

      try:
         # Lấy và xử lý dữ liệu nhiệt độ và độ ẩm
         temperature = data.get("temperature")
         humidity = data.get("humidity")
         rain = data.get("rain")

         # Lưu dữ liệu cho cảm biến nhiệt độ và độ ẩm (nếu có)
         if temperature is not None or humidity is not None:
            device = Device.objects.get(device_type="TEMP_HUMID_SENSOR")
            TempHumidSensorData.objects.create(
               device=device,
               temperature=temperature if temperature is not None else None,
               humidity=humidity if humidity is not None else None,
            )

         # Lưu dữ liệu cho cảm biến mưa (nếu có)
         if rain is not None:
            device = Device.objects.get(device_type="RAIN_SENSOR")
            RainSensorData.objects.create(
               device=device,
               is_raining=bool(rain)
            )

         return JsonResponse({"status": "success", "data": data})

      except Device.DoesNotExist:
         return JsonResponse({"status": "failed", "error": "No device found for the specified type."}, status=400)

   return JsonResponse({"status": "failed"}, status=400)

def get_data(request):
   pump = Device.objects.filter(name="Pump", device_type="CONTROL_SYSTEM").first()
   servo = Device.objects.filter(name="Servo", device_type="CONTROL_SYSTEM").first()

   data = {
      "pump": 0 if pump.status == 'inactive' else 1,
      "servo": 0 if servo.status == 'inactive' else 1
   }
   return JsonResponse(data)