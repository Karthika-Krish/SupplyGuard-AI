
from agent import create_initial_state


state = create_initial_state()


print("\n--- INITIAL AGENT STATE ---")

for key, value in state.items():
    print(f"{key}: {value}")
