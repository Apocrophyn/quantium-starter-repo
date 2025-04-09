from dash.testing.application_runners import import_app
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pytest
from selenium import webdriver

# Import our app
from app import app

def pytest_setup_options():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    return options

@pytest.fixture
def test_client():
    """Create a test client for the app."""
    return app.server.test_client()

def test_header_presence(test_client):
    """Test that the header is present and contains the correct text"""
    response = test_client.get('/')
    assert response.status_code == 200
    assert b'Soul Foods Pink Morsel Sales Analysis' in response.data

def test_visualization_presence(test_client):
    """Test that the visualization graph is present"""
    response = test_client.get('/')
    assert response.status_code == 200
    assert b'sales-chart' in response.data

def test_region_picker_presence(test_client):
    """Test that the region picker is present and contains all expected options"""
    response = test_client.get('/')
    assert response.status_code == 200
    # Check for radio button container
    assert b'region-filter' in response.data
    # Check for all region options
    for region in ['all', 'east', 'north', 'south', 'west']:
        assert region.encode() in response.data 