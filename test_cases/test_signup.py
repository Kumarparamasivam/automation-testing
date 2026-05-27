# ==========================================
# File Name: test_signup.py
# Purpose:
#   Test suite for user registration, input checks, and error boundaries
# ==========================================

import pytest
from utils.helpers import generate_random_email, generate_random_string
from utils.logger import logger

# ==========================================
# Test Case Name: test_successful_signup
# Purpose:
#   Verify registration flow operates correctly with unique random user details
# ==========================================
def test_successful_signup(signup_page):
    logger.info("Executing: test_successful_signup")
    
    # 1. Navigate to signup page
    signup_page.navigate_to_signup()
    
    # 2. Fill out user details
    name = f"Test User {generate_random_string(4)}"
    email = generate_random_email()
    password = "Password123!"
    
    signup_page.signup(name, email, password, password, "male", accept_terms=True)
    
    # 3. Assert success banner is present
    assert signup_page.is_signup_successful(), "Registration success banner was not displayed"
    logger.info("Test passed: test_successful_signup")

# ==========================================
# Test Case Name: test_signup_password_mismatch
# Purpose:
#   Verify validation failure when password and confirm password inputs do not match
# ==========================================
def test_signup_password_mismatch(signup_page):
    logger.info("Executing: test_signup_password_mismatch")
    
    # 1. Navigate to signup page
    signup_page.navigate_to_signup()
    
    # 2. Submit mismatched passwords
    email = generate_random_email()
    signup_page.signup("Mismatched User", email, "Password123!", "MismatchPassword!", "female", accept_terms=True)
    
    # 3. Assert error displays and registration failed
    error_text = signup_page.get_error_messages()
    assert len(error_text) > 0, "No errors displayed for mismatching password confirmation"
    assert "match" in error_text.lower(), f"Unexpected error message: {error_text}"
    assert not signup_page.is_signup_successful(), "User registered successfully despite mismatching passwords"
    logger.info("Test passed: test_signup_password_mismatch")

# ==========================================
# Test Case Name: test_signup_missing_fields
# Purpose:
#   Verify validations prevent submission when mandatory fields (like name or email) are missing
# ==========================================
def test_signup_missing_fields(signup_page):
    logger.info("Executing: test_signup_missing_fields")
    
    # 1. Navigate to signup page
    signup_page.navigate_to_signup()
    
    # 2. Try to signup with name and email set to empty
    signup_page.signup(name="", email="", password="Password123!", confirm_password="Password123!", gender="other", accept_terms=True)
    
    # 3. Assert validations trigger
    error_text = signup_page.get_error_messages()
    assert len(error_text) > 0, "No validation messages showing for missing fields"
    assert "required" in error_text.lower() or "missing" in error_text.lower() or "empty" in error_text.lower(), f"Unexpected error: {error_text}"
    assert not signup_page.is_signup_successful(), "User registered successfully without filling mandatory info"
    logger.info("Test passed: test_signup_missing_fields")
