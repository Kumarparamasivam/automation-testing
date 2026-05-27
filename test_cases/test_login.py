# ==========================================
# File Name: test_login.py
# Purpose:
#   Test suite for authentication: valid logins, invalid logins, and session logouts
# ==========================================

import pytest
from utils.logger import logger

# ==========================================
# Test Case Name: test_successful_login
# Purpose:
#   Verify that a user with valid credentials can log in and view the catalog
# ==========================================
def test_successful_login(login_page, config_data):
    logger.info("Executing: test_successful_login")
    
    # 1. Navigate to login page
    login_page.navigate_to_login()
    
    # 2. Enter valid credentials
    username = config_data.get("username", "testuser")
    password = config_data.get("password", "Password123!")
    login_page.login(username, password)
    
    # 3. Assert successful redirection/view
    assert login_page.is_login_successful(), "Login failed: Success banner or logout button not visible"
    logger.info("Test passed: test_successful_login")

# ==========================================
# Test Case Name: test_invalid_login
# Purpose:
#   Verify that appropriate error message is shown when submitting wrong password
# ==========================================
def test_invalid_login(login_page, config_data):
    logger.info("Executing: test_invalid_login")
    
    # 1. Navigate to login page
    login_page.navigate_to_login()
    
    # 2. Enter invalid credentials
    username = config_data.get("username", "testuser")
    login_page.login(username, "WrongPassword!")
    
    # 3. Assert failure messages are displayed
    error_msg = login_page.get_error_message()
    assert len(error_msg) > 0, "No error message displayed for invalid login credentials"
    assert "invalid" in error_msg.lower() or "incorrect" in error_msg.lower(), f"Unexpected error message: {error_msg}"
    
    # Assert not logged in
    assert not login_page.is_login_successful(), "Session marked as logged in despite invalid credentials"
    logger.info("Test passed: test_invalid_login")

# ==========================================
# Test Case Name: test_logout
# Purpose:
#   Verify that an authenticated user can sign out successfully
# ==========================================
def test_logout(login_page, config_data):
    logger.info("Executing: test_logout")
    
    # 1. Login first
    login_page.navigate_to_login()
    login_page.login(config_data.get("username"), config_data.get("password"))
    assert login_page.is_login_successful(), "Pre-requisite login failed"
    
    # 2. Trigger logout
    login_page.logout()
    
    # 3. Assert logged out state
    assert not login_page.is_login_successful(), "User still logged in after executing logout action"
    logger.info("Test passed: test_logout")
