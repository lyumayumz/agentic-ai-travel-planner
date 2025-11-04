from tools.budget_tool import BudgetTool
from utils import debug

class BudgetAgent:
    def __init__(self, state):
        self.state = state

    def run(self):
        debug("BudgetAgent: Calculating estimated costs...")

        user = self.state.get("user", {})
        destination = self.state.get("destination", {})

        origin_city = user.get("origin", "Singapore")
        dest_city = destination.get("city", "Bangkok")

        debug(f"BudgetAgent: Estimating for {origin_city} → {dest_city}")
        budget_estimate = BudgetTool.estimate_total_budget(origin_city, dest_city, nights=5)

        self.state.update("budget_plan", budget_estimate)
        debug(f"BudgetAgent: Final budget estimate = {budget_estimate}")
