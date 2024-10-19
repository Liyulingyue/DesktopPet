from machine import Pin, PWM, I2C
import utime
import usys
import time

from ssd1306 import SSD1306_I2C

i2c=I2C(0, scl=Pin(5), sda=Pin(4), freq=100000)
# i2c=I2C(1, scl=Pin(19),sda=Pin(18), freq=100000)

oled = SSD1306_I2C(128, 32, i2c)

servo1 = PWM(Pin(6))
servo1.freq(50)
servo2 = PWM(Pin(7))
servo2.freq(50)

def servo_move(servo, angle):
    # 避免越界
    if angle < 0:
        angle = 0
    if angle > 180:
        angle = 180
    
    max_value = 2.5/20 * 65535
    min_value = 0.5/20 * 65535
    
    target = int(min_value + ((angle / 180) * (max_value - min_value)))
    servo.duty_u16(target)

# is_180 = False

# 程序入口
if __name__ == '__main__':
    servo_move(servo1, 90)
    servo_move(servo2, 30)
    oled.fill(0)
    oled.text("(- w -)hi~", 0, 12)
    oled.show()
    
    while 1:
        data = usys.stdin.read(64)
        
        show_text = data[:32]
        oled.fill(0)
        oled.text(show_text, 0, 12)
        oled.show()
        
        servo_angle_list = data[32:]
        servo_angle_list = servo_angle_list.strip()
        
        for action in servo_angle_list.split(","):
            try:
                servo_id, angle = action.split("-")
                servo_id = int(servo_id)
                angle = int(angle)
                if servo_id == 1:
                    servo_move(servo1, angle)
                elif servo_id == 2:
                    servo_move(servo1, angle)
                time.sleep(0.5)
            except:
                print("fail to run")
        
        servo_move(servo1, 90)
        servo_move(servo2, 30)
        
        
    oled.fill(0)
    oled.text("(~_~)bye~", 0, 12)
    oled.show()

