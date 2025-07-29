"""
Test module for the biblestudy package.

This file demonstrates that the package can be imported and tested.
"""

import unittest
import sys
import os

# Add src to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from biblestudy import main
from biblestudy.config_loader import (
    get_notes_directory, 
    get_bible_api_key, 
    get_nlt_api_key, 
    get_esv_api_key, 
    get_openai_api_key
)


class TestBibleStudyPackage(unittest.TestCase):
    """Test cases for the biblestudy package."""
    
    def test_package_import(self):
        """Test that the main package can be imported."""
        self.assertIsNotNone(main)
        self.assertTrue(callable(main))
    
    def test_config_fallback(self):
        """Test that config loading works without config.py."""
        notes_dir = get_notes_directory()
        self.assertEqual(notes_dir, "notes")
    
    def test_cli_module_exists(self):
        """Test that CLI module exists and has main function."""
        from biblestudy import cli
        self.assertTrue(hasattr(cli, 'main'))
        self.assertTrue(callable(cli.main))
    
    def test_api_key_fallbacks(self):
        """Test that API key functions fall back correctly to environment variables or return empty strings."""
        # Save original environment variables if they exist
        original_env = {}
        api_env_vars = ['BIBLE_API_KEY', 'OPENAI_API_KEY', 'NLT_API_KEY', 'ESV_API_KEY']
        for var in api_env_vars:
            original_env[var] = os.environ.get(var)
            # Clear the environment variable for testing
            if var in os.environ:
                del os.environ[var]
        
        try:
            # Test that functions return empty strings when no config.py and no env vars
            self.assertEqual(get_bible_api_key(), "")
            self.assertEqual(get_openai_api_key(), "")
            self.assertEqual(get_nlt_api_key(), "")
            self.assertEqual(get_esv_api_key(), "")
            
            # Test that functions return environment variables when set
            os.environ['BIBLE_API_KEY'] = 'test-bible-key'
            os.environ['OPENAI_API_KEY'] = 'test-openai-key'
            os.environ['NLT_API_KEY'] = 'test-nlt-key'
            os.environ['ESV_API_KEY'] = 'test-esv-key'
            
            self.assertEqual(get_bible_api_key(), 'test-bible-key')
            self.assertEqual(get_openai_api_key(), 'test-openai-key')
            self.assertEqual(get_nlt_api_key(), 'test-nlt-key')
            self.assertEqual(get_esv_api_key(), 'test-esv-key')
            
        finally:
            # Restore original environment variables
            for var in api_env_vars:
                if original_env[var] is not None:
                    os.environ[var] = original_env[var]
                elif var in os.environ:
                    del os.environ[var]


if __name__ == '__main__':
    unittest.main()