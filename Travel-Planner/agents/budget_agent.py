from utils import debug
from tools.budget_tool import BudgetTool
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

class BudgetAgent:
    def __init__(self, state):
        self.state = state
       

    def run(self):
        debug("BudgetAgent: Calculating estimated costs...")

        user = self.state.get("user", {})
        destination = self.state.get("destination", {})

        origin_city = user.get("origin", "Singapore")
        dest_city = destination.get("city", "Bangkok")
        nights = destination.get("nights", 5)

        debug(f"BudgetAgent: Estimating for {origin_city} → {dest_city}")

        # Step 1: Base budget from flight + hotel
        budget_estimate = BudgetTool.estimate_total_budget(origin_city, dest_city, nights=nights)
        total_budget = user.get("budget", 1000)

        debug(f"BudgetAgent: Base budget estimate = {budget_estimate}")
        llm = ChatOpenAI(model_name="gpt-5-nano", temperature=0.7)  # or "gpt-3.5-turbo"
        # Step 2: Ask LLM to suggest allocations
        system_prompt = "You are a travel budget assistant. Suggest how to allocate a total trip budget into flight, hotel, and activities."
        user_prompt = (
            f"The total estimated budget for a trip from {origin_city} to {dest_city} "
            f"for {nights} nights is ${total_budget:.2f}. "
            "Please provide a suggested allocation in percentages and estimated amounts for flight, hotel, and activities."
        )

        response = llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ])

        suggestion = response.content.strip()
        debug(f"BudgetAgent (OpenAI): {suggestion}")
        # budget = BudgetTool.parse_llm_suggestion(suggestion)

        # Step 3: Update state
        self.state.update("budget_plan", suggestion)
