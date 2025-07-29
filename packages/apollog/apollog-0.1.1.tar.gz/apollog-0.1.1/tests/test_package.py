"""
Basic tests for the Apollog package.
"""

import unittest
import os
import sys

# Add the parent directory to the path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import apollog

class TestApollgPackage(unittest.TestCase):
    """Test the Apollog package."""

    def test_version(self):
        """Test that the version is defined."""
        self.assertIsNotNone(apollog.__version__)
        self.assertIsInstance(apollog.__version__, str)

    def test_package_structure(self):
        """Test that the package has the expected structure."""
        # Check that the CLI module exists
        import apollog.cli
        self.assertTrue(hasattr(apollog.cli, 'main'))
        self.assertTrue(callable(apollog.cli.main))

if __name__ == '__main__':
    unittest.main()
