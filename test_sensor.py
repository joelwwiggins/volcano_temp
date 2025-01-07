import board
import busio
from adafruit_bme280 import basic as adafruit_bme280

try:
    i2c = busio.I2C(board.SCL, board.SDA)
    bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, address=0x76)
    print("Temperature:", bme280.temperature)
    print("Humidity:", bme280.humidity)
    print("Pressure:", bme280.pressure)
except Exception as e:
    print("Sensor not detected:", e)
