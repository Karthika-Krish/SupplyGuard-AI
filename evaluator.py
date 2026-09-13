
def evaluate_agent_run(state):
    """
    Independently evaluates whether the agent successfully
    solved the supply chain recovery problem.
    """

    checks = {}

    # 1. Was the initial stockout risk identified?
    checks["initial_risk_identified"] = (
        state["stockout_risk"] is not None
    )

    # 2. Did the original supplier fail?
    checks["supplier_failure_detected"] = (
        len(state["failures"]) > 0
    )

    # 3. Did the agent replan?
    checks["replanning_occurred"] = (
        len(state["replans"]) > 0
    )

    # 4. Was a recovery action actually executed?
    checks["recovery_executed"] = (
        state["recovery_executed"] is True
    )

    # 5. Did final verification pass?
    checks["verification_passed"] = (
        state["verification_result"] is not None
        and state["verification_result"]["verified"] is True
    )

    # 6. Did the final inventory reach at least
    #    two days of demand coverage?
    final_inventory = state["current_inventory"]
    daily_demand = state["daily_demand"]

    checks["inventory_protected"] = (
        daily_demand is not None
        and final_inventory >= daily_demand * 2
    )

    # 7. Was the selected recovery supplier available?
    selected_supplier = None

    if state["current_plan"]:
        selected_supplier = state["current_plan"]["supplier"]

    if selected_supplier:
        supplier_status = state["supplier_status"].get(
            selected_supplier
        )

        # The alternative supplier may not have been checked
        # individually, so use the verification result too.
        if supplier_status:
            checks["recovery_supplier_available"] = (
                supplier_status["available"] is True
            )
        else:
            checks["recovery_supplier_available"] = (
                state["verification_result"] is not None
                and state["verification_result"]["checks"][
                    "supplier_available"
                ]
            )
    else:
        checks["recovery_supplier_available"] = False

    # 8. Did the recovery stay within budget?
    if state["verification_result"]:
        checks["within_budget"] = (
            state["verification_result"]["checks"][
                "within_budget"
            ]
        )
    else:
        checks["within_budget"] = False

    passed = all(checks.values())

    if passed:
        decision = "PASS"
        summary = (
            "Agent successfully recovered inventory "
            "and protected against stockout."
        )
    else:
        decision = "FAIL"

        failed_checks = [
            name
            for name, result in checks.items()
            if not result
        ]

        summary = (
            "Agent failed evaluation. "
            "Failed checks: "
            + ", ".join(failed_checks)
        )

    return {
        "decision": decision,
        "passed": passed,
        "checks": checks,
        "summary": summary
    }
