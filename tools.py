from data import SCENARIO

def get_inventory():
    return {
    "product": SCENARIO["product"],
    "inventory": SCENARIO["inventory"]
}

def get_sales_velocity():
    return {
    "product": SCENARIO["product"],
    "daily_demand": SCENARIO["daily_demand"]
}

def calculate_stockout_risk():
    inventory = SCENARIO["inventory"]
    daily_demand = SCENARIO["daily_demand"]

    coverage_days = inventory / daily_demand

    if coverage_days < 2:
        risk = "HIGH"
    elif coverage_days < 5:
        risk = "MEDIUM"
    else:
        risk = "LOW"

    return {
        "inventory": inventory,
        "daily_demand": daily_demand,
        "coverage_days": round(coverage_days, 2),
        "risk": risk
    }


def get_supplier_status(supplier_name):
    supplier = SCENARIO["suppliers"].get(supplier_name)


    if supplier is None:
        return {
          "supplier": supplier_name,
          "available": False,
          "error": "Supplier not found"
    }

    return {
    "supplier": supplier_name,
    "available": supplier["available"],
    "lead_time_days": supplier["lead_time_days"],
    "cost_per_unit": supplier["cost_per_unit"],
    "carbon_per_unit": supplier.get("carbon_per_unit", 0),
    "reason": supplier.get("reason")
}


def get_alternative_suppliers():
    alternatives = []


    for name, supplier in SCENARIO["suppliers"].items():
        if supplier["available"]:
            alternatives.append({
            "supplier": name,
            "lead_time_days": supplier["lead_time_days"],
            "cost_per_unit": supplier["cost_per_unit"],
            "carbon_per_unit": supplier.get("carbon_per_unit", 0)
        })

    return alternatives


def get_shipment_status():
    shipment = SCENARIO["shipment"]


    return {
    "status": shipment["status"],
    "quantity": shipment["quantity"],
    "destination": shipment["destination"],
    "eta_days": shipment["eta_days"]
}


def get_route_status():
    routes = []


    for name, route in SCENARIO["routes"].items():
        routes.append({
        "route": name,
        "available": route["available"],
        "lead_time_days": route["lead_time_days"],
        "cost": route["cost"],
        "carbon_kg": route["carbon_kg"],
        "reason": route.get("reason")
    })

    return routes

def compare_recovery_options(required_units=15):
    options = []


    budget = SCENARIO["recovery_budget"]
    max_lead_time = SCENARIO["max_acceptable_lead_time"]
    max_carbon = SCENARIO["max_carbon_kg"]

    for name, supplier in SCENARIO["suppliers"].items():
        if not supplier["available"]:
            continue

        cost = required_units * supplier["cost_per_unit"]
        carbon = required_units * supplier.get("carbon_per_unit", 0)
        lead_time = supplier["lead_time_days"]

        feasible = (
        cost <= budget
        and lead_time <= max_lead_time
        and carbon <= max_carbon
    )

        options.append({
            "supplier": name,
            "units": required_units,
            "cost": cost,
            "carbon_kg": round(carbon, 2),
            "lead_time_days": lead_time,
            "feasible": feasible
        })

    feasible_options = [
        option
        for option in options
        if option["feasible"]
    ]

    feasible_options.sort(
        key=lambda option: (
            option["lead_time_days"],
            option["cost"],
            option["carbon_kg"]
        )
    )

    selected = feasible_options[0] if feasible_options else None

    return {
        "required_units": required_units,
        "budget": budget,
        "max_lead_time_days": max_lead_time,
        "max_carbon_kg": max_carbon,
        "options": options,
        "selected": selected
    }


def simulate_recovery_action(supplier_name, units):
    supplier = SCENARIO["suppliers"].get(supplier_name)


    if supplier is None:
        return {
        "success": False,
        "error": "Supplier not found"
    }

    if not supplier["available"]:
        return {
        "success": False,
        "error": f"{supplier_name} is unavailable"
    }

    cost = units * supplier["cost_per_unit"]
    carbon = units * supplier.get("carbon_per_unit", 0)

    if cost > SCENARIO["recovery_budget"]:
        return {
        "success": False,
        "error": "Recovery exceeds budget",
        "cost": cost,
        "budget": SCENARIO["recovery_budget"]
    }

    if carbon > SCENARIO["max_carbon_kg"]:
        return {
        "success": False,
        "error": "Recovery exceeds carbon constraint",
        "carbon_kg": round(carbon, 2),
        "max_carbon_kg": SCENARIO["max_carbon_kg"]
    }

    if supplier["lead_time_days"] > SCENARIO["max_acceptable_lead_time"]:
        return {
        "success": False,
        "error": "Recovery lead time is too long",
        "lead_time_days": supplier["lead_time_days"]
    }

    SCENARIO["inventory"] += units

    SCENARIO["shipment"] = {
    "status": "in_transit",
    "quantity": units,
    "destination": "Chennai Retail Hub",
    "eta_days": supplier["lead_time_days"]
}

    if (
    supplier_name == "Warehouse Chennai"
    and not SCENARIO["second_disruption_triggered"]
   ):
        SCENARIO["second_disruption_triggered"] = True
        SCENARIO["shipment"]["status"] = "delayed"
        SCENARIO["shipment"]["eta_days"] = 4

        return {
        "success": True,
        "supplier": supplier_name,
        "units_received": units,
        "cost": cost,
        "carbon_kg": round(carbon, 2),
        "new_inventory": SCENARIO["inventory"],
        "lead_time_days": supplier["lead_time_days"],
        "new_disruption": True,
        "disruption_message": "Warehouse Chennai shipment was delayed"
    }

    return {
    "success": True,
    "supplier": supplier_name,
    "units_received": units,
    "cost": cost,
    "carbon_kg": round(carbon, 2),
    "new_inventory": SCENARIO["inventory"],
    "lead_time_days": supplier["lead_time_days"],
    "new_disruption": False
}


def monitor_environment():
    shipment = SCENARIO["shipment"]


    disruptions = []

    if shipment["status"] == "delayed":
       disruptions.append("Shipment delayed")

    if shipment["eta_days"] > SCENARIO["max_acceptable_lead_time"]:
       disruptions.append("Shipment ETA exceeds service constraint")

    return {
    "inventory": SCENARIO["inventory"],
    "shipment": {
        "status": shipment["status"],
        "quantity": shipment["quantity"],
        "destination": shipment["destination"],
        "eta_days": shipment["eta_days"]
    },
    "disruptions": disruptions,
    "second_disruption_triggered": SCENARIO["second_disruption_triggered"]
}


def verify_recovery(supplier_name, units, cost):
    supplier = SCENARIO["suppliers"].get(supplier_name)


    if supplier is None:
        return {
        "verified": False,
        "reason": "Supplier not found"
    }

    inventory = SCENARIO["inventory"]
    demand = SCENARIO["daily_demand"]
    coverage_days = inventory / demand
    shipment = SCENARIO["shipment"]

    checks = {
    "supplier_available": supplier["available"],
    "inventory_recovered": inventory >= demand * 2,
    "stockout_risk_reduced": coverage_days >= 2,
    "within_budget": cost <= SCENARIO["recovery_budget"],
    "reasonable_lead_time": (
        supplier["lead_time_days"]
        <= SCENARIO["max_acceptable_lead_time"]
    ),
    "shipment_service_ok": (
        shipment["eta_days"]
        <= SCENARIO["max_acceptable_lead_time"]
    )
}

    verified = all(checks.values())

    return {
    "verified": verified,
    "checks": checks,
    "inventory": inventory,
    "coverage_days": round(coverage_days, 2),
    "cost": cost,
    "shipment_status": shipment["status"],
    "shipment_eta_days": shipment["eta_days"]
}
