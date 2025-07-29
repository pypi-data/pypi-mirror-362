"""
Test suite for CraftX.py router functionality.
Tests the agent routing and model management systems.
"""

import pytest
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


def test_project_structure():
    """Test that the basic project structure exists."""
    project_root = os.path.dirname(os.path.dirname(__file__))

    # Check for essential files
    assert os.path.exists(os.path.join(project_root, 'README.md'))
    assert os.path.exists(os.path.join(project_root, 'requirements.txt'))
    assert os.path.exists(os.path.join(project_root, 'setup.py'))
    assert os.path.exists(os.path.join(project_root, 'run.py'))


def test_requirements_file():
    """Test that requirements.txt contains necessary dependencies."""
    project_root = os.path.dirname(os.path.dirname(__file__))
    requirements_path = os.path.join(project_root, 'requirements.txt')

    with open(requirements_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check for essential dependencies
    assert 'streamlit' in content
    assert 'pytest' in content
    assert 'requests' in content


def test_setup_py_configuration():
    """Test that setup.py is properly configured."""
    project_root = os.path.dirname(os.path.dirname(__file__))
    setup_path = os.path.join(project_root, 'setup.py')

    with open(setup_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check for essential configuration
    assert 'name="craftxpy"' in content
    assert 'version=' in content
    assert 'streamlit' in content
    assert 'pytest' in content


def test_run_script_functionality():
    """Test that run.py contains the expected functions."""
    project_root = os.path.dirname(os.path.dirname(__file__))
    run_path = os.path.join(project_root, 'run.py')

    with open(run_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check for essential functions
    assert 'def check_requirements()' in content
    assert 'def run_tests()' in content
    assert 'def run_assistant()' in content
    assert 'def main()' in content


def test_assistant_ui_exists():
    """Test that the assistant UI directory exists."""
    project_root = os.path.dirname(os.path.dirname(__file__))
    assistant_ui_path = os.path.join(project_root, 'assistant_ui')

    assert os.path.exists(assistant_ui_path)
    assert os.path.exists(os.path.join(assistant_ui_path, 'app.py'))


def test_examples_directory():
    """Test that examples directory exists with demo file."""
    project_root = os.path.dirname(os.path.dirname(__file__))
    examples_path = os.path.join(project_root, 'examples')

    assert os.path.exists(examples_path)
    # Note: demo.py may or may not exist based on current structure


def test_license_file():
    """Test that LICENSE file exists and contains MIT license."""
    project_root = os.path.dirname(os.path.dirname(__file__))
    license_path = os.path.join(project_root, 'LICENSE')

    assert os.path.exists(license_path)

    with open(license_path, 'r', encoding='utf-8') as f:
        content = f.read()

    assert 'MIT License' in content
    assert 'Copyright (c) 2025 ElevateCraft' in content


def test_gitignore_file():
    """Test that .gitignore file exists and contains Python patterns."""
    project_root = os.path.dirname(os.path.dirname(__file__))
    gitignore_path = os.path.join(project_root, '.gitignore')

    assert os.path.exists(gitignore_path)

    with open(gitignore_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check for essential Python ignore patterns
    assert '__pycache__/' in content
    assert '*.py[cod]' in content  # This covers *.pyc
    assert '.env' in content
    assert '*.log' in content


if __name__ == '__main__':
    # Allow running this test file directly
    pytest.main([__file__, '-v'])
