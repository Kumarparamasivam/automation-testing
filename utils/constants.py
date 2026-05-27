# ==========================================
# File Name: constants.py
# Purpose:
#   Centralize framework-wide selectors, timeouts, endpoints, and status messages
# ==========================================

# Timeouts in milliseconds
DEFAULT_TIMEOUT = 10000
SHORT_TIMEOUT = 3000
LONG_TIMEOUT = 20000

# Mock Site Endpoints
LOGIN_PATH = "/mock/login"
SIGNUP_PATH = "/mock/signup"
CATALOG_PATH = "/mock/catalog"
CART_PATH = "/mock/cart"
CHECKOUT_PATH = "/mock/checkout"
PAYMENT_PATH = "/mock/payment"
FORM_VAL_PATH = "/mock/form-validation"
NAV_PATH = "/mock/navigation"
UI_VAL_PATH = "/mock/ui-validation"

# CSS Selectors for login_page.py
LOGIN_USERNAME_INPUT = "#username"
LOGIN_PASSWORD_INPUT = "#password"
LOGIN_SUBMIT_BUTTON = "#login-btn"
LOGIN_ERROR_MESSAGE = ".error-message"
LOGIN_SUCCESS_BANNER = ".success-banner"
LOGOUT_BUTTON = "#logout-btn"

# CSS Selectors for signup_page.py
SIGNUP_NAME_INPUT = "#signup-name"
SIGNUP_EMAIL_INPUT = "#signup-email"
SIGNUP_PASSWORD_INPUT = "#signup-password"
SIGNUP_CONFIRM_PASSWORD_INPUT = "#signup-confirm-password"
SIGNUP_GENDER_SELECT = "#signup-gender"
SIGNUP_TERMS_CHECKBOX = "#signup-terms"
SIGNUP_SUBMIT_BUTTON = "#signup-btn"
SIGNUP_ERROR_LIST = ".error-list"
SIGNUP_SUCCESS_BANNER = ".signup-success"

# CSS Selectors for product_page.py
SEARCH_INPUT = "#search-box"
SEARCH_BUTTON = "#search-btn"
PRODUCT_CARD = ".product-card"
PRODUCT_NAME = ".product-name"
ADD_TO_CART_BUTTON = ".add-to-cart-btn"
CART_COUNT_BADGE = "#cart-count"
PRODUCT_NOT_FOUND = ".no-products-msg"

# CSS Selectors for checkout_page.py
CHECKOUT_NAME_INPUT = "#checkout-name"
CHECKOUT_ADDRESS_INPUT = "#checkout-address"
CHECKOUT_CITY_INPUT = "#checkout-city"
CHECKOUT_ZIP_INPUT = "#checkout-zip"
CHECKOUT_SUBMIT_BUTTON = "#checkout-submit-btn"
CART_ITEMS_TABLE = "#cart-items-table"
CART_TOTAL_PRICE = "#cart-total-price"

# CSS Selectors for payment_page.py
CARD_NAME_INPUT = "#card-name"
CARD_NUMBER_INPUT = "#card-number"
CARD_EXPIRY_INPUT = "#card-expiry"
CARD_CVV_INPUT = "#card-cvv"
PAYMENT_SUBMIT_BUTTON = "#pay-btn"
PAYMENT_ERROR_MSG = "#payment-error"
PAYMENT_SUCCESS_HEADER = "#payment-success-header"
ORDER_NUMBER_TEXT = "#order-number"

# CSS Selectors for UI validations page
VISIBLE_BOX = "#visible-box"
HIDDEN_BOX = "#hidden-box"
DISABLED_BTN = "#disabled-btn"
OVERLAP_BOX_A = "#overlap-a"
OVERLAP_BOX_B = "#overlap-b"
RESPONSIVE_CONTAINER = ".responsive-container"
