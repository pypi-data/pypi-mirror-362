"""
Test configuration for CraftX.py test suite.
Configures pytest settings and test discovery.
"""

import pytest
import os
import sys

# Add the project root to Python path for all tests
project_root = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, project_root)

# pytest configuration


def pytest_configure(config):
    """Configure pytest with custom settings."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )


def pytest_collection_modifyitems(config, items):
    """Modify collected test items."""
    # Add markers to tests based on their names or paths
    for item in items:
        # Mark slow tests
        if "slow" in item.name.lower():
            item.add_marker("slow")

        # Mark integration tests
        if "integration" in item.name.lower() or "test_integration" in str(item.fspath):
            item.add_marker("integration")
        else:
            item.add_marker("unit")


# Test fixtures


@pytest.fixture
def project_root():
    """Provide the project root directory path."""
    return os.path.dirname(os.path.dirname(__file__))


@pytest.fixture
def temp_log_file():
    """Provide a temporary log file for testing."""
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.log', delete=False) as f:
        f.write("Test log entry\n")
        temp_path = f.name

    yield temp_path

    # Cleanup
    if os.path.exists(temp_path):
        os.unlink(temp_path)


@pytest.fixture
def sample_chat_data():
    """Provide sample chat data for testing."""
    return {
        "session_id": "test_session",
        "messages": [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there!"}
        ],
        "timestamp": "2025-07-14T12:00:00Z"
    }
