import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'car_data.db')

def initalize_database():
    print("Connecting to sqlite db...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # vehicles table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Vehicles (
            vehicle_id INTEGER PRIMARY KEY AUTOINCREMENT,
            make TEXT NOT NULL,
            model TEXT NOT NULL,
            year INTEGER NOT NULL,
            engine_type TEXT,
            transmission_type TEXT,
            drivetrain TEXT,
            oil_change_interval_km INTEGER NOT NULL,
            UNIQUE(make, model, year)
        )
    ''')

    # maintenance schedules table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Maintenance_Schedules (
            schedule_id INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicle_id INTEGER NOT NULL,
            task_description TEXT NOT NULL,
            interval_km INTEGER NOT NULL,
            interval_months INTEGER,
            FOREIGN KEY (vehicle_id) REFERENCES Vehicles(vehicle_id) ON DELETE CASCADE
        )
    ''')

    # known issues table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Known_Issues (
            issue_id INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicle_id INTEGER NOT NULL,
            issue_description TEXT NOT NULL,
            severity TEXT NOT NULL,
            is_safety_recall INTEGER NOT NULL DEFAULT 0,
            typical_failure_km_start INTEGER,
            typical_failure_km_end INTEGER,
            FOREIGN KEY (vehicle_id) REFERENCES Vehicles(vehicle_id) ON DELETE CASCADE
        )
    ''')

    # saved searches table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Saved_Searches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            uuid TEXT UNIQUE NOT NULL,
            input_make TEXT NOT NULL,
            input_model TEXT NOT NULL,
            input_year INTEGER NOT NULL,
            input_kms INTEGER NOT NULL,
            raw_ad_text TEXT,
            raw_carfax_text TEXT,
            ai_analysis_json TEXT NOT NULL,
            ai_summary_text TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    print(f"Database successfully initalized at: {DB_PATH}")
    conn.close()

if __name__ == "__main__": # ensure that inialize is only run once
    initalize_database() 