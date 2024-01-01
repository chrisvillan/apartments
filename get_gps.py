from geopy.geocoders import Nominatim
import folium
from folium import IFrame

oc_cities = [
    "Aliso Viejo", "Anaheim", "Brea", "Buena Park", "Costa Mesa", "Cypress", "Dana Point",
    "Fountain Valley", "Fullerton", "Garden Grove", "Huntington Beach", "Irvine", "La Habra",
    "La Palma", "Laguna Beach", "Laguna Hills", "Laguna Niguel", "Laguna Woods", "Lake Forest",
    "Los Alamitos", "Mission Viejo", "Newport Beach", "Orange", "Placentia",
    "Rancho Santa Margarita", "San Clemente", "San Juan Capistrano", "Santa Ana", "Seal Beach",
    "Stanton", "Tustin", "Villa Park", "Westminster", "Yorba Linda", 
]

la_cities = [
    "Long Beach", "Lakewood", "Bellflower", "Artesia", "Cerritos", "Norwalk", "La Mirada", 
    "South Whittier", "Whittier", "La Habra Heights"
]

gps_coordinates = [
    {"County": "Orange", "City": "Tustin", "Latitude": 33.7458511, "Longitude": -117.826166},
    {"County": "Orange", "City": "Santa Ana", "Latitude": 33.7494951, "Longitude": -117.8732213},
    {"County": "Orange", "City": "Orange", "Latitude": 33.787914, "Longitude": -117.853104},
    {"County": "Orange", "City": "Anaheim", "Latitude": 33.8347516, "Longitude": -117.911732},
    {"County": "Orange", "City": "Garden Grove", "Latitude": 33.7746292, "Longitude": -117.9463717},
    {"County": "Orange", "City": "Fountain Valley", "Latitude": 33.7038145, "Longitude": -117.9627349},
    {"County": "Orange", "City": "Brea", "Latitude": 33.9170444, "Longitude": -117.888855},
    {"County": "Orange", "City": "Fullerton", "Latitude": 33.8708215, "Longitude": -117.9294165},
    {"County": "Orange", "City": "Buena Park", "Latitude": 33.870413, "Longitude": -117.9962165},
    {"County": "Orange", "City": "Costa Mesa", "Latitude": 33.6633386, "Longitude": -117.903317},
    {"County": "Orange", "City": "Cypress", "Latitude": 33.8248235, "Longitude": -118.0399368},
    {"County": "Orange", "City": "Huntington Beach", "Latitude": 33.6783336, "Longitude": -118.0000166},
    {"County": "Orange", "City": "Irvine", "Latitude": 33.6856969, "Longitude": -117.8259819},
    {"County": "Orange", "City": "La Habra", "Latitude": 33.9316066, "Longitude": -117.9454867},
    {"County": "Orange", "City": "La Palma", "Latitude": 33.846404, "Longitude": -118.0467306},
    {"County": "Orange", "City": "Los Alamitos", "Latitude": 33.8038865, "Longitude": -118.0772433},
    {"County": "Orange", "City": "Newport Beach", "Latitude": 33.6170092, "Longitude": -117.9294401},
    {"County": "Orange", "City": "Placentia", "Latitude": 33.8714814, "Longitude": -117.8617337},
    {"County": "Orange", "City": "Seal Beach", "Latitude": 33.7423967, "Longitude": -118.1055926},
    {"County": "Orange", "City": "Stanton", "Latitude": 33.79410005, "Longitude": -117.9951006},
    {"County": "Orange", "City": "Westminster", "Latitude": 33.7578725, "Longitude": -117.9859054},
    {"County": "Los Angeles", "City": "Long Beach", "Latitude": 33.7690164, "Longitude": -118.191604},
    {"County": "Los Angeles", "City": "Lakewood", "Latitude": 33.8503463, "Longitude": -118.117191},
    {"County": "Los Angeles", "City": "Bellflower", "Latitude": 33.8825705, "Longitude": -118.1167679},
    {"County": "Los Angeles", "City": "Artesia", "Latitude": 33.8690197, "Longitude": -118.0796195},
    {"County": "Los Angeles", "City": "Cerritos", "Latitude": 33.8644291, "Longitude": -118.0539323},
    {"County": "Los Angeles", "City": "Norwalk", "Latitude": 33.9092802, "Longitude": -118.0849169},
    {"County": "Los Angeles", "City": "La Mirada", "Latitude": 33.9060971, "Longitude": -118.0107092},
    {"County": "Los Angeles", "City": "South Whittier", "Latitude": 33.9366769, "Longitude": -118.0288059},
    {"County": "Los Angeles", "City": "Whittier", "Latitude": 33.9708782, "Longitude": -118.030839},
    {"County": "Los Angeles", "City": "La Habra Heights", "Latitude": 33.9604546, "Longitude": -117.9504255},
]

def get_coordinates_county(city, county):
    geolocator = Nominatim(user_agent="city_coordinates")
    location = geolocator.geocode(city + ", " + county + ", USA")
    if location and county in location.address:
        return location.latitude, location.longitude
    else:
        return None
    

def get_oc_cities():
    for city in oc_cities:
        coordinates = get_coordinates_county(city, "Orange County")
        if coordinates:
            print(f"{city}: Latitude {coordinates[0]}, Longitude {coordinates[1]}")
        else:
            print(f"Coordinates not found for {city}")

def get_la_cities():
    for city in la_cities:
        coordinates = get_coordinates_county(city, "Los Angeles")
        if coordinates:
            print(f"{city}: Latitude {coordinates[0]}, Longitude {coordinates[1]}")
        else:
            print(f"Coordinates not found for {city}")

def display_map_with_markers(coordinates):
    # Create a map centered at the first set of coordinates
    map_center = coordinates[0]["Latitude"], coordinates[0]["Longitude"]
    my_map = folium.Map(location=map_center, zoom_start=12)

    # Add markers for each set of coordinates
    for coord in coordinates:
        city = coord["City"]
        lat, lon = coord["Latitude"], coord["Longitude"]
        popup_text = f"{city}: Latitude {lat}, Longitude {lon}"
        popup = folium.Popup(IFrame(popup_text, width=300, height=100), max_width=300)
        folium.Marker(location=(lat, lon), popup=popup).add_to(my_map)

    # Save the map as an HTML file
    my_map.save('map_with_markers.html')

display_map_with_markers(gps_coordinates)