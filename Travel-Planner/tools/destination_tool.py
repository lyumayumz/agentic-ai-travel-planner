import os
import requests
from utils import debug

class DestinationTool:
    """
    Utility class to suggest destinations based on travel preferences.
    """

    GEOAPIFY_URL = "https://api.geoapify.com/v1/geocode/search"
    GEOAPIFY_KEY = os.getenv("GEOAPIFY_API_KEY")

    @staticmethod
    def parse_llm_suggestion(suggestion: str):
        """Parse AI-generated JSON safely."""
        import json
        try:
            return json.loads(suggestion)
        except json.JSONDecodeError:
            debug("DestinationTool: LLM output not JSON. Returning as text.")
            return {"city": suggestion, "country": "", "reason": "AI free-text suggestion"}

    @staticmethod
    def suggest_from_preferences(preferences):
        """Fallback method: use Geoapify or static mapping."""
        debug(f"DestinationTool: Suggesting via Geoapify using prefs={preferences}")

        theme_map = {
            "beach": "Honolulu",
            "mountain": "Zermatt",
            "city": "Tokyo",
            "adventure": "Queenstown",
            "culture": "Kyoto",
            "romantic": "Paris"
        }

        for pref in preferences:
            pref = pref.strip().lower()
            if pref in theme_map:
                city = theme_map[pref]
                country = DestinationTool.lookup_country(city)
                return {"city": city, "country": country, "reason": f"Matches your preference for {pref}"}

        return {"city": "Singapore", "country": "Singapore", "reason": "Default safe fallback"}

    @staticmethod
    def lookup_country(city):
        """Use Geoapify to look up the country for a given city."""
        if not DestinationTool.GEOAPIFY_KEY:
            return "Unknown"

        params = {"text": city, "apiKey": DestinationTool.GEOAPIFY_KEY}
        try:
            res = requests.get(DestinationTool.GEOAPIFY_URL, params=params)
            data = res.json()
            country = data.get("features", [{}])[0].get("properties", {}).get("country", "Unknown")
            return country
        except Exception as e:
            debug(f"Geoapify lookup failed: {e}")
            return "Unknown"
