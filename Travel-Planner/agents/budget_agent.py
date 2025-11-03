from utils import debug

class BudgetAgent:
    def __init__(self, state):
        self.state = state

    def run(self):
        debug("BudgetAgent: Checking budget...")
        destinations = self.state.get("destinations")
        mock_budget_check = [
            {"destination": d["name"], "cost": 980, "status": "within"} for d in destinations
        ]
        self.state.update("budget_check", mock_budget_check)
        debug(f"Budget results: {mock_budget_check}")
