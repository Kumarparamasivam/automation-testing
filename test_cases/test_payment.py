# ==========================================
# File Name: test_payment.py
# Purpose:
#   Test suite for checkout submission, credit card validations, and CSS/layout style assertions
# ==========================================

import pytest
from utils.logger import logger
import utils.constants as const

# ==========================================
# Test Case Name: test_checkout_and_payment_flow
# Purpose:
#   Verify full order placement: shipping details, payment entry, and order number confirmation
# ==========================================
def test_checkout_and_payment_flow(product_page, checkout_page):
    logger.info("Executing: test_checkout_and_payment_flow")
    
    # 1. Add item to cart
    product_page.navigate_to_catalog()
    product_page.add_product_to_cart("Laptop")
    
    # 2. Proceed to Checkout form
    checkout_page.navigate_to_checkout()
    
    # 3. Enter shipping details
    checkout_page.fill_checkout_details(
        name="Abishek Kumar",
        address="123 Automation Lane",
        city="Chennai",
        zip_code="600001"
    )
    
    # 4. Fill credit card details
    # We will submit a valid mock card
    checkout_page.process_payment(
        card_name="Abishek Kumar",
        card_number="1234567812345678",
        expiry="12/28",
        cvv="123"
    )
    
    # 5. Assert payment confirmation
    assert checkout_page.is_payment_successful(), "Payment confirmation header was not displayed"
    
    order_id = checkout_page.get_order_confirmation_number()
    assert len(order_id) > 0, "No confirmation order reference number was generated"
    logger.info(f"Test passed: Order successfully created with ID: {order_id}")

# ==========================================
# Test Case Name: test_payment_validation_errors
# Purpose:
#   Verify that appropriate validations prevent checkouts with malformed card data
# ==========================================
def test_payment_validation_errors(product_page, checkout_page):
    logger.info("Executing: test_payment_validation_errors")
    
    # 1. Add item and go directly to payment page
    product_page.navigate_to_catalog()
    product_page.add_product_to_cart("Smartphone")
    checkout_page.navigate_to_payment()
    
    # 2. Enter invalid card details (e.g. short card number)
    checkout_page.process_payment(
        card_name="Abishek Kumar",
        card_number="123",  # Malformed card
        expiry="12/22",     # Expired MM/YY
        cvv="9"             # Invalid CVV
    )
    
    # 3. Assert error displays
    error_msg = checkout_page.get_payment_error()
    assert len(error_msg) > 0, "No card validation error displayed for malformed input"
    assert "invalid" in error_msg.lower() or "must be" in error_msg.lower() or "expired" in error_msg.lower(), f"Unexpected error: {error_msg}"
    assert not checkout_page.is_payment_successful(), "Checkout accepted invalid credit card details"
    logger.info("Test passed: test_payment_validation_errors")

# ==========================================
# Test Case Name: test_css_and_layout_validations
# Purpose:
#   Verify elements' styling, visibility, overlap, and disabled state via computed styles
# ==========================================
def test_css_and_layout_validations(checkout_page):
    logger.info("Executing: test_css_and_layout_validations")
    
    # Navigate to the special mock UI-validation page
    checkout_page.navigate_to(const.UI_VAL_PATH)
    
    # 1. Validate element visibility by style
    is_box_visible = checkout_page.validate_computed_visibility(const.VISIBLE_BOX)
    assert is_box_visible, "Expected VISIBLE_BOX to be styled as visible"
    
    # 2. Validate hidden element by style (element has opacity:0 or display:none)
    is_box_hidden = checkout_page.validate_computed_visibility(const.HIDDEN_BOX)
    assert not is_box_hidden, "Expected HIDDEN_BOX to be styled as hidden or opacity 0"
    
    # 3. Validate disabled button styles (should have opacity, disabled attribute or cursor: not-allowed)
    is_btn_disabled = checkout_page.validate_button_disabled(const.DISABLED_BTN)
    assert is_btn_disabled, "Expected DISABLED_BTN to have computed styling indicating disabled state"
    
    # 4. Validate overlapping elements (overlapping vs side-by-side elements)
    # The page contains overlapping elements BOX_A and BOX_B
    is_overlapping = checkout_page.validate_overlapping_elements(const.OVERLAP_BOX_A, const.OVERLAP_BOX_B)
    assert is_overlapping, "Expected overlap check to return True for intersecting elements"
    
    # 5. Check layout overflow within responsive containers
    # Resize viewport to small screen and check if responsive container is overflowing
    checkout_page.page.set_viewport_size({"width": 320, "height": 480})
    checkout_page.page.wait_for_timeout(500)
    
    # Check if children overflow the container or if responsive behaviors work correctly
    # Note: On the mock page, we will make sure layout shifts are tested.
    has_overflow = checkout_page.validate_layout_overflow("#responsive-child", const.RESPONSIVE_CONTAINER)
    # We will configure it to not overflow (responsive child has width: 100% or similar)
    assert not has_overflow, "Responsive layout failed: child overflow detected in container on small viewport"
    
    logger.info("Test passed: test_css_and_layout_validations")
