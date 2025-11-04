from tools.budget_tool import FlightHotelTool

if __name__ == "__main__":
    city = "PEN"
    # pois = POITool.get_top_pois(city, radius_km=3, limit=5)
    # print(f"\nTop attractions in {city}:")
    # for p in pois:
    #     print("-", p)

    flight = FlightHotelTool.get_destinations(city)
    print(flight)