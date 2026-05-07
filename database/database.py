import sqlite3
import os




def getVehicleID(model, make):
    # initalize database connection
    conn = sqlite3.connect("car_data.db")
    cursor = conn.cursor()

    # search db for model and make
    cursor.execute("SELECT vehicle_id FROM Vehicles WHERE model=:model AND make=:make", 
                   {'model':model, 'make':make})
    result = cursor.fetchone()
    # returns as tuple, so store sinlge ID value as int
    vID = result[0]

    print("year still needs to be implemented")

    conn.close()
    return vID

# 
def getInformation(vID):
    # initalize database connection
    conn = sqlite3.connect("car_data.db")

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


tempID = getVehicleID("350Z","Nissan")


def debug_print_car_data(data):
    """Prints the Master Dictionary in a clean, structured terminal format."""
    
    # 1. Header
    meta = data.get("vehicle_metadata", {})
    print("\n" + "="*60)
    print(f" DIAGNOSTIC DATA: {meta.get('year')} {meta.get('make')} {meta.get('model')}")
    print("="*60)

    # 2. Metadata Section
    print(f"{'[ METADATA ]':<20}")
    print(f" Engine:        {meta.get('engine_type')}")
    print(f" Trans:         {meta.get('transmission_type')}")
    print(f" Drivetrain:    {meta.get('drivetrain')}")
    print(f" Oil Interval:  {meta.get('oil_change_interval_km')} km")
    print("-" * 30)

    # 3. Maintenance Section
    print(f"\n{'[ PLANNED MAINTENANCE ]':<30} {'[ INTERVAL ]':>15}")
    for item in data.get("maintenance_items", []):
        task = item.get('task_description')
        km = f"{item.get('interval_km')} km"
        print(f" - {task:<32} {km:>15}")

    # 4. Known Issues Section
    print(f"\n{'[ KNOWN ISSUES & RECALLS ]':<40} {'[ SEVERITY ]':>10}")
    for issue in data.get("known_issues", []):
        desc = issue.get('issue_description')
        sev = f"[{issue.get('severity')}]"
        
        # Add a flag for recalls
        if issue.get('is_safety_recall'):
            sev = f"!! RECALL !!"
            
        print(f" ! {desc:<42} {sev:>15}")
    
    print("="*60 + "\n")


debug_print_car_data(getInformation(tempID))