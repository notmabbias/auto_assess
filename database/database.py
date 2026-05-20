import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'car_data.db')

def getVehicleID(year, make, model):
    # initalize database connection
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # search db for model and make
    cursor.execute("SELECT vehicle_id FROM Vehicles WHERE model=:model AND make=:make AND year=:year", 
                   {'model':model, 'make':make, 'year':year})
    result = cursor.fetchone()

    # print error and return zero on failure
    if (result == None):
        print(f"{year} {make} {model} does not exist in the database.")
        return 0
    # returns as tuple, so store sinlge ID value as int
    vID = result[0]
    
    conn.close()
    return vID

# grab information from database as imperical data for our AI
def getInformation(vID):
    # initalize database connection
    conn = sqlite3.connect(DB_PATH)

    # access columns by name
    conn.row_factory = sqlite3.Row 
    cursor = conn.cursor()

    # store result in dictorinary to be passed into ai
    master_data = {
        "vehicle_metadata": {},
        "maintenance_items": [],
        "known_issues": []
    }

    # fetch vehicle metadata
    cursor.execute("SELECT * FROM Vehicles WHERE vehicle_id = ?", (vID,))
    v_row = cursor.fetchone()
    if v_row:
        # Convert row object to a standard dictionary
        master_data["vehicle_metadata"] = dict(v_row)

    # fetch maintenece records
    cursor.execute("SELECT * FROM Maintenance_Schedules WHERE vehicle_id = ?", (vID,))
    m_rows = cursor.fetchall()
    for row in m_rows:
        master_data["maintenance_items"].append(dict(row))

    # fetch known issues
    cursor.execute("SELECT * FROM Known_Issues WHERE vehicle_id = ?", (vID,))
    i_rows = cursor.fetchall()
    for row in i_rows:
        master_data["known_issues"].append(dict(row))

    conn.close()
    return master_data


def create_pending_search(uuid, make, model, year, listing, carfax):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute('''
            INSERT INTO Saved_Searches (
                uuid,
                input_make,
                input_model,
                input_year,
                raw_ad_text,
                raw_carfax_text,
                ai_analysis_json,
                input_kms
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (uuid, make, model, year, listing, carfax, '{}', -1))
        
        conn.commit()
    except sqlite3.Error as e:
        print(f"[DB ERROR] failed to create pending search for {year} {make} {model}: {e}")
    finally:
        conn.close()

def get_pending_search(uuid):
    # grab data from uuid
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    row = None
    try:
        cursor.execute('''
            SELECT input_make, input_model, input_year, raw_ad_text, raw_carfax_text, ai_analysis_json 
            FROM Saved_Searches WHERE uuid = ?
        ''', (uuid,))
        row = cursor.fetchone()
    except sqlite3.Error as e:
        print(f"[DB ERROR] Query extraction execution failure: {e}")
    finally:
        conn.close()
    return row

def save_ai_result(uuid, ai_json_str):
    # save result from AI after its done (takes a few seconds normally)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute('''
            UPDATE Saved_Searches SET ai_analysis_json = ? WHERE uuid = ?
        ''', (ai_json_str, uuid))
        conn.commit()
    except sqlite3.Error as e:
        print(f"[DB ERROR] Overwrite execution error on save: {e}")
    finally:
        conn.close()

# debug print
def debug_print_car_data(data):
    
    meta = data.get("vehicle_metadata", {})
    print("\n" + "="*60)
    print(f" DIAGNOSTIC DATA: {meta.get('year')} {meta.get('make')} {meta.get('model')}")
    print("="*60)

    print(f"{'[ METADATA ]':<20}")
    print(f" Engine:        {meta.get('engine_type')}")
    print(f" Trans:         {meta.get('transmission_type')}")
    print(f" Drivetrain:    {meta.get('drivetrain')}")
    print(f" Oil Interval:  {meta.get('oil_change_interval_km')} km")
    print("-" * 30)

    print(f"\n{'[ PLANNED MAINTENANCE ]':<30} {'[ INTERVAL ]':>15}")
    for item in data.get("maintenance_items", []):
        task = item.get('task_description')
        km = f"{item.get('interval_km')} km"
        print(f" - {task:<32} {km:>15}")

    print(f"\n{'[ KNOWN ISSUES & RECALLS ]':<40} {'[ SEVERITY ]':>10}")
    for issue in data.get("known_issues", []):
        desc = issue.get('issue_description')
        sev = f"[{issue.get('severity')}]"
        
        if issue.get('is_safety_recall'):
            sev = f"!! RECALL !!"
            
        print(f" ! {desc:<42} {sev:>15}")
    
    print("="*60 + "\n")



# tempID = getVehicleID("2015","Hyundai","Genesis Coupe")

 #if (tempID != 0):
    #debug_print_car_data(getInformation(tempID))
