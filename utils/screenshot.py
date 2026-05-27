# ==========================================
# File Name: screenshot.py
# Purpose:
#   Provide automated screenshot capture services for test validations and failures
# ==========================================

import os
from datetime import datetime
from utils.logger import logger

# ==========================================
# Function Name: capture_screenshot
# Purpose:
#   Capture the current page view and save as PNG in the screenshots directory
#
# Input:
#   page (playwright.sync_api.Page): The active Playwright page instance
#   test_name (str): The name of the running test case to include in the file name
#
# Output:
#   str: The absolute or relative path to the saved screenshot, or None if failed
#
# Error Handling:
#   Catches and logs any exceptions raised during Playwright screenshot operation
# ==========================================
def capture_screenshot(page, test_name):
    try:
        # Resolve the root workspace directory
        root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        screenshot_dir = os.path.join(root_dir, "screenshots")
        
        # Ensure the directory exists
        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)
            
        # Standardize formatting for filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        sanitized_name = test_name.replace("[", "_").replace("]", "_").replace("/", "_").replace(":", "_")
        filename = f"{sanitized_name}_{timestamp}.png"
        file_path = os.path.join(screenshot_dir, filename)
        
        logger.info(f"Attempting to capture failure screenshot for: {test_name}")
        page.screenshot(path=file_path, full_page=True)
        logger.info(f"Screenshot successfully saved to: {file_path}")
        
        return file_path
    except Exception as e:
        logger.error(f"Failed to capture screenshot for test '{test_name}': {str(e)}")
        return None
