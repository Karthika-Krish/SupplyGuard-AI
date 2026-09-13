
from agent import create_initial_state, decide_next_action


state = create_initial_state()


print("Initial state")
print("Next action:", decide_next_action(state))


state["current_inventory"] = 35

print("\nAfter discovering inventory")
print("Next action:", decide_next_action(state))


state["daily_demand"] = 25

print("\nAfter discovering demand")
print("Next action:", decide_next_action(state))


state["stockout_risk"] = "HIGH"

print("\nAfter calculating risk")
print("Next action:", decide_next_action(state))


state["suppliers_checked"].append("Supplier A")

print("\nAfter checking Supplier A")
print("Next action:", decide_next_action(state))


state["failures"].append("Supplier A unavailable")

print("\nAfter Supplier A failure")
print("Next action:", decide_next_action(state))


state["replans"].append("Use Warehouse Chennai")

print("\nAfter replanning")
print("Next action:", decide_next_action(state))


state["actions_taken"].append("Recovery simulated")

print("\nAfter recovery")
print("Next action:", decide_next_action(state))
