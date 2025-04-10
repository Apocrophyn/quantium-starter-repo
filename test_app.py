import pytest
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from dash.testing.application_runners import import_app

def pytest_setup_options():
    options = Options()
    options.add_argument('--headless')
    return options

@pytest.fixture
def dash_duo(dash_duo):
    dash_duo.driver.set_window_size(1280, 800)
    return dash_duo

def test_header_presence(dash_duo):
    """Test that the header is present and contains the correct text"""
    app = import_app("app")
    dash_duo.start_server(app)
    dash_duo.wait_for_text_to_equal("h1", "Soul Foods Pink Morsel Sales Analysis", timeout=4)

def test_visualization_presence(dash_duo):
    """Test that the visualization graph is present"""
    app = import_app("app")
    dash_duo.start_server(app)
    dash_duo.wait_for_element("#sales-chart", timeout=4)

def test_region_picker_presence(dash_duo):
    """Test that the region picker is present and contains all expected options"""
    app = import_app("app")
    dash_duo.start_server(app)
    dash_duo.wait_for_element("#region-filter", timeout=4)
    
    # Check each region option is present
    expected_regions = ["EAST", "NORTH", "SOUTH", "WEST"]
    for region in expected_regions:
        element = dash_duo.find_element(f'#region-filter input[value="{region}"]')
        assert element is not None, f"Region {region} not found" 