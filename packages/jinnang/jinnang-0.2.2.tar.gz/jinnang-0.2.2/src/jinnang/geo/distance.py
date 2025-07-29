import math

def calculate_distance_meters(
    longitude_point_a: float,
    latitude_point_a: float,
    longitude_point_b: float,
    latitude_point_b: float,
) -> float:
    """
    Calculate the great-circle distance between two points on Earth in meters.
    Args:
        latitude_point_a: Latitude of first point in degrees
        longitude_point_a: Longitude of first point in degrees
        latitude_point_b: Latitude of second point in degrees
        longitude_point_b: Longitude of second point in degrees
    Returns:
        Distance between the points in meters
    """
    EARTH_RADIUS_METERS = 6_371_000
    lat_a_rad = math.radians(latitude_point_a)
    lon_a_rad = math.radians(longitude_point_a)
    lat_b_rad = math.radians(latitude_point_b)
    lon_b_rad = math.radians(longitude_point_b)
    delta_latitude = lat_b_rad - lat_a_rad
    delta_longitude = lon_b_rad - lon_a_rad
    haversine_component = (
        math.sin(delta_latitude / 2)**2 
        + math.cos(lat_a_rad) 
        * math.cos(lat_b_rad) 
        * math.sin(delta_longitude / 2)**2
    )
    angular_distance = 2 * math.atan2(
        math.sqrt(haversine_component),
        math.sqrt(1 - haversine_component)
    )
    distance_meters = EARTH_RADIUS_METERS * angular_distance
    return distance_meters