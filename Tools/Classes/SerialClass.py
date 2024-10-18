import serial


class SerialClass(object):
    def __init__(self):
        super(SerialClass, self).__init__()
        self.ser = None # 初始化串口对象
        self.is_open = False # 初始化串口是否打开的标志
        self.port = None # 初始化串口端口号

    def open_serial(self, serial_port, baud_rate=115200):
        self.port = serial_port

        if self.is_open:
            self.close_serial()
        try:
            self.ser = serial.Serial(serial_port, baud_rate, timeout=1)
            self.is_open = True
            print("Serial port successfully opened on port {}.".format(serial_port))
        except Exception as e:
            print("Error opening serial port:", e)
            self.is_open = False

    def close_serial(self):
        if self.is_open:
            self.ser.close()
            self.is_open = False
            print("Serial port successfully closed.")
        else:
            print("Serial port is already closed.")

    def send_data(self, data):
        if self.is_open:
            try:
                self.ser.write(data.encode('utf-8'))  # encode将字符串转换为字节
            except (serial.SerialTimeoutException, serial.SerialException) as e:
                print("Error sending data:", e)
        else:
            print("Serial port is not opened.")