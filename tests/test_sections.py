import unittest
from webassembly import Webassembly

class TestMyFormat(unittest.TestCase):
    
    def test_basic_parsing(self):
        """Test parsing a simple valid file"""
        module = Webassembly.from_file('tests/assets/empty.wasm')
        
        self.assertEqual(module.magic, b'\x00asm')
        self.assertEqual(module.version, 1)
        self.assertEqual(len(module.sections), 0)

    def test_corrupted_magic(self):
        """Test error handling with invalid data"""
        corrupted_data = b'\x00asn\x01\x00\x00\x00'  # wrong magic number
        
        with self.assertRaises(Exception):
            Webassembly.from_bytes(corrupted_data)

if __name__ == '__main__':
    unittest.main()