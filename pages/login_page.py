# ==========================================
# File Name: login_page.py
# Purpose:
#   Define page actions for authentication and login/logout workflows
# ==========================================

from pages.base_page import BasePage
import utils.constants as const
from utils.logger import logger

class LoginPage(BasePage):
    # ==========================================
    # Function Name: navigate_to_login
    # Purpose:
    #   Go to the login page endpoint
    # ==========================================
    def navigate_to_login(self):
        self.navigate_to(const.LOGIN_PATH)

    # ==========================================
    # Function Name: login
    # Purpose:
    #   Perform login action with given username and password
    #
    # Input:
    #   username (str)
    #   password (str)
    #
    # Output:
    #   None
    # ==========================================
    def login(self, username, password):
        logger.info(f"Performing login for user: {username}")
        self.fill_field(const.LOGIN_USERNAME_INPUT, username)
        self.fill_field(const.LOGIN_PASSWORD_INPUT, password)
        self.click_element(const.LOGIN_SUBMIT_BUTTON)

    # ==========================================
    # Function Name: get_error_message
    # Purpose:
    #   Retrieve validation error alert text from the page
    #
    # Output:
    #   str: Error message string
    # ==========================================
    def get_error_message(self):
        return self.get_text(const.LOGIN_ERROR_MESSAGE)

    # ==========================================
    # Function Name: is_login_successful
    # Purpose:
    #   Check if successful login banner is visible or logout button exists
    #
    # Output:
    #   bool: True if logged in successfully
    # ==========================================
    def is_login_successful(self):
        # We can check if the success banner is visible, or if we redirected to catalog, or if logout button exists
        return self.is_element_visible(const.LOGOUT_BUTTON) or self.is_element_visible(const.LOGIN_SUCCESS_BANNER)

    # ==========================================
    # Function Name: logout
    # Purpose:
    #   Log out the current active session
    # ==========================================
    def logout(self):
        logger.info("Logging out current user session")
        self.click_element(const.LOGOUT_BUTTON)
