# SupplyGuard AI

## Autonomous Retail Supply Chain Recovery Agent

SupplyGuard AI is an autonomous supply-chain recovery agent designed to maintain retail service objectives when supplier, shipment, inventory, or demand conditions change.

## Problem

Retail supply chains can experience supplier failures, shipment delays, and inventory shortages. A recovery decision that is valid initially can also become invalid when the environment changes.

SupplyGuard AI addresses this using a closed-loop recovery workflow.

## Autonomous Workflow

Monitor → Detect → Investigate → Optimize → Decide → Execute → Monitor Again → Adapt → Replan → Verify

## How It Works

1. Monitors inventory, demand and shipment state.
2. Detects supplier disruption and stockout risk.
3. Investigates available recovery suppliers.
4. Compares feasible options using cost, lead-time and carbon constraints.
5. Executes a simulated recovery action.
6. Re-monitors the logistics environment.
7. Detects a subsequent disruption.
8. Replans using another feasible recovery option.
9. Executes the new recovery action.
10. Independently verifies the resulting state.

## Example Scenario

- Product: Wireless Headphones
- Initial inventory: 35 units
- Daily demand: 25 units
- Supplier A: Unavailable
- Recovery options: Supplier B / Warehouse Chennai
- A subsequent shipment disruption triggers adaptive replanning.
- The agent switches to another feasible recovery source.

## Technology

- Python
- Streamlit
- Constraint-based recovery planning
- Simulated logistics environment
- State-changing recovery tools
- Independent evaluation and verification

## Project Structure

- `app.py` — Streamlit interface
- `agent.py` — Autonomous recovery agent
- `tools.py` — Logistics environment and recovery tools
- `data.py` — Simulated supply-chain scenario
- `evaluator.py` — Independent evaluation
- `requirements.txt` — Dependencies

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
