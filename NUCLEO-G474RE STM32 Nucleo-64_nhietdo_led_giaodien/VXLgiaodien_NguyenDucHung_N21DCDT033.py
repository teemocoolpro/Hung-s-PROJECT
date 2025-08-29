import tkinter as tk
import serial
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import time

# Thiết lập kết nối với cổng UART
serial_port = serial.Serial('COM6', 115200, timeout=1)

# Danh sách để lưu trữ dữ liệu nhiệt độ và thời gian
temperatures = []
timestamps = []
start_time = time.time()

# Hàm gửi tín hiệu để bật/tắt LED
def toggle_led(led_number, button):
    if button.cget("text") == "Tắt":
        command = chr(ord('a') + led_number).encode()  # Chuyển ký tự thành byte
        button.config(text="Bật", bg="red")  # Đổi màu nút khi tắt
    else:
        command = str(led_number + 1).encode()  # Chuyển số thành byte
        button.config(text="Tắt", bg="green")  # Đổi màu nút khi bật
    serial_port.write(command)  # Gửi dấu hiệu để bật/tắt LED

# Hàm để nhận dữ liệu nhiệt độ từ STM32
def receive_temperature():
    temperature = serial_port.readline().strip().decode()  # Đọc dữ liệu từ cổng UART
    temperature = temperature.split("-")
    
    if len(temperature) == 2:
        temperature_value = float(temperature[0])
        current_time = time.time() - start_time  # Tính thời gian hiện tại dựa trên start_time
        temperatures.append(temperature_value)  # Lưu trữ nhiệt độ
        timestamps.append(current_time)  # Lưu trữ thời gian
        
        temperature_label.config(text=f"Nhiệt độ: {temperature[0]} °C")  # Hiển thị nhiệt độ trên label
        solannhan_label.config(text=f"Số lần nhấn nút: {temperature[1]}")  # Hiển thị số lần nhấn nút trên label
        
        # Cập nhật biểu đồ nhiệt độ
        update_plot()
    
    root.after(100, receive_temperature)  # Lập lịch gọi lại hàm này sau mỗi giây

# Hàm để gửi tín hiệu điều khiển timer
def control_timer(timer_char):
    command = timer_char.encode()  # Chuyển số thành byte
    serial_port.write(command)  # Gửi dấu hiệu để điều khiển timer

# Hàm cập nhật biểu đồ nhiệt độ
def update_plot():
    ax.clear()
    ax.plot(timestamps, temperatures, label="Nhiệt độ")
    ax.set_xlabel('Thời gian (s)')
    ax.set_ylabel('Nhiệt độ (°C)')
    ax.legend()
    canvas.draw()

# Hàm reset thời gian đo nhiệt độ
def reset_time():
    global start_time, temperatures, timestamps
    start_time = time.time()
    temperatures = []
    timestamps = []
    update_plot()

# Tạo cửa sổ giao diện
root = tk.Tk()
root.title("NGUYEN DUC HUNG - N21DCDT033")

# Tạo danh sách để lưu trữ nút điều khiển LED
led_buttons = []

# Hàm tạo nút và kết nối với hàm toggle_led
def create_button(led_number):
    button = tk.Button(root, text=f"Bật", command=lambda idx=led_number: toggle_led(idx, button), width=8, bg="green")
    button.grid(row=led_number // 4, column=led_number % 4, padx=5, pady=5)
    led_buttons.append(button)

# Tạo 8 nút để điều khiển 8 LED
for i in range(8):
    create_button(i)

# Tạo 3 nút để điều khiển các timer
timer_buttons = [
    ("0.5s", 'T'),  # Using 'T' for TIM6
    ("1s", 'U'),  # Using 'U' for TIM7
    ("2s", 'V')   # Using 'V' for TIM3
]

for i, (text, timer_char) in enumerate(timer_buttons):
    button = tk.Button(root, text=text, command=lambda char=timer_char: control_timer(char), width=12)
    button.grid(row=3, column=i, padx=5, pady=5)

# Nút để dừng các timer
stop_button = tk.Button(root, text="Stop Timers", command=lambda: control_timer('r'), width=12)
stop_button.grid(row=3, column=3, padx=5, pady=5)

# Label để hiển thị nhiệt độ
temperature_label = tk.Label(root, text="Nhiệt độ: ", font=("Arial", 12))
temperature_label.grid(row=4, column=0, columnspan=4, pady=5)

# Label để hiển thị số lần nhấn nút
solannhan_label = tk.Label(root, text="Số lần nhấn nút: ", font=("Arial", 12))
solannhan_label.grid(row=5, column=0, columnspan=4, pady=5)

# Tạo biểu đồ nhiệt độ
fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=6, column=0, columnspan=4)

# Nút để reset thời gian đo nhiệt độ
reset_button = tk.Button(root, text="Reset Thời Gian", command=reset_time)
reset_button.grid(row=7, column=0, columnspan=4, pady=5)

# Bắt đầu nhận dữ liệu nhiệt độ
receive_temperature()

# Hiển thị cửa sổ giao diện
root.mainloop()
