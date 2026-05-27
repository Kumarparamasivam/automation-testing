# ==========================================
# File Name: checkout_page.py
# Purpose:
#   Define page actions for cart review, checkout address info, and payment processing
# ==========================================

from pages.base_page import BasePage
import utils.constants as const
from utils.logger import logger

class CheckoutPage(BasePage):
    # ==========================================
    # Function Name: navigate_to_cart
    # Purpose:
    #   Go to the cart page
    # ==========================================
    def navigate_to_cart(self):
        self.navigate_to(const.CART_PATH)

    # ==========================================
    # Function Name: navigate_to_checkout
    # Purpose:
    #   Go to the checkout form page
    # ==========================================
    def navigate_to_checkout(self):
        self.navigate_to(const.CHECKOUT_PATH)

    # ==========================================
    # Function Name: navigate_to_payment
    # Purpose:
    #   Go directly to the payment input form
    # ==========================================
    def navigate_to_payment(self):
        self.navigate_to(const.PAYMENT_PATH)

    # ==========================================
    # Function Name: fill_checkout_details
    # Purpose:
    #   Complete shipping delivery parameters and advance
    #
    # Input:
    #   name (str): Shipping recipient name
    #   address (str): Delivery street address
    #   city (str): Delivery city name
    #   zip_code (str): Postal code
    # ==========================================
    def fill_checkout_details(self, name, address, city, zip_code):
        logger.info(f"Completing shipping address details for: {name}")
        self.fill_field(const.CHECKOUT_NAME_INPUT, name)
        self.fill_field(const.CHECKOUT_ADDRESS_INPUT, address)
        self.fill_field(const.CHECKOUT_CITY_INPUT, city)
        self.fill_field(const.CHECKOUT_ZIP_INPUT, zip_code)
        self.click_element(const.CHECKOUT_SUBMIT_BUTTON)

    # ==========================================
    # Function Name: get_cart_total
    # Purpose:
    #   Extract total shopping price from the billing label
    #
    # Output:
    #   str: Cart total price string
    # ==========================================
    def get_cart_total(self):
        return self.get_text(const.CART_TOTAL_PRICE)

    # ==========================================
    # Function Name: process_payment
    # Purpose:
    #   Fill and submit the mock payment card details form
    #
    # Input:
    #   card_name (str): Cardholder name
    #   card_number (str): 16-digit card number
    #   expiry (str): MM/YY exp date
    #   cvv (str): 3-digit verification code
    # ==========================================
    def process_payment(self, card_name, card_number, expiry, cvv):
        logger.info(f"Processing payment transaction under name: {card_name}")
        self.fill_field(const.CARD_NAME_INPUT, card_name)
        self.fill_field(const.CARD_NUMBER_INPUT, card_number)
        self.fill_field(const.CARD_EXPIRY_INPUT, expiry)
        self.fill_field(const.CARD_CVV_INPUT, cvv)
        self.click_element(const.PAYMENT_SUBMIT_BUTTON)

    # ==========================================
    # Function Name: get_payment_error
    # Purpose:
    #   Fetch errors regarding credit card validity warnings
    #
    # Output:
    #   str: The error message
    # ==========================================
    def get_payment_error(self):
        return self.get_text(const.PAYMENT_ERROR_MSG)

    # ==========================================
    # Function Name: get_order_confirmation_number
    # Purpose:
    #   Extract order reference ID upon successful transaction
    #
    # Output:
    #   str: Order reference code string
    # ==========================================
    def get_order_confirmation_number(self):
        try:
            self.page.wait_for_selector(const.ORDER_NUMBER_TEXT, state="visible", timeout=5000)
            return self.get_text(const.ORDER_NUMBER_TEXT)
        except Exception as e:
            logger.error(f"Failed to find order number: {str(e)}")
            return ""

    # ==========================================
    # Function Name: is_payment_successful
    # Purpose:
    #   Check if order confirmation message is showing
    #
    # Output:
    #   bool: True if payment transaction was successfully validated
    # ==========================================
    def is_payment_successful(self):
        return self.is_element_visible(const.PAYMENT_SUCCESS_HEADER)
