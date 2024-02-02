import time

import board
import busio
import digitalio
import adafruit_bme280
import time
from icm20948 import ICM20948



# OR create library object using our Bus SPI port
i2c = busio.I2C(board.SCL, board.SDA)
fma1_cs = digitalio.DigitalInOut(board.D4)
while not i2c.try_lock():
    pass
[hex(x) for x in i2c.scan()]


imu = ICM20948(0x68,i2c)

#amin = list(imu.read_magnetometer_data())
#amax = list(imu.re
# ad_magnetometer_data())
# change this to match the location's pressure (hPa) at sea level




while True:
    ax, ay, az, gx, gy, gz = imu.read_accelerometer_gyro_data()
  

    print("""
Accel: {:05.2f} {:05.2f} {:05.2f}
Gyro:  {:05.2f} {:05.2f} {:05.2f}""".format(
        ax, ay, az, gx, gy, gz
        ))
    print(" end read.")

    time.sleep(0.25)