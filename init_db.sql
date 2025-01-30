DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_tables WHERE tablename = 'sensor_data') THEN
        CREATE TABLE sensor_data (
            id SERIAL PRIMARY KEY,
            temperature_c REAL,
            temperature_f REAL,
            humidity_percent REAL,
            pressure_hpa REAL,
            altitude_m REAL,
            altitude_ft REAL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    END IF;
END $$;