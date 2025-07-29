"""Tests for arc_file_extractor module."""

import os
import tempfile
from pathlib import Path
import pytest
from unittest.mock import patch, MagicMock

from arc_file_extractor.arc_file_extractor import ArcFileExtractor
from arc_file_extractor import utils


class TestArcFileExtractor:
    """Test cases for ArcFileExtractor class."""
    
    def test_init(self):
        """Test ArcFileExtractor initialization."""
        extractor = ArcFileExtractor()
        assert extractor.extract_commands is not None
        assert extractor.compress_commands is not None
        assert ".zip" in extractor.extract_commands
        assert ".zip" in extractor.compress_commands
    
    def test_extract_nonexistent_file(self):
        """Test extracting a non-existent file."""
        extractor = ArcFileExtractor()
        result = extractor.extract("nonexistent.zip")
        assert result == 1
    
    def test_extract_unsupported_format(self):
        """Test extracting an unsupported format."""
        extractor = ArcFileExtractor()
        with tempfile.NamedTemporaryFile(suffix=".unknown") as tmp:
            result = extractor.extract(tmp.name)
            assert result == 1
    
    def test_compress_nonexistent_source(self):
        """Test compressing a non-existent source."""
        extractor = ArcFileExtractor()
        result = extractor.compress("nonexistent")
        assert result == 1
    
    def test_compress_unsupported_format(self):
        """Test compressing to an unsupported format."""
        extractor = ArcFileExtractor()
        with tempfile.TemporaryDirectory() as tmp_dir:
            result = extractor.compress(tmp_dir, "output.unknown")
            assert result == 1
    
    @patch('subprocess.run')
    def test_extract_success(self, mock_run):
        """Test successful extraction."""
        mock_run.return_value = MagicMock(returncode=0)
        extractor = ArcFileExtractor()
        
        with tempfile.NamedTemporaryFile(suffix=".zip") as tmp:
            result = extractor.extract(tmp.name)
            assert result == 0
            mock_run.assert_called_once()
    
    @patch('subprocess.run')
    def test_compress_success(self, mock_run):
        """Test successful compression."""
        mock_run.return_value = MagicMock(returncode=0)
        extractor = ArcFileExtractor()
        
        with tempfile.TemporaryDirectory() as tmp_dir:
            result = extractor.compress(tmp_dir, "output.zip")
            assert result == 0
            mock_run.assert_called_once()


class TestUtils:
    """Test cases for utility functions."""
    
    def test_get_supported_formats(self):
        """Test getting supported formats."""
        formats = utils.get_supported_formats()
        assert "extract" in formats
        assert "compress" in formats
        assert ".zip" in formats["extract"]
        assert ".zip" in formats["compress"]
    
    def test_validate_file_path_nonexistent(self):
        """Test validating non-existent file path."""
        result = utils.validate_file_path("nonexistent.txt")
        assert result is False
    
    def test_validate_file_path_existing(self):
        """Test validating existing file path."""
        with tempfile.NamedTemporaryFile() as tmp:
            result = utils.validate_file_path(tmp.name)
            assert result is True
    
    def test_get_file_size_nonexistent(self):
        """Test getting file size for non-existent file."""
        result = utils.get_file_size("nonexistent.txt")
        assert result == "Unknown"
    
    def test_get_file_size_existing(self):
        """Test getting file size for existing file."""
        with tempfile.NamedTemporaryFile() as tmp:
            tmp.write(b"test content")
            tmp.flush()
            result = utils.get_file_size(tmp.name)
            assert result.endswith("B")
    
    @patch('shutil.which')
    def test_check_dependencies_all_present(self, mock_which):
        """Test checking dependencies when all are present."""
        mock_which.return_value = "/usr/bin/tool"
        result = utils.check_dependencies()
        assert result == []
    
    @patch('shutil.which')
    def test_check_dependencies_some_missing(self, mock_which):
        """Test checking dependencies when some are missing."""
        mock_which.return_value = None
        result = utils.check_dependencies()
        assert len(result) > 0
