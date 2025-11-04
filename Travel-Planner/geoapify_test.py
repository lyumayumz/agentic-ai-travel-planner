import os
import requests
from dotenv import load_dotenv

load_dotenv(override=True)

API_KEY = os.getenv("GEOAPIFY_API_KEY")

if not API_KEY:
    print("❌ GEOAPIFY_API_KEY not found in .env file.")
    exit(1)

def test_geocoding(city_name: str):
    """Test basic geocoding lookup."""
    print(f"\n🔍 Testing Geoapify Geocoding for: {city_name}")
    res = requests.get(
        "https://api.geoapify.com/v1/geocode/search",
        params={"text": city_name, "apiKey": API_KEY},
        verify=False
    )
    data = res.json()
    if not data.get("features"):
        print("❌ No results found.")
        return
    props = data["features"][0]["properties"]
    print(f"✅ Found: {props.get('city', city_name)}, {props.get('country')}")
    print(f"📍 Coordinates: {props.get('lat')}, {props.get('lon')}")


def test_places(city_name: str):
    """Test places (POIs) lookup using Geoapify Places API."""
    print(f"\n🏙️  Testing Geoapify Places near: {city_name}")

    # Get coordinates first
    geo_res = requests.get(
        "https://api.geoapify.com/v1/geocode/search",
        params={"text": city_name, "apiKey": API_KEY},
        verify=False
    ).json()
    features = geo_res.get("features", [])
    if not features:
        print("❌ Could not get coordinates.")
        return

    coords = features[0]["geometry"]["coordinates"]
    lon, lat = coords[0], coords[1]

    # Now get nearby POIs
    poi_res = requests.get(
        "https://api.geoapify.com/v2/places",
        params={
            "categories": "tourism.sights,tourism.attraction",
            "filter": f"circle:{lon},{lat},5000",
            "limit": 5,
            "apiKey": API_KEY
        },
        verify=False
    ).json()

    features = poi_res.get("features", [])
    if not features:
        print("❌ No POIs found.")
        return

    print("✅ Top POIs:")
    for f in features:
        props = f.get("properties", {})
        name = props.get("name:en") or props.get("name") or "Unnamed"
        print(f" - {name}")


if __name__ == "__main__":
    print("=== 🌍 Geoapify API Test ===")

    test_city = input("Enter a city to test (e.g. Tokyo): ").strip()
    test_geocoding(test_city)
    test_places(test_city)
    print("\n✅ Done.")
