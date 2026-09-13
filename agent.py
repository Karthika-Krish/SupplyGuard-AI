from data import SCENARIO, reset_scenario

from tools import (
    get_inventory,
    get_sales_velocity,
    calculate_stockout_risk,
    get_supplier_status,
    get_alternative_suppliers,
    compare_recovery_options,
    simulate_recovery_action,
    monitor_environment,
    verify_recovery
)

from evaluator import evaluate_agent_run


MAX_ITERATIONS = 15


def create_state():
    return {
        "business_goal": SCENARIO["business_goal"],
        "product": SCENARIO["product"],
        "current_inventory": None,
        "daily_demand": None,
        "stockout_risk": None,
        "initial_stockout_risk": None,
        "final_stockout_risk": None,
        "suppliers_checked": [],
        "supplier_status": {},
        "current_plan": None,
        "observations": [],
        "actions_taken": [],
        "failures": [],
        "replans": [],
        "verification_result": None,
        "recovery_executed": False,
        "final_risk_calculated": False,
        "evaluation_result": None,
        "iteration_count": 0,
        "final_decision": None
    }


def log(state, message):
    print(message)
    state["observations"].append(message)


def choose_best_plan(state):
    result = compare_recovery_options(15)

    state["current_plan"] = result["selected"]

    if result["selected"] is None:
        state["failures"].append("No feasible recovery option")
        return False

    log(
        state,
        f"Selected {result['selected']['supplier']} "
        f"with {result['selected']['lead_time_days']} day lead time"
    )

    return True


def run_agent():
    reset_scenario()

    state = create_state()

    print("\n========================================")
    print("SUPPLYGUARD AI - AUTONOMOUS AGENT")
    print("========================================")

    log(state, f"GOAL: {state['business_goal']}")

    inventory = get_inventory()
    state["current_inventory"] = inventory["inventory"]

    demand = get_sales_velocity()
    state["daily_demand"] = demand["daily_demand"]

    risk = calculate_stockout_risk()
    state["stockout_risk"] = risk["risk"]
    state["initial_stockout_risk"] = risk

    log(
        state,
        f"MONITOR: Inventory {state['current_inventory']}, "
        f"Demand {state['daily_demand']}/day, "
        f"Risk {state['stockout_risk']}"
    )

    current_supplier = SCENARIO["current_supplier"]

    supplier = get_supplier_status(current_supplier)

    state["suppliers_checked"].append(current_supplier)
    state["supplier_status"][current_supplier] = supplier

    if not supplier["available"]:
        state["failures"].append(
            f"{current_supplier} unavailable"
        )

        log(
            state,
            f"DETECT: {current_supplier} unavailable"
        )

    alternatives = get_alternative_suppliers()

    log(
        state,
        f"INVESTIGATE: {len(alternatives)} alternative recovery sources found"
    )

    if not choose_best_plan(state):
        state["final_decision"] = "FAIL"
        return state

    state["replans"].append({
        "reason": "Original supplier unavailable",
        "new_plan": state["current_plan"]
    })

    plan = state["current_plan"]

    log(
        state,
        f"OPTIMIZE: Comparing cost, lead time and carbon"
    )

    log(
        state,
        f"DECISION: Use {plan['supplier']} "
        f"for {plan['units']} units "
        f"at cost {plan['cost']}"
    )

    result = simulate_recovery_action(
        plan["supplier"],
        plan["units"]
    )

    state["actions_taken"].append(result)

    if not result["success"]:
        state["failures"].append(result["error"])
        state["final_decision"] = "FAIL"
        return state

    state["recovery_executed"] = True
    state["current_inventory"] = result["new_inventory"]

    log(
        state,
        f"ACTION: Recovery executed through {plan['supplier']}"
    )

    environment = monitor_environment()

    log(
        state,
        f"MONITOR AGAIN: Shipment status = "
        f"{environment['shipment']['status']}, "
        f"ETA = {environment['shipment']['eta_days']} days"
    )

    if environment["disruptions"]:
        log(
            state,
            "ADAPT: New disruption detected"
        )

        state["failures"].append(
            "Second disruption detected"
        )

        state["replans"].append({
            "reason": "Second shipment disruption",
            "previous_plan": plan
        })

        state["verification_result"] = None

        log(
            state,
            "REPLAN: Previous recovery plan no longer satisfies service constraint"
        )

        alternatives = get_alternative_suppliers()

        second_plan = None

        for option in alternatives:
            if option["supplier"] != plan["supplier"]:
                candidate = compare_recovery_options(15)

                feasible = [
                    item
                    for item in candidate["options"]
                    if item["supplier"] == option["supplier"]
                    and item["feasible"]
                ]

                if feasible:
                    second_plan = feasible[0]
                    break

        if second_plan is None:
            state["final_decision"] = "FAIL"
            return state

        state["current_plan"] = second_plan

        log(
            state,
            f"NEW DECISION: Switch to {second_plan['supplier']}"
        )

        result = simulate_recovery_action(
            second_plan["supplier"],
            second_plan["units"]
        )

        state["actions_taken"].append(result)

        if not result["success"]:
            state["failures"].append(result["error"])
            state["final_decision"] = "FAIL"
            return state

        state["current_inventory"] = result["new_inventory"]

        log(
            state,
            f"ACTION: Second recovery executed through "
            f"{second_plan['supplier']}"
        )

        state["verification_result"] = verify_recovery(
            second_plan["supplier"],
            second_plan["units"],
            second_plan["cost"]
        )

    else:
        state["verification_result"] = verify_recovery(
            plan["supplier"],
            plan["units"],
            plan["cost"]
        )

    final_risk = calculate_stockout_risk()

    state["final_stockout_risk"] = final_risk
    state["stockout_risk"] = final_risk["risk"]
    state["final_risk_calculated"] = True

    log(
        state,
        f"VERIFY: Inventory {final_risk['inventory']}, "
        f"Coverage {final_risk['coverage_days']} days, "
        f"Risk {final_risk['risk']}"
    )

    state["evaluation_result"] = evaluate_agent_run(state)

    state["final_decision"] = (
        state["evaluation_result"]["decision"]
    )

    print("\n========================================")
    print("FINAL DECISION:", state["final_decision"])
    print("========================================")

    print(
        state["evaluation_result"]["summary"]
    )

    return state


if __name__ == "__main__":
    run_agent()