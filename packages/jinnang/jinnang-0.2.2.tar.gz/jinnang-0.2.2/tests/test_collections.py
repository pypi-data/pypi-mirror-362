import unittest
import unittest
from jinnang.common.collections import list_to_tuple, get_first_value, get_unique_key

class TestCollections(unittest.TestCase):

    def test_list_to_tuple(self):
        # Test with int type
        int_list_to_tuple = list_to_tuple(int)
        self.assertEqual(int_list_to_tuple([1, 2, 3]), (1, 2, 3))

        # Test with str type
        str_list_to_tuple = list_to_tuple(str)
        self.assertEqual(str_list_to_tuple(["a", "b", "c"]), ("a", "b", "c"))

        # Test with float type
        float_list_to_tuple = list_to_tuple(float)
        self.assertEqual(float_list_to_tuple([1.1, 2.2, 3.3]), (1.1, 2.2, 3.3))

        # Test with mixed types (should convert to specified type)
        self.assertEqual(int_list_to_tuple(["1", 2.0, "3"]), (1, 2, 3))

        # Test with empty list
        self.assertEqual(int_list_to_tuple([]), ())

class TestCollections(unittest.TestCase):

    def test_get_first_value_found(self):
        d = {"a": "value_a", "b": "value_b"}
        self.assertEqual(get_first_value(d, ["a", "b"]), "value_a")
        self.assertEqual(get_first_value(d, ["b", "a"]), "value_b")

    def test_get_first_value_not_found(self):
        d = {"a": "value_a"}
        self.assertIsNone(get_first_value(d, ["c", "d"]))

    def test_get_first_value_with_default(self):
        d = {"a": "value_a"}
        self.assertEqual(get_first_value(d, ["c", "d"], default="default_value"), "default_value")

    def test_get_first_value_empty_string(self):
        d = {"a": "", "b": "value_b"}
        self.assertEqual(get_first_value(d, ["a", "b"]), "value_b")

    def test_get_first_value_none_value(self):
        d = {"a": None, "b": "value_b"}
        self.assertEqual(get_first_value(d, ["a", "b"]), "value_b")

    def test_get_first_value_empty_keys_list(self):
        d = {"a": "value_a"}
        self.assertIsNone(get_first_value(d, []))

    def test_get_unique_key_new_key(self):
        d = {"existing": 1}
        self.assertEqual(get_unique_key("new_key", d), "new_key")

    def test_get_unique_key_existing_key(self):
        d = {"key": 1}
        self.assertEqual(get_unique_key("key", d), "key-1")

    def test_get_unique_key_multiple_existing(self):
        d = {"key": 1, "key-1": 2, "key-2": 3}
        self.assertEqual(get_unique_key("key", d), "key-3")

    def test_get_unique_key_empty_dict(self):
        d = {}
        self.assertEqual(get_unique_key("key", d), "key")

    def test_get_unique_key_with_different_base_keys(self):
        d = {"item": 1, "item-1": 2, "product": 3}
        self.assertEqual(get_unique_key("item", d), "item-2")
        self.assertEqual(get_unique_key("product", d), "product-1")

if __name__ == '__main__':
    unittest.main()
    def test_list_to_tuple(self):
        # Test with int type
        int_converter = list_to_tuple(int)
        self.assertEqual(int_converter([1, 2, 3]), (1, 2, 3))
        self.assertEqual(int_converter(['1', '2', '3']), (1, 2, 3))
        
        # Test with str type
        str_converter = list_to_tuple(str)
        self.assertEqual(str_converter([1, 2, 3]), ('1', '2', '3'))
        self.assertEqual(str_converter(['a', 'b', 'c']), ('a', 'b', 'c'))
        
        # Test with float type
        float_converter = list_to_tuple(float)
        self.assertEqual(float_converter([1, 2, 3]), (1.0, 2.0, 3.0))
        self.assertEqual(float_converter(['1.1', '2.2', '3.3']), (1.1, 2.2, 3.3))
        
        # Test with empty list
        self.assertEqual(int_converter([]), ())
        
        # Test with custom type
        class CustomType:
            def __init__(self, value):
                self.value = value
                
            def __eq__(self, other):
                if not isinstance(other, CustomType):
                    return False
                return self.value == other.value
        
        custom_converter = list_to_tuple(CustomType)
        result = custom_converter([1, 2, 3])
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].value, 1)
        self.assertEqual(result[1].value, 2)
        self.assertEqual(result[2].value, 3)
        
        # Test with invalid conversions
        with self.assertRaises(ValueError):
            int_converter(['a', 'b', 'c'])
    
    def test_get_first_value(self):
        # Test with dictionary containing all keys
        d = {'a': 1, 'b': 2, 'c': 3}
        self.assertEqual(get_first_value(d, ['a', 'b', 'c']), 1)  # Should return first key's value
        self.assertEqual(get_first_value(d, ['b', 'a', 'c']), 2)  # Should return first key's value
        
        # Test with dictionary missing some keys
        d = {'b': 2, 'd': 4}
        self.assertEqual(get_first_value(d, ['a', 'b', 'c']), 2)  # Should return first found key's value
        
        # Test with dictionary missing all keys
        d = {'x': 10, 'y': 20}
        self.assertIsNone(get_first_value(d, ['a', 'b', 'c']))  # Should return None
        self.assertEqual(get_first_value(d, ['a', 'b', 'c'], default='default'), 'default')  # Should return default
        
        # Test with empty values
        d = {'a': None, 'b': '', 'c': 3}
        self.assertEqual(get_first_value(d, ['a', 'b', 'c']), 3)  # Should skip None and empty string
        
        # Test with empty dictionary
        d = {}
        self.assertIsNone(get_first_value(d, ['a', 'b', 'c']))  # Should return None
        self.assertEqual(get_first_value(d, ['a', 'b', 'c'], default='default'), 'default')  # Should return default
        
        # Test with empty keys list
        d = {'a': 1, 'b': 2, 'c': 3}
        self.assertIsNone(get_first_value(d, []))  # Should return None
        self.assertEqual(get_first_value(d, [], default='default'), 'default')  # Should return default
    
    def test_get_unique_key(self):
        # Test with key not in dictionary
        d = {'a': 1, 'b': 2, 'c': 3}
        self.assertEqual(get_unique_key('d', d), 'd')  # Should return key as is
        
        # Test with key already in dictionary
        d = {'a': 1, 'b': 2, 'c': 3}
        self.assertEqual(get_unique_key('a', d), 'a-1')  # Should return key with suffix
        
        # Test with key and suffixed keys already in dictionary
        d = {'a': 1, 'a-1': 2, 'a-2': 3}
        self.assertEqual(get_unique_key('a', d), 'a-3')  # Should return key with next available suffix
        
        # Test with non-sequential suffixes
        d = {'a': 1, 'a-1': 2, 'a-3': 3}
        self.assertEqual(get_unique_key('a', d), 'a-2')  # Should return key with next available suffix
        
        # Test with empty dictionary
        d = {}
        self.assertEqual(get_unique_key('a', d), 'a')  # Should return key as is
        
        # Test with numeric key
        d = {1: 'a', 2: 'b'}
        self.assertEqual(get_unique_key(1, d), '1-1')  # Should convert key to string and add suffix
        
        # Test with empty string key
        d = {'': 1}
        self.assertEqual(get_unique_key('', d), '-1')  # Should add suffix to empty string


if __name__ == "__main__":
    unittest.main()