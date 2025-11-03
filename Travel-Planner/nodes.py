from langgraph.graph import StateGraph, START, END
from travel_state import TravelState
from agents.coordinator_agent import CoordinatorAgent
from agents.destination_agent import DestinationAgent
from agents.budget_agent import BudgetAgent
from agents.itinerary_agent import ItineraryAgent
from utils import debug


def start_node(state: dict):
    """Initialize graph with existing state (always dict)."""
    debug("LangGraph: Starting execution")
    return {"status": "started"}  


def destination_node(state: dict):
    debug("LangGraph: Running Destination node")
    t_state = TravelState()
    t_state._data = state  
    DestinationAgent(t_state).run()
    return {"destination": t_state.get("destination")}


def budget_node(state: dict):
    debug("LangGraph: Running Budget node")
    t_state = TravelState()
    t_state._data = state
    BudgetAgent(t_state).run()
    return {"budget_plan": t_state.get("budget_plan")}


def itinerary_node(state: dict):
    debug("LangGraph: Running Itinerary node")
    t_state = TravelState()
    t_state._data = state
    ItineraryAgent(t_state).run()
    return {"itinerary": t_state.get("itinerary")}


def coordinator_node(state: dict):
    debug("LangGraph: Running Coordinator node")
    t_state = TravelState()
    t_state._data = state
    CoordinatorAgent(t_state).run()
    return {"final_plan": t_state.get("final_plan")}


def build_graph():
    debug("Building LangGraph...")

    builder = StateGraph(dict) 

    # Add nodes
    builder.add_node("start", start_node)
    builder.add_node("destination", destination_node)
    builder.add_node("budget", budget_node)
    builder.add_node("itinerary", itinerary_node)
    builder.add_node("coordinator", coordinator_node)

    # Define edges
    builder.add_edge(START, "start")
    builder.add_edge("start", "destination")
    builder.add_edge("destination", "budget")
    builder.add_edge("budget", "itinerary")
    builder.add_edge("itinerary", "coordinator")
    builder.add_edge("coordinator", END)

    debug("LangGraph build complete.")
    return builder.compile()
