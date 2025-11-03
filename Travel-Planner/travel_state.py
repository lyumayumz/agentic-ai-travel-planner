class TravelState:
    def __init__(self):
        self.data = {
            "user": {},
            "destinations": [],
            "budget_check": [],
            "itinerary": {},
            "final_plan": {}
        }

    def update(self, key, value):
        self.data[key] = value

    def get(self, key):
        return self.data.get(key)

    def show(self):
        return self.data


