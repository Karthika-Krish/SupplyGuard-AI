
from data import SCENARIO

print("Product:", SCENARIO["product"])
print("Inventory:", SCENARIO["inventory"])
print("Daily demand:", SCENARIO["daily_demand"])

print("\nSuppliers:")

for name, supplier in SCENARIO["suppliers"].items():
    print(
        name,
        "| Available:",
        supplier["available"],
        "| Lead time:",
        supplier["lead_time_days"],
        "days"
    )