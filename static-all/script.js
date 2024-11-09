function updateDeviceStatus() {
   fetch('/device-status/')
      .then(response => response.json())
      .then(data => {
         const deviceList = document.getElementById('device-list');
         deviceList.innerHTML = '';

         data.forEach(device => {
            const listItem = document.createElement('li');
            listItem.className = 'device';

            const nameElement = document.createElement('h5');
            nameElement.textContent = device.name;

            const statusElement = document.createElement('span');
            statusElement.className = 'sub_status ' + (device.status === 'active' ? 'active' : 'inactive');
            statusElement.textContent = device.status === 'active' ? 'Active' : 'Inactive';

            listItem.appendChild(nameElement);
            listItem.appendChild(statusElement);

            deviceList.appendChild(listItem);
         });
      })
      .catch(error => console.error('Lỗi khi tải dữ liệu:', error));
}

// Hàm để lấy dữ liệu cảm biến
function fetchSensorData() {
   fetch('/get-sensor-data/')
      .then(response => response.json())
      .then(data => {
         document.getElementById('temp-value').textContent = data.temperature;
         document.getElementById('humidity-value').textContent = data.humidity;
      })
      .catch(error => console.error('Error fetching sensor data:', error));
}

function toggleDevice(deviceName) {
   console.log('Device to toggle:', deviceName)
   fetch('/toggle-device/', {
      method: 'POST',
      headers: {
         'Content-Type': 'application/x-www-form-urlencoded',
         'X-CSRFToken': '{{ csrf_token }}'
      },
      body: 'device=' + deviceName
   })
   .then(response => response.json())
   .catch(error => console.error('Error toggling device:', error));
}


setInterval(updateDeviceStatus, 2000);
window.onload = updateDeviceStatus;

// setInterval(fetchSensorData, 2000);
// window.onload = fetchSensorData;