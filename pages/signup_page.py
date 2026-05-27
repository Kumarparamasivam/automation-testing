# ==========================================
# File Name: signup_page.py
# Purpose:
#   Define page actions for user registration/signup workflows
# ==========================================

from pages.base_page import BasePage
import utils.constants as const
from utils.logger import logger

class SignupPage(BasePage):
    # ==========================================
    # Function Name: navigate_to_signup
    # Purpose:
    #   Go to the signup page endpoint
    # ==========================================
    def navigate_to_signup(self):
        self.navigate_to(const.SIGNUP_PATH)

    # ==========================================
    # Function Name: signup
    # Purpose:
    #   Complete and submit the registration form
    #
    # Input:
    #   name (str): Full name
    #   email (str): Target email
    #   password (str): Target password
    #   confirm_password (str): Target confirmation password
    #   gender (str): Dropdown value ('male', 'female', 'other')
    #   accept_terms (bool): Agreement confirmation checkbox
    #
    # Output:
    #   None
    # ==========================================
    def signup(self, name, email, password, confirm_password, gender, accept_terms=True):
        logger.info(f"Filling out registration form for: {name} ({email})")
        if name is not None:
            self.fill_field(const.SIGNUP_NAME_INPUT, name)
        if email is not None:
            self.fill_field(const.SIGNUP_EMAIL_INPUT, email)
        if password is not None:
            self.fill_field(const.SIGNUP_PASSWORD_INPUT, password)
        if confirm_password is not None:
            self.fill_field(const.SIGNUP_CONFIRM_PASSWORD_INPUT, confirm_password)
        if gender is not None:
            self.select_option(const.SIGNUP_GENDER_SELECT, gender)
        if accept_terms:
            self.check_checkbox(const.SIGNUP_TERMS_CHECKBOX)
            
        self.click_element(const.SIGNUP_SUBMIT_BUTTON)

    # ==========================================
    # Function Name: get_error_messages
    # Purpose:
    #   Retrieve form validation warnings from the error log element
    #
    # Output:
    #   str: Aggregated error messages text
    # ==========================================
    def get_error_messages(self):
        return self.get_text(const.SIGNUP_ERROR_LIST)

    # ==========================================
    # Function Name: is_signup_successful
    # Purpose:
    #   Check if success banner is visible
    #
    # Output:
    #   bool: True if registration was successful
    # ==========================================
    def is_signup_successful(self):
        return self.is_element_visible(const.SIGNUP_SUCCESS_BANNER)
