from tools.poi_tool import POITool

if __name__ == "__main__":
    city = "singapore"
    pois = POITool.get_top_pois(city, radius_km=3, limit=5)
    print(f"\nTop attractions in {city}:")
    for p in pois:
        print("-", p)