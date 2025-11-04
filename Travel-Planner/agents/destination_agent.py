from utils import debug
from tools.destination_tool import DestinationTool
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage


class DestinationAgent:
    """
    Determines travel destination(s) based on user preferences and budget.
    """

    def __init__(self, state):
        self.state = state

    def run(self):
        debug("DestinationAgent: Selecting destination...")

        user = self.state.get("user", {})
        preferences = user.get("preferences", [])
        budget = user.get("budget", 0)
        origin = user.get("origin", "")

        # --- Option 1: Use OpenAI model for intelligent suggestions ---
        try:
            llm = ChatOpenAI(model="gpt-5-nano", temperature=0.7)
            system_prompt = (
                "You are a world-class travel recommender. "
                "Based on the user's origin, preferences, and budget, suggest 1 ideal destination. "
                "Return JSON in the format: {city: <city>, country: <country>, reason: <why this fits>}"
            )

            user_prompt = f"""
            Origin: {origin}
            Preferences: {preferences}
            Budget: ${budget}
            """

            response = llm.invoke([
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ])

            suggestion = response.content.strip()
            debug(f"DestinationAgent (OpenAI): {suggestion}")
            destination = DestinationTool.parse_llm_suggestion(suggestion)

        except Exception as e:
            debug(f"DestinationAgent: OpenAI failed ({e}), falling back to Geoapify.")
            # --- Option 2: Fallback to Geoapify Tool (no OpenAI) ---
            destination = DestinationTool.suggest_from_preferences(preferences)

        # Update final destination in state
        self.state.update("destination", destination)
        debug(f"DestinationAgent: Final destination = {destination}")
