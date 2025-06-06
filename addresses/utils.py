# from geopy.geocoders import Nominatim
# from django.conf import settings

# def get_coordinates_from_address(location, region):
#     """
#     Convert address to coordinates using Nominatim or another geolocation service.
#     """
#     try:
#         geolocator = Nominatim(user_agent="kleankickx")
#         full_address = f"{location}, {region}"
#         location_data = geolocator.geocode(full_address)
#         if location_data:
#             return location_data.latitude, location_data.longitude
#         return None, None
#     except Exception as e:
#         # Log error for debugging
#         print(f"Geocoding error: {str(e)}")
#         return None, None