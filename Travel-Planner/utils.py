import os


def debug(message, prefix="DEBUG"):
    """
    Print debug message in gray if DEBUG env var is true.

    Args:
        message: The debug message to print
        prefix: Prefix for the debug message (default: "DEBUG")
    """
    if os.getenv("DEBUG", "false").lower() == "true":
        print(f"    \033[2m[{prefix}] {message}\033[0m")

def beautify_itinerary(trip_data):
    """
    Takes a trip dictionary and prints a clean, readable itinerary.
    Expects keys: destination, budget_plan, itinerary (with attractions, restaurants, museums)
    """
    destination = trip_data.get("destination", {})
    budget_plan = trip_data.get("budget_plan", "")
    itinerary = trip_data.get("itinerary", {})

    print("==== Trip Itinerary ====\n")

    # Destination
    print("🏝 Destination:")
    city = destination.get("city", "Unknown")
    country = destination.get("country", "")
    reason = destination.get("reason", "")
    print(f"{city}, {country}")
    print(f"{reason}\n")

    # Budget
    print("💰 Budget Plan:")
    print(budget_plan + "\n")

    # Itinerary
    print("🗓 Itinerary:")
    
    # Attractions
    attractions = itinerary.get("attractions", [])
    if attractions:
        print("\n  Attractions:")
        for i, attr in enumerate(attractions, 1):
            print(f"    {i}. {attr}")
    else:
        print("\n  Attractions: None listed")

    # Restaurants
    restaurants = itinerary.get("restaurants", [])
    if restaurants:
        print("\n  Restaurants:")
        for i, r in enumerate(restaurants, 1):
            print(f"    {i}. {r}")
    else:
        print("\n  Restaurants: None listed")
    print("\n=========================")

