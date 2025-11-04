import os
import requests
from utils import debug
from dotenv import load_dotenv

load_dotenv()

class POITool:
    """Tool for fetching points of interest (POIs) using Geoapify API with type support."""

    GEOAPIFY_API_KEY = os.getenv("GEOAPIFY_API_KEY")
    BASE_URL = "https://api.geoapify.com/v2/places"

    @staticmethod
    def get_city_coordinates(city_name: str):
        """Get latitude/longitude for a city using Geoapify Geocoding API."""
        try:
            res = requests.get(
                "https://api.geoapify.com/v1/geocode/search",
                params={
                    "text": city_name,
                    "apiKey": POITool.GEOAPIFY_API_KEY,
                    "lang": "en",
                },
                verify=False
            )
            data = res.json()
            features = data.get("features", [])
            if not features:
                debug(f"No coordinates found for {city_name}")
                return None, None

            lon, lat = features[0]["geometry"]["coordinates"]
            debug(f"Coordinates for {city_name}: ({lat}, {lon})")
            return lat, lon
        except Exception as e:
            debug(f"POITool.get_city_coordinates error: {e}")
            return None, None

    @staticmethod
    def get_top_pois(city_name: str, poi_types=None, radius_km: int = 5, limit: int = 5):
        """
        Fetch top POIs near a city.
        poi_types: list of Geoapify categories (e.g., ["tourism.sights", "cultural"])
        """
        lat, lon = POITool.get_city_coordinates(city_name)
        if not lat or not lon:
            debug(f"Skipping POI search — invalid coordinates for {city_name}")
            return []

        if poi_types is None:
            poi_types = ["tourism.sights", "tourism.attraction"]

        try:
            res = requests.get(
                POITool.BASE_URL,
                params={
                    "categories": ",".join(poi_types),
                    "filter": f"circle:{lon},{lat},{radius_km*1000}",
                    "limit": limit,
                    "apiKey": POITool.GEOAPIFY_API_KEY
                },
                verify=False
            )
            data = res.json()
            features = data.get("features", [])
            pois = []
            for f in features:
                props = f.get("properties", {})
                name = props.get("name:en") or props.get("name") or "Unnamed place"
                pois.append(name)
            debug(f"Found {len(pois)} POIs in {city_name} for categories {poi_types}")
            return pois
        except Exception as e:
            debug(f"POITool.get_top_pois error: {e}")
            return []
