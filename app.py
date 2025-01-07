import time
import board
import busio
from adafruit_bme280 import basic as adafruit_bme280
from flask import Flask, jsonify

# On a Raspberry Pi, SPI is usually: board.SCK, board.MOSI, board.MISO
# Chip Select can be any free GPIO, but typically we'll use board.CE0

i2c = busio.I2C(board.SCL, board.SDA)
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, address=0x76)

# Optional: set some parameters
bme280.sea_level_pressure = 1013.25  # hPa at sea level, can adjust as needed

app = Flask(__name__)

@app.route('/')
def index():
    return """
    <h1>Welcome to the Weather Sensor API</h1>
    <p>Get sensor data at <a href="/sensor-data">/sensor-data</a></p>
    """

@app.route('/sensor-data', methods=['GET'])
def get_sensor_data():
    try:
        temperature_c = bme280.temperature
        humidity = bme280.humidity
        pressure = bme280.pressure
        altitude_m = bme280.altitude

        # Convert units
        temperature_f = (temperature_c * 9/5) + 32
        altitude_ft = altitude_m * 3.28084

        data = {
            "temperature_c": round(temperature_c, 1),
            "temperature_f": round(temperature_f, 1),
            "humidity_percent": round(humidity, 1),
            "pressure_hpa": round(pressure, 1),
            "altitude_m": round(altitude_m, 2),
            "altitude_ft": round(altitude_ft, 2)
        }
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    # Run Flask on host='0.0.0.0' so it is accessible from outside the container
    app.run(host='0.0.0.0', port=5000, debug=True)
