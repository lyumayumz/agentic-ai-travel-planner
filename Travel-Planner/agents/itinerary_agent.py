from tools.poi_tool import POITool
from utils import debug

class ItineraryAgent:
    """
    Agent to build a travel itinerary based on selected destination
    and POI types (attractions, restaurants, museums, etc.).
    """

    def __init__(self, state):
        self.state = state

    def run(self):
        debug("ItineraryAgent: Generating itinerary...")

        # Get destination info from state
        destination = self.state.get("destination", {})
        city = destination.get("city")
        country = destination.get("country")

        if not city or not country:
            debug("ItineraryAgent: No destination found in state. Skipping itinerary.")
            return

        debug(f"ItineraryAgent: Fetching POIs for {city}, {country}")

        # Define POI types for itinerary
        poi_types = {
            "attractions": ["tourism.sights", "tourism.attraction"],
            "restaurants": ["catering.restaurant"]
        }

        itinerary = {}

        # Fetch POIs for each category
        for category, types in poi_types.items():
            pois = POITool.get_top_pois(city, poi_types=types, limit=5)
            itinerary[category] = pois
            debug(f"ItineraryAgent: {category.capitalize()} - {pois}")

        # Update state with final itinerary
        self.state.update("itinerary", itinerary)
        debug("ItineraryAgent: Itinerary generation complete.")
