from tools.poi_tool import POITool
from utils import debug

class DestinationAgent:
    """
    Agent to select a travel destination based on user preferences.
    Can be deterministic for testing or later upgraded to AI suggestions.
    """

    def __init__(self, state):
        self.state = state

    def run(self):
        debug("DestinationAgent: Selecting destination...")

        user = self.state.get("user", {})
        origin = user.get("origin", "Unknown")
        preferences = user.get("preferences", [])

        # Deterministic selection for testing
        # For example, pick a city based on a simple rule
        if "beach" in preferences:
            destination = {"city": "Bali", "country": "Indonesia"}
        elif "culture" in preferences:
            destination = {"city": "Kyoto", "country": "Japan"}
        elif "adventure" in preferences:
            destination = {"city": "Queenstown", "country": "New Zealand"}
        else:
            destination = {"city": "Singapore", "country": "Singapore"}

        debug(f"DestinationAgent: Selected {destination['city']}, {destination['country']}")

        # Optional: fetch top POIs for the destination for initial hints
        pois = POITool.get_top_pois(destination["city"], limit=5)
        debug(f"DestinationAgent: Top POIs - {pois}")

        # Save destination and POIs to state
        self.state.update("destination", destination)
        self.state.update("destination_pois", pois)

        debug("DestinationAgent: Destination selection complete.")
