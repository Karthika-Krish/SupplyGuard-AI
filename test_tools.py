
from tools import (
    get_inventory,
    get_sales_velocity,
    calculate_stockout_risk,
    get_supplier_status,
    get_alternative_suppliers
)


print("\n--- INVENTORY ---")
print(get_inventory())


print("\n--- SALES VELOCITY ---")
print(get_sales_velocity())


print("\n--- STOCKOUT RISK ---")
print(calculate_stockout_risk())


print("\n--- SUPPLIER A ---")
print(get_supplier_status("Supplier A"))


print("\n--- ALTERNATIVE SUPPLIERS ---")
print(get_alternative_suppliers())