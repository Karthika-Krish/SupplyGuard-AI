SCENARIO = {
# -------------------------
# BUSINESS OBJECTIVE
# -------------------------
"business_goal": "Maintain service and prevent a stockout",

"product": "Wireless Headphones",

# -------------------------
# INVENTORY
# -------------------------
"inventory": 35,
"initial_inventory": 35,
"daily_demand": 25,

# -------------------------
# CONSTRAINTS
# -------------------------
"recovery_budget": 500,
"max_acceptable_lead_time": 2,
"max_carbon_kg": 15,

# -------------------------
# PRIMARY SUPPLIER
# -------------------------
"current_supplier": "Supplier A",

# -------------------------
# SUPPLIERS
# -------------------------
"suppliers": {
    "Supplier A": {
        "available": False,
        "lead_time_days": 5,
        "cost_per_unit": 12,
        "carbon_per_unit": 0.8,
        "reason": "Supplier disruption"
    },

    "Supplier B": {
        "available": True,
        "lead_time_days": 2,
        "cost_per_unit": 15,
        "carbon_per_unit": 0.6,
    },

    "Warehouse Chennai": {
        "available": True,
        "lead_time_days": 1,
        "cost_per_unit": 18,
        "carbon_per_unit": 0.4,
    }
},

# -------------------------
# SIMULATED SHIPMENT
# -------------------------
"shipment": {
    "status": "delayed",
    "quantity": 15,
    "destination": "Chennai Retail Hub",
    "eta_days": 4
},

# -------------------------
# ROUTES
# -------------------------
"routes": {
    "Route A": {
        "available": False,
        "lead_time_days": 4,
        "cost": 180,
        "carbon_kg": 12,
        "reason": "Route disruption"
    },

    "Route B": {
        "available": True,
        "lead_time_days": 2,
        "cost": 150,
        "carbon_kg": 8
    }
},

# -------------------------
# DEMO CONTROL
# -------------------------
# The first recovery succeeds.
# Then the environment creates a second disruption.
"second_disruption_triggered": False,

"second_disruption": {
    "target": "Warehouse Chennai",
    "type": "shipment_delay",
    "message": "Warehouse Chennai recovery shipment was delayed"
}


}

def reset_scenario():
#Reset the simulated environment before every agent run.
    SCENARIO["inventory"] = SCENARIO["initial_inventory"]


    SCENARIO["shipment"] = {
    "status": "delayed",
    "quantity": 15,
    "destination": "Chennai Retail Hub",
    "eta_days": 4
}

SCENARIO["second_disruption_triggered"] = False

# Restore supplier availability.
SCENARIO["suppliers"]["Supplier A"]["available"] = False
SCENARIO["suppliers"]["Supplier B"]["available"] = True
SCENARIO["suppliers"]["Warehouse Chennai"]["available"] = True

