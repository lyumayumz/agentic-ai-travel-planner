from utils import debug

class ItineraryAgent:
    def __init__(self, state):
        self.state = state

    def run(self):
        debug("ItineraryAgent: Building itinerary...")
        mock_itinerary = {
            "Bali": [
                {"day": 1, "activity": "Visit Uluwatu Temple"},
                {"day": 2, "activity": "Relax at Seminyak Beach"},
                {"day": 3, "activity": "Mount Batur sunrise hike"}
            ]
        }
        self.state.update("itinerary", mock_itinerary)
        debug(f"Itinerary created: {mock_itinerary}")
