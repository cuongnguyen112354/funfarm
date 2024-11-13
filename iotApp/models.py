from django.db import models
from django.contrib.auth.models import User

class Land(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lands')
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.name} - Owned by {self.owner.username}"

class Device(models.Model):
    DEVICE_TYPES = [
        ('TEMP_HUMID_SENSOR', 'Cảm biến nhiệt độ, độ ẩm'),
        ('RAIN_SENSOR', 'Cảm biến mưa'),
        ('CONTROL_SYSTEM', 'Hệ thống điều khiển')
    ]

    land = models.ForeignKey(Land, on_delete=models.CASCADE, related_name='devices')
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

    @classmethod
    def create(cls, device, temperature, humidity):
        # Giới hạn số lượng dữ liệu cho mỗi thiết bị là 100 dòng
        if cls.objects.filter(device=device).count() >= 100:
            # Nếu đã có 100 dòng, xóa dòng cũ nhất
            cls.objects.filter(device=device).order_by('timestamp').first().delete()

        # Tạo một dòng dữ liệu mới
        return cls.objects.create(device=device, temperature=temperature, humidity=humidity)

    def __str__(self):
        return f"{self.device.name} - Temperature: {self.temperature}°C, Humidity: {self.humidity}% at {self.timestamp}"


class RainSensorData(models.Model):
    # Khóa ngoại đến bảng Device (chỉ những thiết bị có loại 'RAIN_SENSOR' mới được chọn)
    device = models.ForeignKey('Device', on_delete=models.CASCADE, limit_choices_to={'device_type': 'RAIN_SENSOR'})
    
    # Trạng thái mưa (True hoặc False)
    is_raining = models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add=True)

    @classmethod
    def create(cls, device, is_raining):
        # Giới hạn số lượng dữ liệu cho mỗi thiết bị là 100 dòng
        if cls.objects.filter(device=device).count() >= 100:
            # Nếu đã có 100 dòng, xóa dòng cũ nhất
            cls.objects.filter(device=device).order_by('timestamp').first().delete()

        # Tạo một dòng dữ liệu mới
        return cls.objects.create(device=device, is_raining=is_raining)

    def __str__(self):
        return f"{self.device.name} - Is it raining? {'Yes' if self.is_raining else 'No'} at {self.timestamp}"