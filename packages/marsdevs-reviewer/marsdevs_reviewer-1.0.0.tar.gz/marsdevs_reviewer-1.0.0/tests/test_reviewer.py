"""
Basic tests for MarsDevs Code Reviewer
"""

import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from marsdevs_reviewer.reviewer import (
    get_file_extension,
    get_cache_key,
    format_review_output
)


class TestReviewer(unittest.TestCase):
    """Test cases for reviewer functions."""
    
    def test_get_file_extension(self):
        """Test file extension extraction."""
        self.assertEqual(get_file_extension("test.py"), ".py")
        self.assertEqual(get_file_extension("path/to/file.js"), ".js")
        self.assertEqual(get_file_extension("no_extension"), "")
        self.assertEqual(get_file_extension("multiple.dots.py"), ".py")
    
    def test_get_cache_key(self):
        """Test cache key generation."""
        diff1 = "diff --git a/test.py b/test.py"
        diff2 = "diff --git a/other.py b/other.py"
        conventions = "test conventions"
        
        # Same inputs should produce same key
        key1 = get_cache_key(diff1, conventions)
        key2 = get_cache_key(diff1, conventions)
        self.assertEqual(key1, key2)
        
        # Different inputs should produce different keys
        key3 = get_cache_key(diff2, conventions)
        self.assertNotEqual(key1, key3)
    
    def test_format_review_output_no_issues(self):
        """Test output formatting when no issues found."""
        review = {
            "has_issues": False,
            "summary": "All good!"
        }
        fixes_applied = []
        
        should_allow, output = format_review_output(review, fixes_applied)
        
        self.assertTrue(should_allow)
        self.assertIn("No convention violations found", output)
        self.assertIn("All good!", output)
    
    def test_format_review_output_with_issues(self):
        """Test output formatting with issues."""
        review = {
            "has_issues": True,
            "severity": "high",
            "issues": [
                {
                    "type": "convention",
                    "file": "test.py",
                    "line_start": 10,
                    "description": "Test issue",
                    "convention_violated": "Test convention"
                }
            ],
            "summary": "Found issues"
        }
        fixes_applied = []
        
        should_allow, output = format_review_output(review, fixes_applied)
        
        self.assertFalse(should_allow)  # High severity blocks
        self.assertIn("Found 1 convention issue(s)", output)
        self.assertIn("Test issue", output)
        self.assertIn("COMMIT BLOCKED", output)


if __name__ == "__main__":
    unittest.main()