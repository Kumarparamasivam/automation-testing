# ==========================================
# File Name: main.py
# Purpose:
#   Primary application runner. Serves local control dashboard,
#   hosts local mock target e-commerce web app, and executes automation runs.
# ==========================================

import os
import re
import sys
import uuid
import queue
import threading
import subprocess
from datetime import datetime
from flask import Flask, render_template, request, jsonify, Response, session, redirect, url_for, send_from_directory

# Utility imports
from utils.logger import logger
from utils.helpers import load_json_file, save_json_file

app = Flask(__name__)
app.secret_key = "local_automation_framework_secret_key"

# Global paths
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
LOGS_DIR = os.path.join(ROOT_DIR, "logs")
REPORTS_DIR = os.path.join(ROOT_DIR, "reports")
SCREENSHOTS_DIR = os.path.join(ROOT_DIR, "screenshots")

# Ensure required directories exist
for folder in [LOGS_DIR, REPORTS_DIR, SCREENSHOTS_DIR]:
    os.makedirs(folder, exist_ok=True)

# Global execution state tracker
execution_state = {
    "is_running": False,
    "latest_status": "idle",
    "log_queue": queue.Queue()
}

# ==========================================
# Mock Catalog Products List
# ==========================================
MOCK_PRODUCTS = [
    {"id": "p1", "name": "High-Performance Laptop", "price": 999.99, "desc": "Intel i7, 16GB RAM, 512GB SSD. Perfect for development.", "icon": "💻"},
    {"id": "p2", "name": "Next-Gen Smartphone", "price": 699.49, "desc": "6.1-inch OLED, 128GB Storage, Dual camera lens system.", "icon": "📱"},
    {"id": "p3", "name": "Wireless ANC Headphones", "price": 199.99, "desc": "Active Noise Cancelling, 30h Battery life, Smart touch.", "icon": "🎧"},
    {"id": "p4", "name": "Mechanical Keyboard", "price": 89.95, "desc": "Tactile Blue Switches, RGB backlit, USB-C connectivity.", "icon": "⌨️"},
    {"id": "p5", "name": "UltraWide IPS Monitor", "price": 299.00, "desc": "34-inch screen, 144Hz refresh rate, 1ms response latency.", "icon": "🖥️"}
]

# ==========================================
# ROUTE: / (Dashboard Index)
# Purpose:
#   Render the main Dark Theme Test Runner control dashboard
# ==========================================
@app.route("/")
def index():
    config = load_json_file("config/config.json")
    
    # List reports (HTML files)
    reports = []
    if os.path.exists(REPORTS_DIR):
        reports = [f for f in os.listdir(REPORTS_DIR) if f.endswith(".html")]
        reports.sort(reverse=True) # Newest first

    # List failure screenshots (PNG files)
    screenshots = []
    if os.path.exists(SCREENSHOTS_DIR):
        screenshots = [f for f in os.listdir(SCREENSHOTS_DIR) if f.endswith(".png")]
        screenshots.sort(reverse=True)

    return render_template(
        "dashboard.html", 
        config=config, 
        reports=reports, 
        screenshots=screenshots
    )

# ==========================================
# ROUTE: /reports/<filename>
# Purpose:
#   Serve test reports locally
# ==========================================
@app.route("/reports/<path:filename>")
def serve_report(filename):
    return send_from_directory(REPORTS_DIR, filename)

# ==========================================
# ROUTE: /screenshots/<filename>
# Purpose:
#   Serve captured screenshots locally
# ==========================================
@app.route("/screenshots/<path:filename>")
def serve_screenshot(filename):
    return send_from_directory(SCREENSHOTS_DIR, filename)

# ==========================================
# ROUTE: /api/assets
# Purpose:
#   Return lists of reports and failure screenshots dynamically
# ==========================================
@app.route("/api/assets")
def get_assets():
    reports = []
    if os.path.exists(REPORTS_DIR):
        reports = [f for f in os.listdir(REPORTS_DIR) if f.endswith(".html")]
        reports.sort(reverse=True)

    screenshots = []
    if os.path.exists(SCREENSHOTS_DIR):
        screenshots = [f for f in os.listdir(SCREENSHOTS_DIR) if f.endswith(".png")]
        screenshots.sort(reverse=True)

    return jsonify({"reports": reports, "screenshots": screenshots})

# ==========================================
# Function Name: run_pytest_subprocess
# Purpose:
#   Worker thread function. Triggers pytest, pipes log lines to queue in real-time
# ==========================================
def run_pytest_subprocess(cmd, q):
    logger.info(f"Subprocess started with command: {' '.join(cmd)}")
    q.put(">>> Initializing Pytest Test Suite Runner...\n")
    
    try:
        # Start pytest subprocess redirecting stderr to stdout
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            cwd=ROOT_DIR
        )
        
        for line in process.stdout:
            stripped = line.rstrip()
            q.put(stripped)
            logger.info(stripped) # Mirror to framework file log
            
        process.wait()
        exit_code = process.returncode
        
        if exit_code == 0:
            status = "success"
            q.put(f"\n>>> Pytest finished. SUCCESS (Code: {exit_code})")
        else:
            status = "failed"
            q.put(f"\n>>> Pytest finished. FAILURES DETECTED (Code: {exit_code})")
            
        execution_state["latest_status"] = status
        q.put(f"=== TESTRUN_FINISHED: {status} ===")
        
    except Exception as e:
        logger.error(f"Error running pytest subprocess: {str(e)}")
        q.put(f"\n>>> CRITICAL RUNNER ERROR: {str(e)}")
        execution_state["latest_status"] = "failed"
        q.put("=== TESTRUN_FINISHED: failed ===")
    finally:
        execution_state["is_running"] = False

# ==========================================
# ROUTE: /api/run-tests (POST)
# Purpose:
#   Trigger background execution of the Pytest framework
# ==========================================
@app.route("/api/run-tests", methods=["POST"])
def run_tests():
    if execution_state["is_running"]:
        return jsonify({"status": "error", "message": "Tests are already running"}), 400

    data = request.json
    # 1. Update config.json with current form settings
    config = load_json_file("config/config.json")
    config["base_url"] = data.get("base_url", "http://127.0.0.1:5000")
    config["username"] = data.get("username", "testuser")
    config["password"] = data.get("password", "Password123!")
    config["browser"] = data.get("browser", "chromium")
    config["timeout"] = int(data.get("timeout", 10000))
    config["headless"] = bool(data.get("headless", True))
    config["extension_path"] = data.get("extension_path", "")
    config["selected_tests"] = data.get("selected_tests", [])
    save_json_file("config/config.json", config)

    # 2. Construct Pytest execution command
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"report_{timestamp}.html"
    cmd = [
        "pytest",
        "-v",
        f"--html=reports/{report_file}",
        "--self-contained-html"
    ]

    selected_tests = config.get("selected_tests", [])
    if selected_tests:
        # Map checkbox names to specific python file paths
        for test in selected_tests:
            test_path = os.path.join("test_cases", f"test_{test}.py")
            if os.path.exists(os.path.join(ROOT_DIR, test_path)):
                cmd.append(test_path)
    else:
        # Run all if none explicitly selected
        cmd.append("test_cases/")

    # 3. Spin worker thread to prevent locking the Flask application
    # Clear old logs from queue
    while not execution_state["log_queue"].empty():
        try:
            execution_state["log_queue"].get_nowait()
        except queue.Empty:
            break

    execution_state["is_running"] = True
    execution_state["latest_status"] = "running"
    
    t = threading.Thread(target=run_pytest_subprocess, args=(cmd, execution_state["log_queue"]))
    t.start()

    return jsonify({"status": "started", "report": report_file})

# ==========================================
# ROUTE: /stream-logs
# Purpose:
#   SSE log stream yielding lines to the Dashboard in real-time
# ==========================================
@app.route("/stream-logs")
def stream_logs():
    def generate():
        # Keep track if runner finished
        while True:
            try:
                # Block briefly for new log lines
                line = execution_state["log_queue"].get(timeout=3.0)
                yield f"data: {line}\n\n"
                
                # Check for completion flag
                if "=== TESTRUN_FINISHED:" in line:
                    break
            except queue.Empty:
                # If tests are not running, close connection
                if not execution_state["is_running"]:
                    break
                # Keep-alive heartbeat
                yield "data: ...\n\n"
    
    return Response(generate(), mimetype="text/event-stream")


# ==========================================
# ==========================================
# MOCK E-COMMERCE WEBSITE TARGET ROUTES
# ==========================================
# ==========================================

# ==========================================
# ROUTE: /mock/login (GET/POST)
# Purpose:
#   Handle credentials checking and mock user log-in state
# ==========================================
@app.route("/mock/login", methods=["GET", "POST"])
def mock_login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        
        # Load credentials from config
        config = load_json_file("config/config.json")
        expected_username = config.get("username", "testuser")
        expected_password = config.get("password", "Password123!")

        if username == expected_username and password == expected_password:
            session["username"] = username
            session["cart"] = [] # Reset cart on fresh login
            return render_template("mock_login.html", success="Login successful! Redirecting to catalog...")
        else:
            return render_template("mock_login.html", error="Invalid username or incorrect password.")
            
    return render_template("mock_login.html")

# ==========================================
# ROUTE: /mock/logout
# Purpose:
#   Reset authentication session details
# ==========================================
@app.route("/mock/logout")
def mock_logout():
    session.pop("username", None)
    session.pop("cart", None)
    return redirect(url_for("mock_login"))

# ==========================================
# ROUTE: /mock/signup (GET/POST)
# Purpose:
#   Provide user signup form with validation logic matching test suites
# ==========================================
@app.route("/mock/signup", methods=["GET", "POST"])
def mock_signup():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()
        confirm_password = request.form.get("confirm_password", "").strip()
        gender = request.form.get("gender", "").strip()
        terms = request.form.get("terms", "") == "true"

        errors = []
        
        # Form field validations
        if not name:
            errors.append("Full Name is required.")
        if not email:
            errors.append("Email Address is required.")
        elif "@" not in email or "." not in email:
            errors.append("Invalid email address format.")
            
        if not password:
            errors.append("Password is required.")
        elif len(password) < 6:
            errors.append("Password must be at least 6 characters.")
            
        if password != confirm_password:
            errors.append("Passwords do not match.")
            
        if not gender:
            errors.append("Gender selection is required.")
            
        if not terms:
            errors.append("You must accept the Terms and Conditions.")

        if errors:
            return render_template("mock_signup.html", errors=errors)
        
        # Simulating successful signup
        return render_template("mock_signup.html", success="Account created successfully!")

    return render_template("mock_signup.html")

# ==========================================
# ROUTE: /mock/catalog
# Purpose:
#   Display mock products with search query filter q
# ==========================================
@app.route("/mock/catalog")
def mock_catalog():
    query = request.args.get("q", "").strip()
    
    if query:
        # Case insensitive regex match for search testing
        filtered_products = [
            p for p in MOCK_PRODUCTS 
            if query.lower() in p["name"].lower() or query.lower() in p["desc"].lower()
        ]
    else:
        filtered_products = MOCK_PRODUCTS
        
    return render_template("mock_catalog.html", products=filtered_products, query=query)

# ==========================================
# ROUTE: /mock/add-to-cart (POST)
# Purpose:
#   Simulate items incrementing in the local cart dictionary
# ==========================================
@app.route("/mock/add-to-cart", methods=["POST"])
def mock_add_to_cart():
    product_id = request.form.get("product_id")
    # Find product details
    product = next((p for p in MOCK_PRODUCTS if p["id"] == product_id), None)
    
    if product:
        if "cart" not in session:
            session["cart"] = []
        # Need to reassign session dictionary/array to trigger updates in Flask session
        cart = session["cart"]
        cart.append(product)
        session["cart"] = cart
        logger.info(f"Mock Site: Added '{product['name']}' to cart. Total items: {len(session['cart'])}")

    return redirect(url_for("mock_catalog"))

# ==========================================
# ROUTE: /mock/remove-from-cart (POST)
# Purpose:
#   Simulate item removal
# ==========================================
@app.route("/mock/remove-from-cart", methods=["POST"])
def mock_remove_from_cart():
    index = int(request.form.get("index", -1))
    if "cart" in session and 0 <= index < len(session["cart"]):
        cart = session["cart"]
        cart.pop(index)
        session["cart"] = cart
        
    return redirect(url_for("mock_cart"))

# ==========================================
# ROUTE: /mock/cart
# Purpose:
#   View current items in the shopping cart
# ==========================================
@app.route("/mock/cart")
def mock_cart():
    cart_items = session.get("cart", [])
    total = sum(item["price"] for item in cart_items)
    return render_template("mock_cart.html", cart_items=cart_items, total=total)

# ==========================================
# ROUTE: /mock/checkout (GET/POST)
# Purpose:
#   Manage shipping forms before entering checkout payment details
# ==========================================
@app.route("/mock/checkout", methods=["GET", "POST"])
def mock_checkout():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        address = request.form.get("address", "").strip()
        city = request.form.get("city", "").strip()
        zip_code = request.form.get("zip_code", "").strip()
        
        if not name or not address or not city or not zip_code:
            return redirect(url_for("mock_checkout")) # Simple redirect reload on error
            
        # Store shipping details in session, progress to payment
        session["shipping_name"] = name
        return redirect(url_for("mock_payment"))

    return render_template("mock_checkout.html")

# ==========================================
# ROUTE: /mock/payment (GET/POST)
# Purpose:
#   Simulate credit card validations and complete mock order transaction
# ==========================================
@app.route("/mock/payment", methods=["GET", "POST"])
def mock_payment():
    cart_items = session.get("cart", [])
    total = sum(item["price"] for item in cart_items)

    if request.method == "POST":
        card_name = request.form.get("card_name", "").strip()
        card_number = request.form.get("card_number", "").strip()
        card_expiry = request.form.get("card_expiry", "").strip()
        card_cvv = request.form.get("card_cvv", "").strip()

        # Regular expressions for validation checks
        is_num = card_number.isdigit() and len(card_number) == 16
        is_exp = bool(re.match(r"^(0[1-9]|1[0-2])\/\d{2}$", card_expiry))
        is_cvv = card_cvv.isdigit() and len(card_cvv) == 3

        if not card_name:
            return render_template("mock_payment.html", total=total, error="Cardholder Name is required.")
        if not is_num:
            return render_template("mock_payment.html", total=total, error="Invalid credit card number. Must be 16 digits.")
        if not is_exp:
            return render_template("mock_payment.html", total=total, error="Invalid expiry date. Must be in MM/YY format.")
        if not is_cvv:
            return render_template("mock_payment.html", total=total, error="Invalid CVV. Must be 3 digits.")

        # Payment successful simulation
        order_id = f"ORD-{uuid.uuid4().hex[:8].upper()}"
        # Empty user cart
        session["cart"] = []
        return render_template("mock_payment.html", success=True, order_id=order_id)

    return render_template("mock_payment.html", total=total)

# ==========================================
# ROUTE: /mock/ui-validation
# Purpose:
#   Render page specifically built for computed CSS styles testing
# ==========================================
@app.route("/mock/ui-validation")
def mock_ui_validation():
    return render_template("mock_ui_validation.html")

# ==========================================
# Execution Boot
# ==========================================
if __name__ == "__main__":
    logger.info("Starting Flask application dashboard services...")
    # Serve locally on port 5000
    app.run(host="127.0.0.1", port=5000, debug=True)
