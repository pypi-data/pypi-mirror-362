"""
Test suite for CraftX.py static website functionality.
Tests the HTML pages and static site structure.
"""

import pytest
import sys
import os
from pathlib import Path

# Add the project root to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


def test_static_website_files():
    """Test that all static website files exist."""
    project_root = os.path.dirname(os.path.dirname(__file__))

    # Check for main HTML files
    html_files = [
        'index.html',
        'docs.html',
        'examples.html',
        'about.html'
    ]

    for html_file in html_files:
        file_path = os.path.join(project_root, html_file)
        assert os.path.exists(file_path), f"{html_file} should exist"

        # Check file is not empty
        assert os.path.getsize(
            file_path) > 0, f"{html_file} should not be empty"


def test_index_html_content():
    """Test that index.html contains expected content."""
    project_root = os.path.dirname(os.path.dirname(__file__))
    index_path = os.path.join(project_root, 'index.html')

    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check for essential content
    assert 'CraftX.py' in content
    assert 'Python-native intelligence' in content
    assert 'modular by design' in content
    assert 'assets/img/craftx-logo.png' in content

    # Check for navigation
    assert 'docs.html' in content
    assert 'examples.html' in content
    assert 'about.html' in content


def test_docs_html_content():
    """Test that docs.html contains documentation content."""
    project_root = os.path.dirname(os.path.dirname(__file__))
    docs_path = os.path.join(project_root, 'docs.html')

    with open(docs_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check for documentation sections
    assert 'Documentation' in content
    assert 'Quick Start' in content
    assert 'Installation' in content
    assert 'Architecture' in content
    assert 'Testing' in content


def test_examples_html_content():
    """Test that examples.html contains code examples."""
    project_root = os.path.dirname(os.path.dirname(__file__))
    examples_path = os.path.join(project_root, 'examples.html')

    with open(examples_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check for examples content
    assert 'Examples' in content
    assert 'AgentRouter' in content
    assert 'BaseTool' in content
    assert 'streamlit run' in content


def test_about_html_content():
    """Test that about.html contains project information."""
    project_root = os.path.dirname(os.path.dirname(__file__))
    about_path = os.path.join(project_root, 'about.html')

    with open(about_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check for about page content
    assert 'About CraftX.py' in content
    assert 'Mission' in content
    assert 'Key Features' in content
    assert 'MIT License' in content
    assert 'assets/img/craftx-logo.png' in content


def test_github_pages_workflow():
    """Test that GitHub Pages workflow file exists."""
    project_root = os.path.dirname(os.path.dirname(__file__))
    workflow_path = os.path.join(
        project_root, '.github', 'workflows', 'deploy.yml')

    assert os.path.exists(workflow_path), "GitHub Pages workflow should exist"

    with open(workflow_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check for workflow content
    assert 'Deploy Static Website' in content
    assert 'actions/checkout' in content
    assert 'peaceiris/actions-gh-pages' in content


def test_html_file_validation():
    """Test that HTML files have basic valid structure."""
    project_root = os.path.dirname(os.path.dirname(__file__))

    html_files = ['index.html', 'docs.html', 'examples.html', 'about.html']

    for html_file in html_files:
        file_path = os.path.join(project_root, html_file)

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Basic HTML structure checks
        assert '<!DOCTYPE html>' in content, f"{html_file} should have DOCTYPE"
        assert '<html' in content, f"{html_file} should have html tag"
        assert '<head>' in content, f"{html_file} should have head section"
        assert '<body>' in content, f"{html_file} should have body section"
        assert '</html>' in content, f"{html_file} should close html tag"

        # Check for title
        assert '<title>' in content, f"{html_file} should have a title"


if __name__ == '__main__':
    # Allow running this test file directly
    pytest.main([__file__, '-v'])
