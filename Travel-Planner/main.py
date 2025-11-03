from nodes import build_graph
from travel_state import TravelState
from utils import debug

def main():
    print("=== AI Travel Planning Committee with LangGraph ===\n")

    user = {
        "origin": input("Enter your origin city: "),
        "preferences": input("Enter travel preferences (e.g. beach, adventure): ").split(","),
        "budget": float(input("Enter your budget (USD): "))
    }

    state = TravelState()

    debug("Initializing LangGraph...")
    graph = build_graph()

    debug("Starting graph execution...")
    graph.invoke({"user": user})

    print("\n✅ FINAL TRAVEL PLAN")
    print(state.get("final_plan"))

if __name__ == "__main__":
    main()
