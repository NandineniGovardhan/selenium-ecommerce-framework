# Ecommerce Selenium Automation Framework

A production-ready, enterprise-grade UI test automation framework for an
Ecommerce web application, built with **Python + Selenium WebDriver + Pytest**
using the **Page Object Model (POM)** and a **data-driven** architecture.

Clone it, install dependencies, and start writing tests immediately.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Folder Structure](#folder-structure)
3. [Framework Design & Architecture](#framework-design--architecture)
4. [Prerequisites](#prerequisites)
5. [Installation](#installation)
6. [Configuration & Environment Switching](#configuration--environment-switching)
7. [Running Tests](#running-tests)
8. [Reports](#reports)
9. [Logging](#logging)
10. [Adding New Test Cases](#adding-new-test-cases)
11. [Adding New Page Objects](#adding-new-page-objects)
12. [Adding New Utilities](#adding-new-utilities)
13. [Git Workflow](#git-workflow)
14. [Troubleshooting](#troubleshooting)
15. [Best Practices & Coding Standards](#best-practices--coding-standards)
16. [Future Enhancements](#future-enhancements)

---

## Project Overview

This framework automates end-to-end UI flows for an Ecommerce application:
login/logout, product search, add/remove cart items, and checkout. It is
designed so a new automation engineer can clone the repo, run
`pip install -r requirements.txt`, and write their first test within minutes
— without needing to touch framework internals.

**Key characteristics:**

- Page Object Model with centralized locators
- Data-driven via external JSON test data (no hardcoded data in tests)
- Environment-aware (QA / DEV / PROD) via a single config switch
- Cross-browser (Chrome, Firefox, Edge) via a single config switch
- Explicit-wait synchronization only — no `time.sleep()`
- Automatic screenshot capture on failure, embedded into the HTML report
- Centralized logging to file + console
- Parallel execution via `pytest-xdist`
- CI-ready (sample GitHub Actions workflow included)

---

## Folder Structure

```
selenium-ecommerce-framework/
├── base/                     # Framework core: driver factory, BasePage, BaseTest
│   ├── base_page.py
│   ├── base_test.py
│   └── driver_factory.py
├── config/                   # Environment & global configuration
│   ├── config.ini
│   ├── qa_config.json
│   ├── dev_config.json
│   ├── prod_config.json
│   └── config_reader.py
├── constants/                 # Static, non-configurable constants
│   └── constants.py
├── pages/                     # Page Objects (POM)
│   ├── locators/               # Centralized locators, one file per page
│   │   ├── login_locators.py
│   │   ├── home_locators.py
│   │   ├── search_locators.py
│   │   ├── product_locators.py
│   │   ├── cart_locators.py
│   │   └── checkout_locators.py
│   ├── login_page.py
│   ├── home_page.py
│   ├── search_page.py
│   ├── product_page.py
│   ├── cart_page.py
│   └── checkout_page.py
├── tests/                     # Test scripts (business flow only)
│   ├── test_login.py
│   ├── test_logout.py
│   ├── test_search_product.py
│   ├── test_add_to_cart.py
│   ├── test_remove_from_cart.py
│   └── test_checkout.py
├── testdata/                  # External, environment-agnostic JSON test data
│   ├── users/users.json
│   ├── products/products.json
│   ├── addresses/addresses.json
│   └── orders/orders.json
├── utilities/                 # Reusable, single-purpose helper classes
│   ├── selenium_actions_utility.py
│   ├── wait_utility.py
│   ├── js_executor_utility.py
│   ├── screenshot_utility.py
│   ├── logger_utility.py
│   ├── file_reader_utility.py
│   ├── json_reader_utility.py
│   ├── config_reader.py        # (re-exported from config/, see below)
│   ├── date_utility.py
│   ├── retry_utility.py
│   ├── assertion_utility.py
│   ├── window_utility.py
│   ├── alert_utility.py
│   ├── dropdown_utility.py
│   ├── mouse_action_utility.py
│   └── keyboard_action_utility.py
├── reports/                   # Generated HTML reports (git-ignored)
├── logs/                      # Generated execution logs (git-ignored)
├── screenshots/                # Generated failure screenshots (git-ignored)
├── drivers/                   # Reserved for local manual driver binaries (git-ignored; normally unused — see Driver Management)
├── resources/                  # Static non-code resources (fonts, sample files, etc.)
├── .github/workflows/          # CI pipeline definition
├── conftest.py                 # Pytest fixtures, CLI options, failure-screenshot hook
├── pytest.ini                  # Pytest configuration (markers, HTML report, discovery)
├── requirements.txt
├── .env.example                 # Template for local secrets (never commit .env itself)
├── .gitignore
├── README.md
└── FRAMEWORK_DOCUMENTATION.md   # Deep-dive design documentation
```

> Note: `config_reader.py` physically lives in `config/` (it reads
> `config.ini` and the environment JSON files that live alongside it) but is
> conceptually one of the framework's core utilities — every layer of the
> framework imports it the same way: `from config.config_reader import config_reader`.

---

## Framework Design & Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         tests/*.py                               │
│   (business flow only: page-object calls + assertions)           │
└───────────────────────────┬───────────────────────────────────────┘
                            │ uses
┌───────────────────────────▼───────────────────────────────────────┐
│                    base/base_test.py (BaseTest)                    │
│         exposes self.driver + get_pages() + self.assertions        │
└───────────────────────────┬───────────────────────────────────────┘
                            │ instantiates
┌───────────────────────────▼───────────────────────────────────────┐
│                          pages/*.py (POM)                           │
│   business-meaningful methods (login(), add_to_cart(), ...)         │
│   locators imported from pages/locators/*.py                        │
└───────────────────────────┬───────────────────────────────────────┘
                            │ extends
┌───────────────────────────▼───────────────────────────────────────┐
│                    base/base_page.py (BasePage)                     │
│   wires up: SeleniumActionsUtility, WaitUtility, JsExecutor,         │
│   DropdownUtility, AlertUtility, WindowUtility, Mouse/Keyboard       │
└───────────────────────────┬───────────────────────────────────────┘
                            │ delegates raw Selenium calls to
┌───────────────────────────▼───────────────────────────────────────┐
│                        utilities/*.py                                │
│   every raw driver.find_element/execute_script call lives HERE      │
└─────────────────────────────────────────────────────────────────────┘

              ┌───────────────────────────────────────┐
              │      base/driver_factory.py            │
              │  creates Chrome/Firefox/Edge driver      │
              │  based on config/config_reader.py         │
              └───────────────────────────────────────┘

              ┌───────────────────────────────────────┐
              │            conftest.py                  │
              │  `driver` fixture (setup/teardown)       │
              │  CLI options: --env --browser --headless │
              │  failure screenshot hook                  │
              └───────────────────────────────────────┘
```

**Design patterns used:**

| Pattern | Where | Why |
|---|---|---|
| Page Object Model | `pages/` | Isolates UI structure from test logic |
| Factory | `base/driver_factory.py` | Encapsulates browser-specific creation logic |
| Singleton | `config/config_reader.py` | One consistent config source, cached |
| Data-Driven | `testdata/*.json` + `JsonReaderUtility` | No hardcoded test data |
| Facade | `base/base_page.py` | Simplifies access to many utilities via one object |
| Dependency Injection | `conftest.py` `driver` fixture | Tests receive a ready driver instead of creating one |

---

## Prerequisites

- **Python**: 3.10 or higher (developed/tested on 3.11–3.12)
- **pip**: latest version recommended
- One of the supported browsers installed locally: Google Chrome, Mozilla
  Firefox, or Microsoft Edge (browser binaries/drivers are auto-managed via
  `webdriver-manager` — you do **not** need to manually download
  chromedriver/geckodriver/msedgedriver)
- Git
- VS Code (recommended) with the **Python** extension

---

## Installation

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd selenium-ecommerce-framework

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up local secrets
cp .env.example .env
# then fill in real values in .env (never commit this file)
```

Open the folder in VS Code (`code .`) and you're ready to write tests.

---

## Configuration & Environment Switching

Environment and browser are controlled from **one file**:
`config/config.ini`.

```ini
[DEFAULT]
environment = qa      ; qa | dev | prod
browser = chrome      ; chrome | firefox | edge
headless = false
```

Every environment's URLs and settings live in their own JSON file:
`config/qa_config.json`, `config/dev_config.json`, `config/prod_config.json`.
**No URL is ever hardcoded** in a page object or test.

### Overriding at runtime (no file edits needed)

```bash
pytest --env=dev --browser=firefox --headless
```

CLI flags always take precedence over `config.ini`.

---

## Running Tests

```bash
# Run the entire suite (uses config.ini defaults)
pytest

# Run a single test file
pytest tests/test_login.py

# Run a single test case
pytest tests/test_login.py::TestLogin::test_successful_login_with_valid_credentials

# Run by marker (see pytest.ini for the full marker list)
pytest -m smoke
pytest -m "regression and cart"

# Run against a specific environment/browser
pytest --env=prod --browser=edge

# Run headless
pytest --headless

# Run in parallel across all available CPU cores
pytest -n auto

# Combine everything
pytest -n auto --headless --env=qa --browser=chrome -m smoke
```

---

## Reports

HTML reports are generated automatically on every run (configured in
`pytest.ini`) at:

```
reports/report.html
```

The report includes pass/fail/skipped counts, execution time per test, and
an embedded screenshot for every failed test (via the `pytest-html` +
failure-screenshot hook in `conftest.py`).

Reports are **git-ignored** — they are a build artifact, not source code.

---

## Logging

Every run creates a timestamped log file under `/logs`
(`logs/execution_<timestamp>.log`) via `utilities/logger_utility.py`.
Log level is controlled in `config/config.ini` (`[LOGGING] log_level`).

```python
from utilities.logger_utility import get_logger
log = get_logger(__name__)

log.info("Navigating to login page")
log.warning("Element took longer than expected to appear")
log.error("Checkout failed with unexpected error")
```

---

## Adding New Test Cases

1. Create a new file under `tests/`, named `test_<feature>.py`.
2. Extend `BaseTest` and use `pytest.mark.usefixtures("driver")`.
3. Use `self.get_pages()` to access page objects and `self.assertions` for
   assertions. Never call Selenium directly from a test.

```python
import pytest
from base.base_test import BaseTest

@pytest.mark.usefixtures("driver")
class TestMyFeature(BaseTest):

    @pytest.mark.regression
    def test_my_new_scenario(self):
        pages = self.get_pages()
        pages.home_page.open()
        # ... business flow ...
        self.assertions.assert_true(True, "example assertion")
```

---

## Adding New Page Objects

1. Add a locators file under `pages/locators/<page>_locators.py`.
2. Add the page class under `pages/<page>_page.py`, extending `BasePage`.
3. Register it as a property inside `base/base_test.py`'s `_PageRegistry`
   so it becomes available via `self.get_pages().<page>_page`.

---

## Adding New Utilities

1. Add a new file under `utilities/`, e.g. `utilities/my_new_utility.py`.
2. Keep it single-purpose (one utility = one responsibility).
3. If it needs to be available on every page object, wire it into
   `base/base_page.py`'s `__init__`.

---

## Git Workflow

- `main` — always green, deployable/CI-passing state
- `develop` — integration branch for in-progress work
- Feature branches: `feature/<short-description>`
- Bugfix branches: `bugfix/<short-description>`

```bash
git checkout -b feature/add-wishlist-tests
git add .
git commit -m "Add wishlist page object and smoke tests"
git push origin feature/add-wishlist-tests
# open a Pull Request into develop
```

Never commit: `.env`, `reports/`, `logs/`, `screenshots/`, driver binaries,
or `__pycache__/` — all are covered by `.gitignore`.

---

## Troubleshooting

| Symptom | Likely Cause | Fix |
|---|---|---|
| `WebDriverException: unable to find binary` | Browser not installed locally | Install the target browser |
| Tests can't find elements | App UI/locators changed | Update the relevant `pages/locators/*.py` file only |
| `FileNotFoundError` for config JSON | Invalid `--env` value | Use one of `qa`, `dev`, `prod` |
| Placeholder `${VAR}` shows up as literal text in logs | `.env` not loaded / var not exported | Ensure `.env` exists and variables are exported to the shell/CI secrets |
| Report shows no embedded screenshots | `pytest-html` not installed | `pip install -r requirements.txt` |
| Tests pass locally but fail in CI | Headless-specific timing/rendering differences | Increase relevant explicit waits; verify with `--headless` locally first |

---

## Best Practices & Coding Standards

- PEP 8 compliant, descriptive naming (`get_order_confirmation_message`,
  not `getMsg`)
- Explicit waits only — never `time.sleep()`
- One utility class = one responsibility (SOLID's Single Responsibility)
- Locators live only in `pages/locators/`
- Test data lives only in `testdata/*.json`
- Secrets are referenced via `${ENV_VAR}` placeholders, never hardcoded
- Type hints on all public method signatures
- Every test is independent and can run in any order or in parallel

---

## Future Enhancements

- API-layer setup/teardown (create test data via API instead of UI where
  possible, to speed up suite execution)
- Visual regression testing integration
- Allure reporting as an alternative to pytest-html
- Dockerized execution with Selenium Grid for true cross-browser parallelism
- BDD layer (pytest-bdd) for stakeholder-readable scenarios
