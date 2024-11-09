from django.db import models

class Device(models.Model):
    DEVICE_TYPES = [
        ('TEMP_HUMID_SENSOR', 'Cảm biến nhiệt độ, độ ẩm'),
        ('RAIN_SENSOR', 'Cảm biến mưa'),
        ('CONTROL_SYSTEM', 'Hệ thống điều khiển')
    ]

    name = models.CharField(max_length=100)
    device_type = models.CharField(max_length=50, choices=DEVICE_TYPES)
    status = models.CharField(max_length=50, default='inactive')
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.device_type} - {self.status}"

class TempHumidSensorData(models.Model):
    # Khóa ngoại đến bảng Device (chỉ những thiết bị có loại 'TEMP_HUMID_SENSOR' mới được chọn)
    device = models.ForeignKey('Device', on_delete=models.CASCADE, limit_choices_to={'device_type': 'TEMP_HUMID_SENSOR'})
    
    # Các giá trị cảm biến nhiệt độ và độ ẩm
    temperature = models.FloatField()
    humidity = models.FloatField()

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.device.name} - Temperature: {self.temperature}°C, Humidity: {self.humidity}% at {self.timestamp}"


class RainSensorData(models.Model):
    # Khóa ngoại đến bảng Device (chỉ những thiết bị có loại 'RAIN_SENSOR' mới được chọn)
    device = models.ForeignKey('Device', on_delete=models.CASCADE, limit_choices_to={'device_type': 'RAIN_SENSOR'})
    
    # Trạng thái mưa (True hoặc False)
    is_raining = models.BooleanField()

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.device.name} - Is it raining? {'Yes' if self.is_raining else 'No'} at {self.timestamp}"