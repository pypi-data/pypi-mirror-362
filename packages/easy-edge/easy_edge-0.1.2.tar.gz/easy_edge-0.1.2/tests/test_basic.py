#!/usr/bin/env python3
"""
Basic tests for Easy Edge
"""

import pytest
import subprocess
import sys
from pathlib import Path

def test_help_command():
    """Test that the help command works"""
    result = subprocess.run([sys.executable, "easy_edge.py", "--help"], 
                          capture_output=True, text=True)
    assert result.returncode == 0
    assert "usage:" in result.stdout.lower()
    assert "--version" in result.stdout

def test_version_command():
    """Test that version command works"""
    result = subprocess.run([sys.executable, "easy_edge.py", "--version"], 
                          capture_output=True, text=True)
    # Version command should work and return 0
    assert result.returncode == 0
    assert "easy-edge" in result.stdout
    assert "1.0.0" in result.stdout

def test_models_directory_exists():
    """Test that models directory exists"""
    models_dir = Path("models")
    assert models_dir.exists(), "models directory should exist"
    assert models_dir.is_dir(), "models should be a directory"

def test_config_file_exists():
    """Test that config.json exists in models directory"""
    config_file = Path("models/config.json")
    assert config_file.exists(), "models/config.json should exist"

def test_build_script_exists():
    """Test that build script exists"""
    build_script = Path("build.py")
    assert build_script.exists(), "build.py should exist"

def test_requirements_file_exists():
    """Test that requirements.txt exists"""
    requirements_file = Path("requirements.txt")
    assert requirements_file.exists(), "requirements.txt should exist"

def test_package_json_exists():
    """Test that package.json exists"""
    package_json = Path("package.json")
    assert package_json.exists(), "package.json should exist" 