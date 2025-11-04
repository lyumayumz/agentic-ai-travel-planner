from dotenv import load_dotenv
from travel_state import TravelState
from nodes import start_node, destination_node, budget_node, itinerary_node, coordinator_node
from utils import debug

load_dotenv(override=True)

def main():
    print("=== AI Travel Planning Committee ===\n")

    user = {
        "origin": input("Enter your origin city: ").strip(),
        "preferences": input("Enter travel preferences (e.g., beach, adventure): ").split(","),
        "budget": float(input("Enter your budget (USD): ").strip())
    }

    state = TravelState()
    state.update("user", user)

    debug("Workflow started...")

    # Sequential execution
    start_node(state)
    destination_node(state)
    budget_node(state)
    itinerary_node(state)
    coordinator_node(state)

    print("\n✅ FINAL TRAVEL PLAN\n")
    print(state.get("final_plan"))

if __name__ == "__main__":
    main()
