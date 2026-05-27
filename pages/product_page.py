# ==========================================
# File Name: product_page.py
# Purpose:
#   Define page actions for searching, filtering, and interacting with product listings
# ==========================================

from pages.base_page import BasePage
import utils.constants as const
from utils.logger import logger

class ProductPage(BasePage):
    # ==========================================
    # Function Name: navigate_to_catalog
    # Purpose:
    #   Go to the catalog page endpoint
    # ==========================================
    def navigate_to_catalog(self):
        self.navigate_to(const.CATALOG_PATH)

    # ==========================================
    # Function Name: search_product
    # Purpose:
    #   Enter a search keyword and trigger search query
    #
    # Input:
    #   keyword (str): The search phrase
    # ==========================================
    def search_product(self, keyword):
        logger.info(f"Searching catalog for keyword: {keyword}")
        self.fill_field(const.SEARCH_INPUT, keyword)
        self.click_element(const.SEARCH_BUTTON)

    # ==========================================
    # Function Name: add_product_to_cart
    # Purpose:
    #   Add a product to the cart by its name matching text
    #
    # Input:
    #   product_name (str): Product name exact or partial text
    #
    # Output:
    #   bool: True if click succeeded, False if product not found
    # ==========================================
    def add_product_to_cart(self, product_name):
        logger.info(f"Adding product to cart: {product_name}")
        try:
            # Wait for products to render in the DOM
            self.page.wait_for_selector(const.PRODUCT_CARD, state="visible", timeout=5000)
            
            # Locate product cards
            product_cards = self.page.locator(const.PRODUCT_CARD)
            count = product_cards.count()
            
            for i in range(count):
                card = product_cards.nth(i)
                name_el = card.locator(const.PRODUCT_NAME)
                name_text = name_el.inner_text().strip()
                
                if product_name.lower() in name_text.lower():
                    # Click add to cart button inside this specific card
                    card.locator(const.ADD_TO_CART_BUTTON).click()
                    logger.info(f"Successfully clicked 'Add to Cart' for '{product_name}'")
                    return True
                    
            logger.warning(f"Product '{product_name}' not found in the search listings.")
            return False
        except Exception as e:
            logger.error(f"Failed to add product '{product_name}' to cart: {str(e)}")
            raise e

    # ==========================================
    # Function Name: get_cart_count
    # Purpose:
    #   Retrieve the item count displayed on the shopping cart badge
    #
    # Output:
    #   int: Number of items in the cart
    # ==========================================
    def get_cart_count(self):
        try:
            badge_text = self.get_text(const.CART_COUNT_BADGE)
            if not badge_text:
                return 0
            return int(badge_text)
        except Exception as e:
            logger.error(f"Could not read cart badge: {str(e)}")
            return 0

    # ==========================================
    # Function Name: is_no_products_message_visible
    # Purpose:
    #   Check if search returned empty notification banner
    #
    # Output:
    #   bool: True if 'no products' warning is displayed
    # ==========================================
    def is_no_products_message_visible(self):
        return self.is_element_visible(const.PRODUCT_NOT_FOUND)
