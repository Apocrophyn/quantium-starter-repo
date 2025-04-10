import pytest
from selenium.webdriver.chrome.options import Options

@pytest.fixture
def chrome_options():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    return options

def pytest_setup_options():
    return chrome_options() 