import unittest
import math
from jinnang.geo import calculate_distance_meters

class TestGeoUtils(unittest.TestCase):

    def test_calculate_distance_meters_zero_distance(self):
        # Test case for zero distance (same point)
        lon_a, lat_a = 0.0, 0.0
        lon_b, lat_b = 0.0, 0.0
        distance = calculate_distance_meters(lon_a, lat_a, lon_b, lat_b)
        self.assertAlmostEqual(distance, 0.0, places=5)

    def test_calculate_distance_meters_known_distance(self):
        # Test case for a known distance (e.g., equator)
        # Distance between (0,0) and (0, 90) should be approx 10,000,000 meters (1/4 of Earth's circumference)
        lon_a, lat_a = 0.0, 0.0
        lon_b, lat_b = 0.0, 90.0
        distance = calculate_distance_meters(lon_a, lat_a, lon_b, lat_b)
        # Earth's circumference is approx 40,075,000 meters. Quarter is 10,018,750
        self.assertAlmostEqual(distance, 10018754.3, delta=12000)

    def test_calculate_distance_meters_antipodal(self):
        # Test case for antipodal points (opposite sides of the Earth)
        lon_a, lat_a = 0.0, 0.0
        lon_b, lat_b = 180.0, 0.0
        distance = calculate_distance_meters(lon_a, lat_a, lon_b, lat_b)
        # Half of Earth's circumference
        self.assertAlmostEqual(distance, 20037508.3, delta=25000)

    def test_calculate_distance_meters_different_hemispheres(self):
        # Test case for points in different hemispheres
        lon_a, lat_a = -74.0060, 40.7128  # New York City
        lon_b, lat_b = 151.2093, -33.8688  # Sydney
        distance = calculate_distance_meters(lon_a, lat_a, lon_b, lat_b)
        # Expected distance is approximately 15990000 meters
        self.assertAlmostEqual(distance, 15993000, delta=200000) # Allow for some delta due to Earth model variations

    def test_calculate_distance_meters_small_distance(self):
        # Test case for a very small distance
        lon_a, lat_a = 0.0, 0.0
        lon_b, lat_b = 0.00001, 0.00001
        distance = calculate_distance_meters(lon_a, lat_a, lon_b, lat_b)
        self.assertAlmostEqual(distance, 1.57, places=2)