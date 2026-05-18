import json
from ai_agent import analyze_vehicle

def run_test():
    mock_db_data = {
        "vehicle_metadata": {
            "year": 2004,
            "make": "Nissan",
            "model": "350Z",
            "engine_type": "3.5L V6 (VQ35DE)",
            "transmission_type": "6-Speed Manual"
        },
        "maintenance_items": [
            {"task_description": "Spark plug replacement & valve cover gasket inspection", "interval_km": 100000},
            {"task_description": "Manual transmission & differential fluid flush", "interval_km": 60000},
            {"task_description": "Engine oil & filter change", "interval_km": 60000}
        ],
        "known_issues": [
            {"issue_description": "High oil consumption due to piston ring wear", "severity": "Medium"},
            {"issue_description": "Early 6-speed manual transmissions (CD001 to CD008) suffer from weak synchronizers causing grinding in 2nd/3rd gear", "severity": "High"},
            {"issue_description": "Valve cover spark plug tube seals leak oil into the spark plug wells", "severity": "Medium"}
        ]
    }

    mock_listing_text = """
    Selling my 2004 350z track project. 185,000 km on the dash. 
    Aero kit installed, lowered on coilovers, cold air intake, and a straight pipe exhaust (sounds crazy loud). 
    AC needs a recharge but heater works great. Sometimes 3rd gear grinds if you shift too fast, but if you take your time it's totally fine. 
    Just put a fresh quart of oil in it last week. Drift ready, just needs a new owner. Text only, no lowballers.
    """

    mock_carfax = """
    - Title State: Saskatchewan
    - Total Owners: 7
    - Accident History: Rear-end collision reported in 2018 ($4,500 repair cost).
    - Status: Active registration, but flag for structural inspection bypass noted in 2022.
    """

    print("[SYSTEM] Transmitting clapped payload to OpenAI...")
    
    result = analyze_vehicle(mock_db_data, mock_listing_text, mock_carfax)

    print("\n[SYSTEM] Payload received. Outputting JSON:\n")
    print(json.dumps(result, indent=4))
    

if __name__ == "__main__":
    run_test()