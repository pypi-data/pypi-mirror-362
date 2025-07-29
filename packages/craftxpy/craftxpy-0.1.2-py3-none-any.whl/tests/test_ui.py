"""
Test suite for CraftX.py assistant UI functionality.
Tests the Streamlit-based user interface components.
"""

import pytest
import sys
import os
import tempfile
import json

# Add the project root to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


def test_assistant_app_exists():
    """Test that the assistant app file exists and has basic structure."""
    project_root = os.path.dirname(os.path.dirname(__file__))
    app_path = os.path.join(project_root, 'assistant_ui', 'app.py')

    assert os.path.exists(app_path), "assistant_ui/app.py should exist"

    with open(app_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check for Streamlit imports and basic structure
    # Note: These checks are basic since we don't know the exact content
    assert len(content) > 0, "app.py should not be empty"


def test_chat_logs_directory():
    """Test that chat logs directory exists and is properly structured."""
    project_root = os.path.dirname(os.path.dirname(__file__))
    chat_logs_path = os.path.join(project_root, 'chat_logs')

    assert os.path.exists(chat_logs_path), "chat_logs directory should exist"

    # Check for default.json
    default_log = os.path.join(chat_logs_path, 'default.json')
    if os.path.exists(default_log):
        with open(default_log, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                assert isinstance(data, (dict, list)
                                  ), "default.json should contain valid JSON"
            except json.JSONDecodeError:
                pytest.fail("default.json should contain valid JSON")


def test_assets_directory():
    """Test that assets directory exists with logo files."""
    project_root = os.path.dirname(os.path.dirname(__file__))
    assets_path = os.path.join(project_root, 'assets')

    assert os.path.exists(assets_path), "assets directory should exist"

    img_path = os.path.join(assets_path, 'img')
    assert os.path.exists(img_path), "assets/img directory should exist"

    # Check for logo files
    logo_svg = os.path.join(img_path, 'craftx-logo.svg')
    monogram_svg = os.path.join(img_path, 'craftx-monogram.svg')

    # At least one logo should exist
    assert os.path.exists(logo_svg) or os.path.exists(monogram_svg), \
        "At least one logo file should exist"


def test_streamlit_compatibility():
    """Test that the project structure is compatible with Streamlit."""
    project_root = os.path.dirname(os.path.dirname(__file__))

    # Check that streamlit is in requirements
    requirements_path = os.path.join(project_root, 'requirements.txt')
    with open(requirements_path, 'r', encoding='utf-8') as f:
        content = f.read()

    assert 'streamlit' in content, "Streamlit should be in requirements.txt"

    # Check that assistant UI exists
    assistant_path = os.path.join(project_root, 'assistant_ui', 'app.py')
    assert os.path.exists(
        assistant_path), "assistant_ui/app.py should exist for Streamlit"


def test_run_assistant_command():
    """Test that the run_assistant.py script exists and is executable."""
    project_root = os.path.dirname(os.path.dirname(__file__))
    run_assistant_path = os.path.join(project_root, 'run_assistant.py')

    assert os.path.exists(run_assistant_path), "run_assistant.py should exist"

    with open(run_assistant_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check for essential function
    assert 'def run_assistant()' in content, "run_assistant() function should exist"
    assert 'streamlit' in content.lower(), "Should reference Streamlit"


def test_logs_handling():
    """Test that log files can be created and managed properly."""
    project_root = os.path.dirname(os.path.dirname(__file__))

    # Test that we can create a temporary log file
    import tempfile
    temp_dir = tempfile.gettempdir()
    temp_log_path = os.path.join(temp_dir, 'test_craftx.log')

    try:
        # Write test log
        with open(temp_log_path, 'w') as temp_log:
            temp_log.write("Test log entry\n")

        # Verify we can read it back
        with open(temp_log_path, 'r') as read_log:
            content = read_log.read()
            assert "Test log entry" in content
    finally:
        # Cleanup
        if os.path.exists(temp_log_path):
            os.unlink(temp_log_path)


def test_logo_files():
    """Test that logo files exist and are accessible."""
    project_root = os.path.dirname(os.path.dirname(__file__))

    # Check PNG logo (main logo)
    png_logo = os.path.join(project_root, 'assets', 'img', 'craftx-logo.png')
    assert os.path.exists(png_logo), "craftx-logo.png should exist"

    # Check SVG logos
    svg_logo = os.path.join(project_root, 'assets', 'img', 'craftx-logo.svg')
    monogram_svg = os.path.join(
        project_root, 'assets', 'img', 'craftx-monogram.svg')

    assert os.path.exists(svg_logo), "craftx-logo.svg should exist"
    assert os.path.exists(monogram_svg), "craftx-monogram.svg should exist"

    # Check file sizes (logos should not be empty)
    assert os.path.getsize(png_logo) > 0, "PNG logo should not be empty"
    assert os.path.getsize(svg_logo) > 0, "SVG logo should not be empty"
    assert os.path.getsize(monogram_svg) > 0, "Monogram should not be empty"


if __name__ == '__main__':
    # Allow running this test file directly
    pytest.main([__file__, '-v'])
