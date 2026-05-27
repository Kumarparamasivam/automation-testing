# ==========================================
# File Name: validations.py
# Purpose:
#   Implement CSS and UI validation algorithms using computed styling and layout checks
# ==========================================

from utils.logger import logger

# ==========================================
# Function Name: get_computed_style_property
# Purpose:
#   Retrieve a CSS property value for an element using window.getComputedStyle()
#
# Input:
#   page (playwright.sync_api.Page): Playwright page context
#   selector (str): CSS selector for the element
#   property_name (str): Target style property (e.g. 'display', 'opacity')
#
# Output:
#   str: The computed value of the CSS property, or None on failure
#
# Error Handling:
#   Catches exceptions if selector is invalid or element is not found
# ==========================================
def get_computed_style_property(page, selector, property_name):
    try:
        # Wait briefly for element
        page.wait_for_selector(selector, state="attached", timeout=3000)
        
        js_code = """
            ([selector, prop]) => {
                const el = document.querySelector(selector);
                if (!el) return null;
                const style = window.getComputedStyle(el);
                return style[prop];
            }
        """
        return page.evaluate(js_code, [selector, property_name])
    except Exception as e:
        logger.error(f"Error fetching computed style '{property_name}' for selector '{selector}': {str(e)}")
        return None

# ==========================================
# Function Name: is_visible_by_style
# Purpose:
#   Determine visibility using computed style and bounding dimensions
#
# Input:
#   page (playwright.sync_api.Page): Playwright page
#   selector (str): CSS selector
#
# Output:
#   bool: True if element is visibly rendered, False otherwise
#
# Error Handling:
#   Returns False if element is missing or validation fails
# ==========================================
def is_visible_by_style(page, selector):
    try:
        # Check if the element exists in DOM first
        el = page.locator(selector).first
        if el.count() == 0:
            return False
            
        js_code = """
            (sel) => {
                const el = document.querySelector(sel);
                if (!el) return false;
                const style = window.getComputedStyle(el);
                if (style.display === 'none') return false;
                if (style.visibility === 'hidden') return false;
                if (parseFloat(style.opacity) === 0) return false;
                
                const rect = el.getBoundingClientRect();
                return rect.width > 0 && rect.height > 0;
            }
        """
        return page.evaluate(js_code, selector)
    except Exception as e:
        logger.error(f"Failed style visibility check on '{selector}': {str(e)}")
        return False

# ==========================================
# Function Name: is_button_disabled_by_style
# Purpose:
#   Check if button is disabled by attribute OR style (pointer-events, opacity, cursor)
#
# Input:
#   page (playwright.sync_api.Page): Playwright page
#   selector (str): CSS selector
#
# Output:
#   bool: True if disabled, False otherwise
#
# Error Handling:
#   Logs exceptions, defaults to False
# ==========================================
def is_button_disabled_by_style(page, selector):
    try:
        # Check standard DOM attribute first
        is_attr_disabled = page.locator(selector).first.is_disabled()
        if is_attr_disabled:
            return True
            
        js_code = """
            (sel) => {
                const el = document.querySelector(sel);
                if (!el) return false;
                const style = window.getComputedStyle(el);
                
                // Common indicators of styled-only disabled state
                const pointerEvents = style.pointerEvents;
                const cursor = style.cursor;
                const opacity = parseFloat(style.opacity);
                
                return pointerEvents === 'none' || cursor === 'not-allowed' || opacity < 0.5 || el.classList.contains('disabled');
            }
        """
        return page.evaluate(js_code, selector)
    except Exception as e:
        logger.error(f"Failed disabled button check on '{selector}': {str(e)}")
        return False

# ==========================================
# Function Name: check_elements_overlap
# Purpose:
#   Verify if bounding boxes of two elements overlap in the layout
#
# Input:
#   page (playwright.sync_api.Page): Playwright page
#   selector_a (str): First selector
#   selector_b (str): Second selector
#
# Output:
#   bool: True if elements overlap, False otherwise
#
# Error Handling:
#   Returns False if any element is missing
# ==========================================
def check_elements_overlap(page, selector_a, selector_b):
    try:
        js_code = """
            ([selA, selB]) => {
                const elA = document.querySelector(selA);
                const elB = document.querySelector(selB);
                if (!elA || !elB) return false;
                
                const rA = elA.getBoundingClientRect();
                const rB = elB.getBoundingClientRect();
                
                // Check intersection of bounding rectangles
                return !(rA.right <= rB.left || 
                         rA.left >= rB.right || 
                         rA.bottom <= rB.top || 
                         rA.top >= rB.bottom);
            }
        """
        return page.evaluate(js_code, [selector_a, selector_b])
    except Exception as e:
        logger.error(f"Overlap validation exception between '{selector_a}' and '{selector_b}': {str(e)}")
        return False

# ==========================================
# Function Name: check_layout_overflow
# Purpose:
#   Verify if a child element overflows its parent boundaries (layout issue)
#
# Input:
#   page (playwright.sync_api.Page): Playwright page
#   selector_child (str): Child element selector
#   selector_parent (str): Parent element selector
#
# Output:
#   bool: True if child overflows parent, False otherwise
#
# Error Handling:
#   Logs exceptions, defaults to False
# ==========================================
def check_layout_overflow(page, selector_child, selector_parent):
    try:
        js_code = """
            ([selChild, selParent]) => {
                const child = document.querySelector(selChild);
                const parent = document.querySelector(selParent);
                if (!child || !parent) return false;
                
                const c = child.getBoundingClientRect();
                const p = parent.getBoundingClientRect();
                
                return c.left < p.left || c.right > p.right || c.top < p.top || c.bottom > p.bottom;
            }
        """
        return page.evaluate(js_code, [selector_child, selector_parent])
    except Exception as e:
        logger.error(f"Layout overflow exception between '{selector_child}' and '{selector_parent}': {str(e)}")
        return False
