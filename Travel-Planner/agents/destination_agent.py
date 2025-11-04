from utils import debug

class DestinationAgent:
    def __init__(self, state):
        self.state = state

    def run(self):
        debug("DestinationAgent: Finding destinations...")
        preferences = self.state.get("user").get("preferences", [])
        mock_destinations = [
            {"name": "Bali", "country": "Indonesia"},
            {"name": "Phuket", "country": "Thailand"}
        ]
        self.state.update("destinations", mock_destinations)
        debug(f"Destinations found: {mock_destinations}")
