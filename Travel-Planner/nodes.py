from travel_state import TravelState
from agents.coordinator_agent import CoordinatorAgent
from agents.destination_agent import DestinationAgent
from agents.budget_agent import BudgetAgent
from agents.itinerary_agent import ItineraryAgent
from utils import debug

def start_node(state: TravelState):
    debug("Starting travel planner workflow")
    return state

def destination_node(state: TravelState):
    debug("Running Destination node")
    DestinationAgent(state).run()
    return state

def budget_node(state: TravelState):
    debug("Running Budget node")
    BudgetAgent(state).run()
    return state

def itinerary_node(state: TravelState):
    debug("Running Itinerary node")
    ItineraryAgent(state).run()
    return state

def coordinator_node(state: TravelState):
    debug("Running Coordinator node")
    CoordinatorAgent(state).run()
    return state
