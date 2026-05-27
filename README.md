# Local Website Automation Testing Framework

A professional, fully self-contained local web automation testing framework built using **Python**, **Playwright**, and **Pytest**. This framework is engineered to run 100% offline, requires no AI API keys or third-party cloud integrations, and is easily migratable to other machines.

It includes:
1. A **Web Control Dashboard** powered by Flask to configure environment details, trigger pytest suite executions, stream logs in real-time, view HTML reports, and browse failed assertion screenshots.
2. A **Mock E-Commerce Application** hosted locally (under `/mock/`) which provides the target pages for offline automation verification (Login, Signup, Catalog Search, Cart Management, Checkout Address details, Payment processing, and CSS computed layout validation).
3. Robust Page Object Model (POM) architecture.
4. Custom CSS computed style validations (`window.getComputedStyle()`) checking element visibilities, overlaps, and layout overflow.

---

## Folder Structure

```text
AutomationTesting/
│
├── main.py                   # App entrypoint (Serves Dashboard & Mock Target Web App)
├── requirements.txt          # Python dependencies
├── README.md                 # Documentation
├── .gitignore                # Git check-in rules
│
├── config/
│   ├── config.json           # Default user automation settings
│   └── environments.json     # Environment presets (mock vs production targets)
│
├── browser/
│   └── browser_setup.py      # Playwright driver startup and extension injections
│
├── pages/
│   ├── base_page.py          # Wrapper routines for clicks, inputs, and style validations
│   ├── login_page.py         # Login POM
│   ├── signup_page.py        # Registration POM
│   ├── product_page.py       # Catalog search & shopping cart POM
│   └── checkout_page.py      # Delivery address & payment POM
│
├── test_cases/
│   ├── conftest.py           # Pytest configurations, POM fixtures, failure hooks
│   ├── test_login.py         # Authentication verification test cases
│   ├── test_signup.py        # Registration validation test cases
│   ├── test_order.py         # Catalog search & cart badge test cases
│   └── test_payment.py       # Delivery checkout, payment gateway, & CSS style test cases
│
├── utils/
│   ├── logger.py             # Global framework logging output utility
│   ├── screenshot.py         # Failure timestamped screenshot capture utility
│   ├── validations.py        # Computed style checking functions (overlap, visibility, disabled)
│   ├── helpers.py            # JSON loading/saving and test data generation
│   └── constants.py          # Selector registries and default timeout durations
│
├── reports/                  # Generated HTML test execution reports
├── logs/                     # Saved run log files (test_execution.log)
└── screenshots/              # Failure screenshots directory
```

---

## Installation & Setup

Ensure you have Python 3.11+ installed. Run the following setup steps locally:

1. **Clone/Copy Project** into your desired directory.
2. **Open Terminal** in the project root directory.
3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Install Playwright Browsers**:
   ```bash
   playwright install
   ```

---

## How to Execute

### Option 1: Interactive Control Dashboard (Recommended)

1. Launch the local web server:
   ```bash
   python main.py
   ```
2. Open your web browser and navigate to:
   [http://127.0.0.1:5000](http://127.0.0.1:5000)
3. Use the sidebar config panel to adjust URL, username, password, target browser, and specific test suite selection.
4. Click **Run Automation Suite**. The live pytest execution output will stream directly in the console log terminal.
5. Review the test reports generated in the **Test Reports** list and view failure screenshots under the **Failed Assertions Gallery**.

### Option 2: Direct Command Line (Pytest CLI)

You can run test cases directly from the terminal. First, start the server (`python main.py`) in the background so the mock target website is active, then run:

* **Run all tests**:
  ```bash
  pytest
  ```
* **Run with HTML reporting**:
  ```bash
  pytest -v --html=reports/report.html --self-contained-html
  ```
* **Run a specific test module**:
  ```bash
  pytest test_cases/test_login.py
  ```
* **Run a specific browser**:
  Change the `"browser"` parameter inside [config.json](file:///d:/project/Finel_year/AutomationTesting/config/config.json) before running.

---

## Key Framework Features

### 1. CSS / UI validations using `getComputedStyle`
In [validations.py](file:///d:/project/Finel_year/AutomationTesting/utils/validations.py), we check elements properties:
- **Visibility**: Checks if display is `none`, visibility is `hidden`, opacity is `0`, or bounding rect size is zero.
- **Disabled State**: Inspects both `disabled` attribute and styles like `cursor: not-allowed` or `pointer-events: none`.
- **Overlapping Elements**: Evaluates bounding client rect intersections to verify overlapping elements.
- **Layout Overflow**: Compares container and child bounding dimensions to detect responsive breaks.

### 2. Failure screenshot capture & pytest-html attachments
In [conftest.py](file:///d:/project/Finel_year/AutomationTesting/test_cases/conftest.py), the `pytest_runtest_makereport` hook catches assertion failures, captures a screenshot via Playwright, saves it to `screenshots/`, and embeds a link of the thumbnail directly inside the HTML report page.

### 3. Log centralization
Logs are written to both standard stdout console stream and [logs/test_execution.log](file:///d:/project/Finel_year/AutomationTesting/logs/test_execution.log) with formatted timestamps and calling line numbers.

---

## Troubleshooting

- **Subprocess failures**: Make sure you ran `playwright install` to set up Chromium, Firefox, and WebKit on your computer.
- **Port 5000 in use**: If port 5000 is occupied, update `app.run(port=5000)` inside [main.py](file:///d:/project/Finel_year/AutomationTesting/main.py) and change `"base_url"` inside [config.json](file:///d:/project/Finel_year/AutomationTesting/config/config.json).
- **Extension fails to load**: Custom extensions only load on Chromium when running in headed mode (`"headless": false`).
