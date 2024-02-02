import time

import board
import busio
import digitalio
import adafruit_bme280
import time
# Create library object using our Bus I2C port
#i2c = busio.I2C(board.SCL, board.SDA)
#bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)

# OR create library object using our Bus SPI port
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
fma1_cs = digitalio.DigitalInOut(board.D4)

# change this to match the location's pressure (hPa) at sea level

fma1_cs.direction = digitalio.Direction.OUTPUT
fma1_cs.value= True

while not spi.try_lock():
    pass


spi.configure(baudrate=9600, phase=0, polarity=0)
while(1):
    fma1_cs.value=False
    result=bytearray(1)
    spi.readinto(result)
    fma1_cs.value=True
    print(result)
    time.sleep(1)