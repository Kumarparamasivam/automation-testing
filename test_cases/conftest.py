# ==========================================
# File Name: conftest.py
# Purpose:
#   Define global fixtures, browser lifecycle controls, config parsers, and reporting hooks
# ==========================================

import os
import sys

# Append project root directory to sys.path for direct module import resolution
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from playwright.sync_api import sync_playwright
from utils.helpers import load_json_file
from utils.logger import logger
from utils.screenshot import capture_screenshot
from browser.browser_setup import init_browser

# Page Object Imports
from pages.login_page import LoginPage
from pages.signup_page import SignupPage
from pages.product_page import ProductPage
from pages.checkout_page import CheckoutPage

# ==========================================
# Fixture Name: config_data
# Purpose:
#   Load config settings dynamically from config.json
# ==========================================
@pytest.fixture(scope="session")
def config_data():
    config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config", "config.json")
    logger.info(f"Loading configuration file from: {config_path}")
    data = load_json_file(config_path)
    return data

# ==========================================
# Fixture Name: browser_context
# Purpose:
#   Manage Playwright browser launch, context separation, and teardown
# ==========================================
@pytest.fixture(scope="function")
def browser_context(config_data):
    browser_type = config_data.get("browser", "chromium")
    headless = config_data.get("headless", True)
    timeout = config_data.get("timeout", 10000)
    extension_path = config_data.get("extension_path", "")
    
    with sync_playwright() as p:
        browser, context, page = init_browser(
            playwright=p,
            browser_type=browser_type,
            headless=headless,
            timeout=timeout,
            extension_path=extension_path
        )
        
        # Yield page context to the test case
        yield page
        
        # Teardown
        logger.info("Closing browser context and page")
        try:
            page.close()
            context.close()
            if browser:
                browser.close()
        except Exception as e:
            logger.warning(f"Error during browser teardown: {str(e)}")

# ==========================================
# Fixture Name: page
# Purpose:
#   Provide direct page fixture mapping browser_context for easy accessibility
# ==========================================
@pytest.fixture(scope="function")
def page(browser_context):
    return browser_context

# ==========================================
# Fixtures for Page Objects
# Purpose:
#   Expose ready-to-use Page Object Model instances
# ==========================================
@pytest.fixture(scope="function")
def login_page(page, config_data):
    base_url = config_data.get("base_url", "http://127.0.0.1:5000")
    return LoginPage(page, base_url)

@pytest.fixture(scope="function")
def signup_page(page, config_data):
    base_url = config_data.get("base_url", "http://127.0.0.1:5000")
    return SignupPage(page, base_url)

@pytest.fixture(scope="function")
def product_page(page, config_data):
    base_url = config_data.get("base_url", "http://127.0.0.1:5000")
    return ProductPage(page, base_url)

@pytest.fixture(scope="function")
def checkout_page(page, config_data):
    base_url = config_data.get("base_url", "http://127.0.0.1:5000")
    return CheckoutPage(page, base_url)

# ==========================================
# Hook Name: pytest_runtest_makereport
# Purpose:
#   Intercept test execution status. On test failure, capture screenshot 
#   and link it to the generated pytest-html report.
# ==========================================
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, "extra", [])
    
    # We only take screenshot at the end of the test step 'call'
    if report.when == "call":
        # Check if test failed
        if report.failed:
            page_instance = item.funcargs.get("page")
            if page_instance:
                try:
                    # Capture screenshot using helper
                    screenshot_path = capture_screenshot(page_instance, item.name)
                    if screenshot_path and os.path.exists(screenshot_path):
                        # Construct a relative path for the HTML report
                        # Note: Reports are written to reports/report.html, screenshots are in screenshots/
                        # So relative path from reports/ is ../screenshots/filename
                        rel_path = f"../screenshots/{os.path.basename(screenshot_path)}"
                        
                        # Add to pytest-html extra elements
                        html_attachment = (
                            f'<div>'
                            f'  <span style="font-weight: bold; color: red;">Failure Screenshot:</span><br/>'
                            f'  <a href="{rel_path}" target="_blank">'
                            f'    <img src="{rel_path}" alt="screenshot" style="width: 320px; border: 1px solid #ccc; margin-top: 5px;"/>'
                            f'  </a>'
                            f'</div>'
                        )
                        # We try importing pytest_html.extras inside to avoid dependency issues if not installed yet
                        try:
                            import pytest_html
                            extra.append(pytest_html.extras.html(html_attachment))
                        except ImportError:
                            pass
                except Exception as e:
                    logger.error(f"Failed to attach screenshot to report: {str(e)}")
        report.extra = extra
