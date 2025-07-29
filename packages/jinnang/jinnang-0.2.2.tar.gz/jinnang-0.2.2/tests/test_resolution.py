import unittest

from jinnang.media.resolution import ResolutionPreset


class TestResolutionPreset(unittest.TestCase):
    def test_resolution_values(self):
        # Test that resolution presets have correct values
        self.assertEqual(ResolutionPreset.ORIGINAL.value, (None, None))
        self.assertEqual(ResolutionPreset.RES_4K.value, (3840, 2160))
        self.assertEqual(ResolutionPreset.RES_1080P.value, (1920, 1080))
        self.assertEqual(ResolutionPreset.RES_720P.value, (1280, 720))
        self.assertEqual(ResolutionPreset.RES_480P.value, (854, 480))
        self.assertEqual(ResolutionPreset.RES_360P.value, (640, 360))
        self.assertEqual(ResolutionPreset.RES_240P.value, (426, 240))
        self.assertEqual(ResolutionPreset.RES_16P.value, (16, 16))
    
    def test_equality_comparison(self):
        # Test equality comparison
        self.assertEqual(ResolutionPreset.RES_1080P, ResolutionPreset.RES_1080P)
        self.assertNotEqual(ResolutionPreset.RES_720P, ResolutionPreset.RES_1080P)
        
        # Test equality with non-ResolutionPreset objects
        self.assertNotEqual(ResolutionPreset.RES_1080P, (1920, 1080))
        self.assertNotEqual(ResolutionPreset.RES_1080P, "1080p")
    
    def test_less_than_comparison(self):
        # Test less than comparison
        self.assertLess(ResolutionPreset.RES_720P, ResolutionPreset.RES_1080P)
        self.assertLess(ResolutionPreset.RES_480P, ResolutionPreset.RES_720P)
        self.assertLess(ResolutionPreset.RES_360P, ResolutionPreset.RES_480P)
        self.assertLess(ResolutionPreset.RES_240P, ResolutionPreset.RES_360P)
        self.assertLess(ResolutionPreset.RES_16P, ResolutionPreset.RES_32P)
        
        # Test that ORIGINAL is never less than any other resolution
        for resolution in ResolutionPreset:
            if resolution != ResolutionPreset.ORIGINAL:
                self.assertLess(resolution, ResolutionPreset.ORIGINAL)
                self.assertFalse(ResolutionPreset.ORIGINAL < resolution)
    
    def test_greater_than_comparison(self):
        # Test greater than comparison
        self.assertGreater(ResolutionPreset.RES_1080P, ResolutionPreset.RES_720P)
        self.assertGreater(ResolutionPreset.RES_720P, ResolutionPreset.RES_480P)
        self.assertGreater(ResolutionPreset.RES_480P, ResolutionPreset.RES_360P)
        self.assertGreater(ResolutionPreset.RES_360P, ResolutionPreset.RES_240P)
        self.assertGreater(ResolutionPreset.RES_32P, ResolutionPreset.RES_16P)
        
        # Test that ORIGINAL is always greater than any other resolution
        for resolution in ResolutionPreset:
            if resolution != ResolutionPreset.ORIGINAL:
                self.assertGreater(ResolutionPreset.ORIGINAL, resolution)
                self.assertFalse(resolution > ResolutionPreset.ORIGINAL)
    
    def test_less_than_or_equal_comparison(self):
        # Test less than or equal comparison
        self.assertLessEqual(ResolutionPreset.RES_720P, ResolutionPreset.RES_1080P)
        self.assertLessEqual(ResolutionPreset.RES_720P, ResolutionPreset.RES_720P)  # Equal case
        
        # Test with ORIGINAL
        self.assertLessEqual(ResolutionPreset.RES_4K, ResolutionPreset.ORIGINAL)
        self.assertLessEqual(ResolutionPreset.ORIGINAL, ResolutionPreset.ORIGINAL)  # Equal case
    
    def test_greater_than_or_equal_comparison(self):
        # Test greater than or equal comparison
        self.assertGreaterEqual(ResolutionPreset.RES_1080P, ResolutionPreset.RES_720P)
        self.assertGreaterEqual(ResolutionPreset.RES_720P, ResolutionPreset.RES_720P)  # Equal case
        
        # Test with ORIGINAL
        self.assertGreaterEqual(ResolutionPreset.ORIGINAL, ResolutionPreset.RES_4K)
        self.assertGreaterEqual(ResolutionPreset.ORIGINAL, ResolutionPreset.ORIGINAL)  # Equal case
    
    def test_comparison_with_non_resolution_objects(self):
        # Test comparison with non-ResolutionPreset objects
        with self.assertRaises(TypeError):
            ResolutionPreset.RES_1080P < (1920, 1080)
        
        with self.assertRaises(TypeError):
            ResolutionPreset.RES_1080P > "1080p"
    
    def test_resolution_ordering(self):
        # Test that resolutions are ordered correctly from smallest to largest
        resolutions = [
            ResolutionPreset.RES_16P,
            ResolutionPreset.RES_32P,
            ResolutionPreset.RES_48P,
            ResolutionPreset.RES_64P,
            ResolutionPreset.RES_96P, # 128x96 = 12288
            ResolutionPreset.RES_80P, # 160x80 = 12800
            ResolutionPreset.RES_120P,
            ResolutionPreset.RES_144P,
            ResolutionPreset.RES_240P,
            ResolutionPreset.RES_360P,
            ResolutionPreset.RES_480P,
            ResolutionPreset.RES_540P,
            ResolutionPreset.RES_720P,
            ResolutionPreset.RES_1080P,
            ResolutionPreset.RES_2K,
            ResolutionPreset.RES_4K,
            ResolutionPreset.ORIGINAL
        ]
        
        # Check that each resolution is greater than all previous resolutions
        for i in range(1, len(resolutions)):
            for j in range(i):
                self.assertGreater(resolutions[i], resolutions[j])
                self.assertLess(resolutions[j], resolutions[i])
    
    def test_enum_iteration(self):
        # Test that we can iterate through all resolution presets
        resolutions = list(ResolutionPreset)
        self.assertIn(ResolutionPreset.ORIGINAL, resolutions)
        self.assertIn(ResolutionPreset.RES_4K, resolutions)
        self.assertIn(ResolutionPreset.RES_1080P, resolutions)
        self.assertIn(ResolutionPreset.RES_720P, resolutions)
        self.assertIn(ResolutionPreset.RES_16P, resolutions)


if __name__ == "__main__":
    unittest.main()