import os
import requests
from dotenv import load_dotenv
from utils import debug

load_dotenv()


class BudgetTool:
    """
    Tool for estimating trip budget using free or mock APIs.
    Combines flight and hotel estimations based on city and duration.
    """

    TRAVELPAYOUTS_API = "https://api.travelpayouts.com/aviasales/v3/prices_for_dates"
    GEOAPIFY_API_KEY = os.getenv("GEOAPIFY_API_KEY")

    @staticmethod
    def get_average_hotel_price(city: str, nights: int = 5):
        """
        Estimate hotel price based on city (mock or heuristic using Geoapify).
        """
        try:
            # Geoapify Places API for accommodation listings
            res = requests.get(
                "https://api.geoapify.com/v2/places",
                params={
                    "categories": "accommodation.hotel",
                    "filter": f"name:{city}",
                    "limit": 5,
                    "apiKey": BudgetTool.GEOAPIFY_API_KEY,
                },
                timeout=8,
                verify=False,
            )
            data = res.json()
            features = data.get("features", [])
            if not features:
                raise ValueError("No hotels found")

            # Use a rough heuristic: base price depending on # of results
            avg_price = 80 + len(features) * 10  # mock heuristic
            total = avg_price * nights
            debug(f"BudgetTool: Estimated hotel cost for {nights} nights = ${total:.2f}")
            return total
        except Exception as e:
            debug(f"BudgetTool.get_average_hotel_price error: {e}")
            # Default mock fallback
            return 100 * nights

    @staticmethod
    def get_estimated_flight_price(origin: str, destination: str):
        """
        Estimate flight price using TravelPayouts API or fallback to mock.
        """
        try:
            res = requests.get(
                BudgetTool.TRAVELPAYOUTS_API,
                params={
                    "origin": origin[:3].upper(),  # airport code approx
                    "destination": destination[:3].upper(),
                    "one_way": "false",
                    "currency": "usd",
                },
                timeout=8,
                verify=False,
            )
            data = res.json()
            prices = [f.get("price") for f in data.get("data", []) if "price" in f]
            if not prices:
                raise ValueError("No price data found")

            avg_flight = sum(prices) / len(prices)
            debug(f"BudgetTool: Estimated flight cost = ${avg_flight:.2f}")
            return avg_flight
        except Exception as e:
            debug(f"BudgetTool.get_estimated_flight_price error: {e}")
            # Default mock fallback
            return 300.0

    @staticmethod
    def estimate_total_budget(origin: str, destination: str, nights: int = 5):
        """
        Combine flight and hotel cost into total estimated trip cost.
        """
        debug(f"BudgetTool: Estimating total budget for {origin} → {destination}")
        flight_cost = BudgetTool.get_estimated_flight_price(origin, destination)
        hotel_cost = BudgetTool.get_average_hotel_price(destination, nights)
        total = flight_cost + hotel_cost
        return {
            "flight_cost": round(flight_cost, 2),
            "hotel_cost": round(hotel_cost, 2),
            "total_estimated": round(total, 2),
            "nights": nights,
        }
