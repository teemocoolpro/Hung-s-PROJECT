from flask import Flask, render_template, jsonify
import requests
import time
import threading

app = Flask(__name__)

# Thông tin kết nối đến Home Assistant
HA_URL1 = "http://192.168.2.138:8123/api/states/switch.0xa4c138d7168fb636_l1"
HA_URL2 = "http://192.168.2.138:8123/api/states/switch.0xa4c138d7168fb636_l2"
HA_URL3 = "http://192.168.2.138:8123/api/states/switch.0xa4c138d7168fb636_l3"
HA_URL4 = "http://192.168.2.138:8123/api/states/switch.0xa4c138d7168fb636_l4"

# Thông tin cảm biến nhiệt độ, độ ẩm và áp suất
HA_URL_PRESSURE = "http://192.168.2.138:8123/api/states/sensor.0x54ef441000d1f33a_pressure"
HA_URL_HUMIDITY = "http://192.168.2.138:8123/api/states/sensor.0x54ef441000d1f33a_humidity"
HA_URL_TEMPERATURE = "http://192.168.2.138:8123/api/states/sensor.0x54ef441000d1f33a_temperature"

HEADERS = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiIxY2FiZjUxMzk5ZTg0NGZkYmYxMzI5YTc0NzgwMzNhMCIsImlhdCI6MTcyOTYwMjgwNiwiZXhwIjoyMDQ0OTYyODA2fQ.aS_iRJPbK3tec2iYIgJXf_NxEHyDqZcJeq-ea8QQmt0",
    "Content-Type": "application/json"
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_switch_state1')
def get_switch_state1():
    response = requests.get(HA_URL1, headers=HEADERS)
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": "Could not retrieve state"}), 500

@app.route('/get_switch_state2')
def get_switch_state2():
    response = requests.get(HA_URL2, headers=HEADERS)
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": "Could not retrieve state"}), 500

@app.route('/get_switch_state3')
def get_switch_state3():
    response = requests.get(HA_URL3, headers=HEADERS)
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": "Could not retrieve state"}), 500

@app.route('/get_switch_state4')
def get_switch_state4():
    response = requests.get(HA_URL4, headers=HEADERS)
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": "Could not retrieve state"}), 500

# Thêm các route cho cảm biến nhiệt độ, áp suất, độ ẩm
@app.route('/get_pressure')
def get_pressure():
    response = requests.get(HA_URL_PRESSURE, headers=HEADERS)
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": "Could not retrieve pressure"}), 500

@app.route('/get_humidity')
def get_humidity():
    response = requests.get(HA_URL_HUMIDITY, headers=HEADERS)
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": "Could not retrieve humidity"}), 500

@app.route('/get_temperature')
def get_temperature():
    response = requests.get(HA_URL_TEMPERATURE, headers=HEADERS)
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": "Could not retrieve temperature"}), 500

# Route để bật công tắc
@app.route('/turn_on_switch/<int:switch_number>', methods=['POST'])                            
def turn_on_switch(switch_number):
    url = f"http://192.168.2.138:8123/api/services/switch/turn_on"                                  #sua ip
    data = {
        "entity_id": f"switch.0xa4c138d7168fb636_l{switch_number}"
    }
    response = requests.post(url, headers=HEADERS, json=data)
    if response.status_code == 200:
        return jsonify({"success": True})
    else:
        return jsonify({"error": "Could not turn on switch"}), 500

# Route để tắt công tắc
@app.route('/turn_off_switch/<int:switch_number>', methods=['POST'])
def turn_off_switch(switch_number):
    url = f"http://192.168.2.138:8123/api/services/switch/turn_off"                              #sua ip
    data = {
        "entity_id": f"switch.0xa4c138d7168fb636_l{switch_number}"
    }
    response = requests.post(url, headers=HEADERS, json=data)
    if response.status_code == 200:
        return jsonify({"success": True})
    else:
        return jsonify({"error": "Could not turn off switch"}), 500

# Hàm để lưu dữ liệu vào file
def save_data_to_file():
    file_path = '/home/pi/frontend/data.txt'  # Đặt tên file duy nhất
    while True:
        try:
            # Lấy dữ liệu cảm biến
            temperature_response = requests.get(HA_URL_TEMPERATURE, headers=HEADERS)
            humidity_response = requests.get(HA_URL_HUMIDITY, headers=HEADERS)
            pressure_response = requests.get(HA_URL_PRESSURE, headers=HEADERS)

            # Kiểm tra xem tất cả các phản hồi đều thành công
            if (temperature_response.status_code == 200 and 
                humidity_response.status_code == 200 and 
                pressure_response.status_code == 200):

                temperature = temperature_response.json()
                humidity = humidity_response.json()
                pressure = pressure_response.json()

                # Lưu dữ liệu vào file
                with open(file_path, 'a') as f:
                    f.write(f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}, "
                            f"Temperature: {temperature['state']}°C, "
                            f"Humidity: {humidity['state']}%, "
                            f"Pressure: {pressure['state']} hPa\n")
            else:
                print("Error retrieving sensor data")

            time.sleep(1800)  # Đợi 30 phút
        except Exception as e:
            print(f"Error: {e}")  # In ra lỗi nếu có

if __name__ == '__main__':
    threading.Thread(target=save_data_to_file, daemon=True).start()  # Chạy hàm lưu dữ liệu trong thread riêng
    app.run(host='0.0.0.0', port=5000, debug=True)
