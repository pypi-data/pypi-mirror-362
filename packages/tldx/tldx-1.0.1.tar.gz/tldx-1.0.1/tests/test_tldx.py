import os
import tempfile
import unittest
from unittest.mock import patch
from tldx.core import fetch_tlds, load_keywords, generate_combinations

class TestTLDX(unittest.TestCase):
    def test_load_keywords(self):
        # Test single keyword
        self.assertEqual(load_keywords(keyword="test"), ["test"])
        
        # Test keyword file
        with tempfile.NamedTemporaryFile(mode='w+') as f:
            f.write("key1\nkey2\nkey3")
            f.seek(0)
            self.assertEqual(load_keywords(keyword_file=f.name), ["key1", "key2", "key3"])
    
    @patch('requests.get')
    def test_fetch_tlds(self, mock_get):
        # Mock IANA response
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = "# Comment\nCOM\nNET\nORG\n"
        self.assertEqual(fetch_tlds(), ["com", "net", "org"])
        
        # Test custom file
        with tempfile.NamedTemporaryFile(mode='w+') as f:
            f.write("# Custom TLDs\nTEST\nDEV\n")
            f.seek(0)
            self.assertEqual(fetch_tlds(f.name), ["test", "dev"])
    
    def test_generate_combinations(self):
        keywords = ["api", "dev"]
        tlds = ["com", "net"]
        expected = ["api.com", "api.net", "dev.com", "dev.net"]
        self.assertEqual(list(generate_combinations(keywords, tlds)), expected)

if __name__ == "__main__":
    unittest.main()

import pytest
from unittest.mock import patch, mock_open
from tldx.core import load_tlds, expand_keyword, expand_keywords_from_file
import requests

# Add these tests to existing test_tldx.py

def test_load_tlds_connection_error():
    """Test TLD loading fails with connection error"""
    with patch('requests.get') as mock_get:
        mock_get.side_effect = requests.exceptions.ConnectionError()
        tlds = load_tlds()
        assert tlds == []

def test_custom_tld_file_not_found():
    """Test custom TLD file not found error handling"""
    with patch('builtins.open', side_effect=FileNotFoundError):
        domains = expand_keyword('test', tld_list='missing_tlds.txt')
        assert domains == []

def test_keyword_file_not_found():
    """Test keyword file not found error handling"""
    with patch('builtins.open', side_effect=FileNotFoundError):
        domains = expand_keywords_from_file('missing_keywords.txt')
        assert domains == []