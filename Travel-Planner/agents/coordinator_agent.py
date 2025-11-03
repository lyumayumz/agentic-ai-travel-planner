from utils import debug
from agents.destination_agent import DestinationAgent
from agents.budget_agent import BudgetAgent
from agents.itinerary_agent import ItineraryAgent

class CoordinatorAgent:
    def __init__(self, state):
        self.state = state
        self.destination_agent = DestinationAgent(state)
        self.budget_agent = BudgetAgent(state)
        self.itinerary_agent = ItineraryAgent(state)

    def run(self):
        debug("Coordinator started...")
        self.destination_agent.run()
        self.budget_agent.run()
        self.itinerary_agent.run()
        debug("Coordinator finished planning.")

        self.state.update("final_plan", {
            "recommendation": "Bali 🇮🇩",
            "estimated_cost": "$980",
            "duration": "5 days / 4 nights"
        })
