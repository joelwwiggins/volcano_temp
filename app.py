import time
import board
import busio
import psycopg2
from adafruit_bme280 import basic as adafruit_bme280
from flask import Flask, jsonify
from apscheduler.schedulers.background import BackgroundScheduler

i2c = busio.I2C(board.SCL, board.SDA)
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, address=0x76)

# Optional: set some parameters
bme280.sea_level_pressure = 1013.25  # hPa at sea level, can adjust as needed

app = Flask(__name__)

# Database connection
conn = psycopg2.connect(
    dbname="weatherdb",
    user="user",
    password="password",
    host="postgres-db"
)

def store_sensor_data():
    temperature_c = bme280.temperature
    humidity = bme280.humidity
    pressure = bme280.pressure
    altitude_m = bme280.altitude

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

    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO sensor_data (temperature_c, temperature_f, humidity_percent, pressure_hpa, altitude_m, altitude_ft) VALUES (%s, %s, %s, %s, %s, %s)",
            (data["temperature_c"], data["temperature_f"], data["humidity_percent"], data["pressure_hpa"], data["altitude_m"], data["altitude_ft"])
        )
        # Keep only the last 1,000,000 rows
        cur.execute("""
            DELETE FROM sensor_data
             WHERE id < (SELECT max(id) - 1000000 FROM sensor_data)
        """)
        conn.commit()

# Execute the SQL script to initialize the database
with conn.cursor() as cur:
    with open('init_db.sql', 'r') as f:
        cur.execute(f.read())
    conn.commit()

# Set up a background scheduler to store data every 5 minutes
scheduler = BackgroundScheduler()
scheduler.add_job(store_sensor_data, 'interval', minutes=5)
scheduler.start()

@app.route('/')
def index():
    return """
    <h1>Welcome to the Weather Sensor API</h1>
    <p>Get sensor data at <a href="/sensor-data">/sensor-data</a></p>
    """

@app.route('/sensor-data', methods=['GET'])
def get_sensor_data():
    try:
        # On-demand sensor reading
        store_sensor_data()
        return jsonify({"message": "Sensor data stored"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    # Run Flask on host='0.0.0.0' so it is accessible from outside the container
    app.run(host='0.0.0.0', port=5000, debug=True)
