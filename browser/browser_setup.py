# ==========================================
# File Name: browser_setup.py
# Purpose:
#   Manage the lifecycle and configuration of Playwright browser instances
# ==========================================

import os
import tempfile
from utils.logger import logger

# ==========================================
# Function Name: init_browser
# Purpose:
#   Start a browser instance and return page/context based on configuration
#
# Input:
#   playwright (playwright.sync_api.Playwright): Playwright engine instance
#   browser_type (str): Type of browser ("chromium", "firefox", "webkit")
#   headless (bool): Run headless or headed
#   timeout (int): Base navigation timeout in ms
#   extension_path (str): Path to browser extension folder (optional, chromium only)
#
# Output:
#   tuple: (browser_instance, context_instance, page_instance)
#
# Error Handling:
#   Raises exception if browser launch fails, logging error state
# ==========================================
def init_browser(playwright, browser_type="chromium", headless=True, timeout=10000, extension_path=""):
    browser = None
    context = None
    page = None
    
    try:
        browser_type_lower = browser_type.lower()
        logger.info(f"Initializing browser: {browser_type_lower} (Headless: {headless})")
        
        # Determine browser engine
        if browser_type_lower == "chromium":
            engine = playwright.chromium
        elif browser_type_lower == "firefox":
            engine = playwright.firefox
        elif browser_type_lower == "webkit":
            engine = playwright.webkit
        else:
            logger.warning(f"Unknown browser '{browser_type}', defaulting to Chromium")
            engine = playwright.chromium
            browser_type_lower = "chromium"
            
        # Extension handling (Only supported on Chromium + Headed mode)
        if extension_path and os.path.exists(extension_path) and browser_type_lower == "chromium":
            logger.info(f"Loading extension from path: {extension_path}. Enforcing headed mode.")
            # Create a temp directory for persistent profile
            temp_profile_dir = tempfile.mkdtemp(prefix="playwright_profile_")
            
            # Persistent context is required to load chrome extensions
            context = engine.launch_persistent_context(
                user_data_dir=temp_profile_dir,
                headless=False,  # Extensions do not load in headless mode
                args=[
                    f"--disable-extensions-except={extension_path}",
                    f"--load-extension={extension_path}"
                ],
                viewport={"width": 1280, "height": 720}
            )
            page = context.pages[0] if context.pages else context.new_page()
            # Since we launched persistent context, we do not have a separate browser object
            browser = None 
            logger.info("Persistent browser context launched with extension.")
        else:
            # Standard launch
            if browser_type_lower == "chromium" and extension_path:
                logger.warning(f"Extension path provided but not found or not Chromium. Ignoring extension.")
                
            browser = engine.launch(headless=headless)
            context = browser.new_context(viewport={"width": 1280, "height": 720})
            page = context.new_page()
            logger.info("Standard browser launched successfully.")
            
        # Set default timeout
        page.set_default_timeout(timeout)
        return browser, context, page
        
    except Exception as e:
        logger.critical(f"Critical error launching browser: {str(e)}")
        # Perform clean-up if anything was partially created
        try:
            if context:
                context.close()
            if browser:
                browser.close()
        except Exception:
            pass
        raise e
