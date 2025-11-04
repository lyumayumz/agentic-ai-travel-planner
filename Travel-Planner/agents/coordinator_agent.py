from utils import debug
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from agents.destination_agent import DestinationAgent
from agents.budget_agent import BudgetAgent
from agents.itinerary_agent import ItineraryAgent

class CoordinatorAgent:
    def __init__(self, state: dict):
        self.state = state
        self.destination_agent = DestinationAgent(state)
        self.budget_agent = BudgetAgent(state)
        self.itinerary_agent = ItineraryAgent(state)

    def run(self):
        debug("Coordinator started...")

        user = self.state.get("user")
        destination = self.state.get("destination")
        budget_plan = self.state.get("budget_plan")
        itinerary = self.state.get("itinerary")
 
        llm = ChatOpenAI(model="gpt-5-nano", temperature=1)
        system_prompt = (
            """
            You are an expert AI travel planner that generates structured travel recommendations.
            Your response must begin with a concise summary paragraph (2-4 sentences) that captures the overall travel idea — who the trip is for, where, and what kind of experience it offers.
            After that paragraph, always format the rest of your response **exactly** in the following structure:
            Destination: <summary of the destination(s) with key highlights and why it's a good fit>
            Budget Plan: <concise summary of estimated cost range, assumptions, and value>
            Itinerary:
            <day-by-day breakdown with key activities, transport, meals, and optional tips>
            Do not include any text outside of these sections. If any information is missing from the user’s input, clearly indicate assumptions in brackets."""
            
        )

        # """
        #     "You are a professional travel planner. "
        #     "Summarize the entire travel plan in a friendly and informative tone, "
        #     "including destination, itinerary highlights, and cost overview."
        # """
 
        user_prompt = f"""
        User Info: {user}
        Destination: {destination}
        Budget Plan: {budget_plan}
        Itinerary: {itinerary}
        """

        ### UNCOMMENT FOR OPENAI ###
        # response = llm.invoke([
        #     SystemMessage(content=system_prompt),
        #     HumanMessage(content=user_prompt)
        # ])

        # summary = response.content.strip()
        # self.state.update("final_plan", summary)

        ### FOR NOAI ###
        self.destination_agent.run()
        self.budget_agent.run()
        self.itinerary_agent.run()
        

        self.state.update("final_plan", {
        "destination": self.state.get("destination"),
        "budget_plan": self.state.get("budget_plan"),
        "itinerary": self.state.get("itinerary")
        })

        debug("Coordinator finished planning.")
