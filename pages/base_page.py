# ==========================================
# File Name: base_page.py
# Purpose:
#   Define base object behaviors, locators, custom wrapper functions and visual validation bindings
# ==========================================

from utils.logger import logger
from utils.validations import is_visible_by_style, is_button_disabled_by_style, check_elements_overlap, check_layout_overflow

class BasePage:
    # ==========================================
    # Class Name: BasePage
    # Purpose:
    #   Initialize Page Object Base configuration
    #
    # Input:
    #   page (playwright.sync_api.Page): Playwright page context
    #   base_url (str): Target base url string
    # ==========================================
    def __init__(self, page, base_url=""):
        self.page = page
        self.base_url = base_url

    # ==========================================
    # Function Name: navigate_to
    # Purpose:
    #   Navigate to a URL path relative to the base URL
    #
    # Input:
    #   path (str): Relative path (e.g. "/login")
    #
    # Output:
    #   None
    #
    # Error Handling:
    #   Logs error and raises navigation exception
    # ==========================================
    def navigate_to(self, path=""):
        target_url = f"{self.base_url}{path}" if self.base_url else path
        try:
            logger.info(f"Navigating to: {target_url}")
            self.page.goto(target_url, wait_until="load")
        except Exception as e:
            logger.error(f"Failed to navigate to {target_url}: {str(e)}")
            raise e

    # ==========================================
    # Function Name: click_element
    # Purpose:
    #   Click on a selected DOM node safely
    #
    # Input:
    #   selector (str): CSS selector string
    #   timeout (int): Maximum time to wait
    #
    # Output:
    #   None
    #
    # Error Handling:
    #   Logs failure and raises exception if interaction fails
    # ==========================================
    def click_element(self, selector, timeout=5000):
        try:
            logger.info(f"Clicking element: {selector}")
            self.page.wait_for_selector(selector, state="visible", timeout=timeout)
            self.page.click(selector)
        except Exception as e:
            logger.error(f"Failed to click element '{selector}': {str(e)}")
            raise e

    # ==========================================
    # Function Name: fill_field
    # Purpose:
    #   Input text characters into a text field safely
    #
    # Input:
    #   selector (str): CSS Selector string
    #   value (str): Text characters to input
    #   timeout (int): Wait timeout in milliseconds
    #
    # Output:
    #   None
    #
    # Error Handling:
    #   Raises exception on failure to input
    # ==========================================
    def fill_field(self, selector, value, timeout=5000):
        try:
            logger.info(f"Filling field '{selector}' with values.")
            self.page.wait_for_selector(selector, state="visible", timeout=timeout)
            self.page.fill(selector, value)
        except Exception as e:
            logger.error(f"Failed to fill field '{selector}': {str(e)}")
            raise e

    # ==========================================
    # Function Name: check_checkbox
    # Purpose:
    #   Check a checkbox element
    #
    # Input:
    #   selector (str): CSS selector
    #
    # Output:
    #   None
    #
    # Error Handling:
    #   Raises exception if checkbox is missing or disabled
    # ==========================================
    def check_checkbox(self, selector):
        try:
            logger.info(f"Checking checkbox: {selector}")
            self.page.wait_for_selector(selector, state="visible", timeout=5000)
            self.page.check(selector)
        except Exception as e:
            logger.error(f"Failed to check checkbox '{selector}': {str(e)}")
            raise e

    # ==========================================
    # Function Name: select_option
    # Purpose:
    #   Select an option in dropdown element
    #
    # Input:
    #   selector (str): CSS selector
    #   value_or_label (str): Value or label to select
    #
    # Output:
    #   None
    # ==========================================
    def select_option(self, selector, value_or_label):
        try:
            logger.info(f"Selecting option '{value_or_label}' in dropdown '{selector}'")
            self.page.wait_for_selector(selector, state="visible", timeout=5000)
            self.page.select_option(selector, value=value_or_label)
        except Exception as e:
            logger.error(f"Failed to select option in '{selector}': {str(e)}")
            raise e

    # ==========================================
    # Function Name: get_text
    # Purpose:
    #   Retrieve inner text value of selector
    #
    # Input:
    #   selector (str): CSS Selector
    #
    # Output:
    #   str: Element's inner text
    # ==========================================
    def get_text(self, selector):
        try:
            self.page.wait_for_selector(selector, state="attached", timeout=5000)
            return self.page.inner_text(selector).strip()
        except Exception as e:
            logger.error(f"Failed to extract text from '{selector}': {str(e)}")
            return ""

    # ==========================================
    # Function Name: is_element_visible
    # Purpose:
    #   Check standard visibility state of selector (DOM state check)
    #
    # Input:
    #   selector (str): CSS selector
    #
    # Output:
    #   bool: True if visible, False otherwise
    # ==========================================
    def is_element_visible(self, selector):
        try:
            return self.page.locator(selector).first.is_visible()
        except Exception:
            return False

    # ==========================================
    # Function Name: validate_computed_visibility
    # Purpose:
    #   Validate elements' visual rendering using window.getComputedStyle()
    #
    # Input:
    #   selector (str): Target selector
    #
    # Output:
    #   bool: True if visible according to styling rules, False if hidden
    # ==========================================
    def validate_computed_visibility(self, selector):
        return is_visible_by_style(self.page, selector)

    # ==========================================
    # Function Name: validate_button_disabled
    # Purpose:
    #   Validate if a button is disabled using standard traits and computed styles
    #
    # Input:
    #   selector (str): Target selector
    #
    # Output:
    #   bool: True if disabled, False otherwise
    # ==========================================
    def validate_button_disabled(self, selector):
        return is_button_disabled_by_style(self.page, selector)

    # ==========================================
    # Function Name: validate_overlapping_elements
    # Purpose:
    #   Check if two components overlap on the layout sheet
    #
    # Input:
    #   selector_a (str): First selector
    #   selector_b (str): Second selector
    #
    # Output:
    #   bool: True if overlap is detected
    # ==========================================
    def validate_overlapping_elements(self, selector_a, selector_b):
        return check_elements_overlap(self.page, selector_a, selector_b)

    # ==========================================
    # Function Name: validate_layout_overflow
    # Purpose:
    #   Check if an element overflows its container boundary
    #
    # Input:
    #   selector_child (str): Child selector
    #   selector_parent (str): Parent container selector
    #
    # Output:
    #   bool: True if child overflows parent
    # ==========================================
    def validate_layout_overflow(self, selector_child, selector_parent):
        return check_layout_overflow(self.page, selector_child, selector_parent)
