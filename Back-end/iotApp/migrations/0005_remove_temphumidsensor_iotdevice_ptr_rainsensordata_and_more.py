# Generated by Django 5.1.3 on 2024-11-09 10:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iotApp', '0004_delete_controlsystem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='temphumidsensor',
            name='iotdevice_ptr',
        ),
        migrations.CreateModel(
            name='RainSensorData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_raining', models.BooleanField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('device', models.ForeignKey(limit_choices_to={'device_type': 'RAIN_SENSOR'}, on_delete=django.db.models.deletion.CASCADE, to='iotApp.iotdevice')),
            ],
        ),
        migrations.CreateModel(
            name='TempHumidSensorData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('temperature', models.FloatField()),
                ('humidity', models.FloatField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('device', models.ForeignKey(limit_choices_to={'device_type': 'TEMP_HUMID_SENSOR'}, on_delete=django.db.models.deletion.CASCADE, to='iotApp.iotdevice')),
            ],
        ),
        migrations.DeleteModel(
            name='RainSensor',
        ),
        migrations.DeleteModel(
            name='TempHumidSensor',
        ),
    ]
