# ==========================================
# File Name: test_order.py
# Purpose:
#   Test suite for catalog searches, product filtering, and shopping cart increments
# ==========================================

import pytest
from utils.logger import logger

# ==========================================
# Test Case Name: test_product_search_success
# Purpose:
#   Verify searching for a valid product brings up matching cards
# ==========================================
def test_product_search_success(product_page):
    logger.info("Executing: test_product_search_success")
    
    # 1. Navigate to catalog page
    product_page.navigate_to_catalog()
    
    # 2. Search for a specific valid product (e.g. 'Laptop')
    product_page.search_product("Laptop")
    
    # 3. Assert matching items are displayed
    assert not product_page.is_no_products_message_visible(), "Product search for 'Laptop' returned empty results warning"
    
    # Check that at least one product card is found
    cards_count = product_page.page.locator(".product-card").count()
    assert cards_count > 0, "No product cards were shown on search success"
    logger.info("Test passed: test_product_search_success")

# ==========================================
# Test Case Name: test_product_search_empty
# Purpose:
#   Verify appropriate warning is visible when searching for non-existing products
# ==========================================
def test_product_search_empty(product_page):
    logger.info("Executing: test_product_search_empty")
    
    # 1. Navigate to catalog page
    product_page.navigate_to_catalog()
    
    # 2. Search for a dummy string
    product_page.search_product("NonExistentItem12345")
    
    # 3. Assert 'no products' notification is displayed
    assert product_page.is_no_products_message_visible(), "No search-empty message displayed for fake product"
    logger.info("Test passed: test_product_search_empty")

# ==========================================
# Test Case Name: test_add_to_cart_increments_badge
# Purpose:
#   Verify adding items to shopping cart increments the header count badge
# ==========================================
def test_add_to_cart_increments_badge(product_page):
    logger.info("Executing: test_add_to_cart_increments_badge")
    
    # 1. Navigate to catalog page
    product_page.navigate_to_catalog()
    
    # 2. Check initial count (should be 0)
    initial_count = product_page.get_cart_count()
    
    # 3. Add products to cart
    added = product_page.add_product_to_cart("Laptop")
    assert added, "Could not locate laptop product to add to cart"
    
    # 4. Check new badge count (should be initial_count + 1)
    new_count = product_page.get_cart_count()
    assert new_count == initial_count + 1, f"Cart badge count did not increment correctly. Expected {initial_count + 1}, got {new_count}"
    
    # Add another different product
    added2 = product_page.add_product_to_cart("Smartphone")
    assert added2, "Could not locate smartphone product to add to cart"
    
    new_count_2 = product_page.get_cart_count()
    assert new_count_2 == initial_count + 2, f"Cart badge did not increment on second item. Expected {initial_count + 2}, got {new_count_2}"
    logger.info("Test passed: test_add_to_cart_increments_badge")
