# Framework Documentation (Deep Dive)

This document explains **why** every folder and class exists, how data
flows through the framework, and how each subsystem works internally.
Read this if you're onboarding onto the framework or need to extend it
safely.

---

## 1. Why Each Folder Exists

| Folder | Responsibility | Why it's separate |
|---|---|---|
| `base/` | Framework core (driver creation, BasePage, BaseTest) | These classes are infrastructure, not test logic — separating them keeps `tests/` and `pages/` free of plumbing code |
| `config/` | Environment + global settings | A single, obvious place to change environment/browser without touching code |
| `constants/` | Static values that never change per environment | Prevents magic strings/numbers scattered across the codebase |
| `pages/` | Page Objects (UI structure + interactions) | Isolates "how the UI works" from "what the test verifies" |
| `pages/locators/` | Element locators only | If the UI changes, only ONE file per page needs updating |
| `tests/` | Test scripts (business flow + assertions) | Keeps test intent readable; no Selenium noise |
| `testdata/` | JSON test data | Enables data-driven testing without touching code |
| `utilities/` | Reusable, single-purpose helper classes | Eliminates duplicate Selenium code across pages |
| `reports/` | Generated HTML reports | Build artifact — regenerated every run, never committed |
| `logs/` | Generated execution logs | Build artifact — regenerated every run, never committed |
| `screenshots/` | Failure screenshots | Build artifact — regenerated every run, never committed |
| `resources/` | Static non-code assets (e.g. sample upload files) | Keeps binary/static assets out of code folders |
| `drivers/` | Reserved, normally empty | Browser drivers are auto-managed by `webdriver-manager`; this folder exists only as a documented fallback location for engineers who must pin a manual driver binary locally |

---

## 2. Why Each Core Class Exists

### `config/config_reader.py` — `ConfigReader`
Single source of truth for **all** configuration. Without it, every module
would need to know how to parse `config.ini` and pick the right JSON file
— that logic would be duplicated everywhere. It's implemented as a
thread-safe singleton so the underlying files are parsed exactly once per
test run, with CLI overrides layered on top.

### `base/driver_factory.py` — `DriverFactory`
The only class that knows how to construct a Chrome/Firefox/Edge
`WebDriver`. Kept separate from `BaseTest` so that browser-creation logic
(options, headless flags, driver-manager calls) doesn't bloat test
lifecycle code, and so it can be reused anywhere a raw driver is needed
(e.g. a future API+UI hybrid test).

### `base/base_page.py` — `BasePage`
The parent of every Page Object. It wires up one instance each of every
interaction utility (`SeleniumActionsUtility`, `WaitUtility`,
`JavaScriptExecutorUtility`, `DropdownUtility`, `AlertUtility`,
`WindowUtility`, `MouseActionUtility`, `KeyboardActionUtility`) so page
classes never need to import or instantiate them individually. It also
provides generic navigation helpers (`navigate_to`, `refresh_page`,
`go_back`) shared by literally every page.

### `base/base_test.py` — `BaseTest`
The parent of every test class. It does NOT create or destroy the driver
itself (that's the `driver` pytest fixture's job — see below); instead it
exposes `self.get_pages()`, which lazily instantiates and caches every
Page Object against the current test's driver, and `self.assertions`, a
shorthand to `AssertionUtility`.

### `conftest.py`
The only file that:
- Registers custom CLI options (`--env`, `--browser`, `--headless`)
- Applies those options to `ConfigReader` before any test runs
  (`pytest_configure`)
- Defines the `driver` fixture: creates a fresh WebDriver per test
  function, attaches it to the test instance (`request.instance.driver`),
  yields it, and guarantees `driver.quit()` afterward — even on failure
- Implements the `pytest_runtest_makereport` hook, which fires after every
  test call and captures + embeds a screenshot automatically if (and only
  if) the test failed

---

## 3. How Data Flows Through the Framework

```
testdata/*.json
      │  read by
      ▼
JsonReaderUtility.find_record(...)   ──►  returns a dict (user/product/etc.)
      │
      ▼
tests/test_*.py                      ──►  passes dict fields into page methods
      │
      ▼
pages/*_page.py (Page Object)         ──►  calls self.actions.type_text(locator, value)
      │
      ▼
utilities/selenium_actions_utility.py ──►  calls self.wait.wait_for_visible(locator)
      │                                        then element.send_keys(value)
      ▼
utilities/wait_utility.py             ──►  WebDriverWait(...).until(EC.visibility_of_element_located)
      │
      ▼
Selenium WebDriver ──► Browser ──► Application Under Test
```

Test data never touches the browser directly — it always flows through a
Page Object method, which in turn always flows through
`SeleniumActionsUtility`.

---

## 4. How Browser Initialization Works

1. `conftest.py`'s `driver` fixture runs before each test function.
2. It calls `DriverFactory.create_driver()`.
3. `DriverFactory` asks `ConfigReader.get_browser()` which browser to use
   (respecting any `--browser` CLI override applied in
   `pytest_configure`).
4. Based on the browser name, it builds the matching `Options` object
   (headless flag, window size, notification/infobar suppression) and
   uses the matching `webdriver-manager` class
   (`ChromeDriverManager`, `GeckoDriverManager`,
   `EdgeChromiumDriverManager`) to fetch/cache the correct driver binary
   automatically — no manual downloads, nothing committed to Git.
5. The driver is configured with implicit wait, page load timeout, and
   maximized, then returned.
6. The fixture attaches it to `request.instance.driver` so `BaseTest`'s
   `get_pages()` can use it, and yields control to the test.
7. After the test completes (pass or fail), the fixture calls
   `driver.quit()` in its teardown section — this always runs because
   it's placed after `yield`.

---

## 5. How Fixtures Work

- **`driver` fixture** (`conftest.py`, function-scoped): one fresh browser
  per test function — this keeps tests fully independent, which is a
  hard requirement for reliable parallel execution (`pytest -n auto`).
- Every test class is decorated with `@pytest.mark.usefixtures("driver")`,
  which triggers the fixture without needing an explicit `driver`
  parameter in every test method (since the driver is accessed via
  `self.driver` / `self.get_pages()` instead).
- Because the fixture is function-scoped and independent per test, tests
  can safely run in any order and in parallel workers without state
  leaking between them.

---

## 6. How Reports Are Generated

- `pytest.ini`'s `addopts` always runs pytest with
  `--html=reports/report.html --self-contained-html`.
- `pytest-html` automatically records pass/fail/skip status, duration, and
  captured output for every test.
- `conftest.py`'s `pytest_runtest_makereport` hook adds one extra piece:
  when a test fails, it captures a screenshot via `ScreenshotUtility` and
  attaches it as an inline image (`pytest_html.extras.image(...)`) so the
  failure is visible directly inside the HTML report, without needing to
  open a separate screenshots folder.

---

## 7. How Logging Works

- `utilities/logger_utility.get_logger(__name__)` is the only way any
  module should obtain a logger.
- The first call in a test run triggers `_initialize_root_logger()`,
  which configures exactly one `RotatingFileHandler` (writing to
  `logs/execution_<timestamp>.log`) and one console `StreamHandler`,
  both using the same formatter: `timestamp | LEVEL | module | message`.
- Because configuration happens once on the root logger, every
  module-level logger obtained afterward automatically inherits the same
  handlers — no duplicate log lines, no per-module reconfiguration.
- Log level is controlled centrally via `config/config.ini`
  (`[LOGGING] log_level`), supporting `DEBUG`, `INFO`, `WARNING`, `ERROR`.

---

## 8. How Screenshots Work

- `utilities/screenshot_utility.ScreenshotUtility.capture(driver, test_name)`
  saves a PNG under `/screenshots`, named
  `<sanitized_test_name>_<timestamp>.png`.
- It's called automatically (and only) on test failure, from
  `conftest.py`'s `pytest_runtest_makereport` hook — no engineer needs to
  remember to add screenshot code to their tests.
- It can also be called manually from anywhere a `driver` is available,
  e.g. for debugging an in-progress test.

---

## 9. How Configuration Switching Works

- `config/config.ini` holds the **default** environment and browser.
- `config/<env>_config.json` holds environment-specific values (base URL,
  API URL, DB connection info) — one file per environment, loaded lazily
  and cached by `ConfigReader`.
- CLI flags (`--env`, `--browser`, `--headless`) always override the
  `config.ini` defaults for that run, applied once in
  `conftest.py::pytest_configure`, before any fixture or test executes.
- No code anywhere else needs to know how environment switching works —
  every consumer just calls `config_reader.get_base_url()`,
  `config_reader.get_browser()`, etc.

---

## 10. How Test Execution Happens (End-to-End)

1. Engineer runs `pytest --env=qa --browser=chrome -m smoke`.
2. `pytest_addoption` registers the custom flags;
   `pytest_configure` applies them to `ConfigReader` and exports them as
   environment variables for cross-process consistency (useful with
   `pytest-xdist`).
3. Pytest collects all `test_*.py` files under `tests/` matching the
   `smoke` marker.
4. For each collected test: the `driver` fixture builds a fresh browser,
   attaches it to the test instance, and the test method runs using
   `self.get_pages()` to drive Page Object methods.
5. Assertions run through `AssertionUtility`, which logs pass/fail clearly.
6. On completion (pass/fail/error), the fixture's teardown quits the
   driver; the failure-screenshot hook fires if needed.
7. `pytest-html` writes the consolidated report to `reports/report.html`.

---

## 11. How Page Objects Interact With Test Scripts

Test scripts never talk to Selenium. They only ever call:

```python
pages = self.get_pages()
pages.<page_name>.<business_method>(...)
self.assertions.assert_true(...)
```

Each Page Object method (e.g. `LoginPage.login(username, password)`)
internally composes one or more lower-level `SeleniumActionsUtility`
calls, keeping the test script focused purely on *what* is being
verified, not *how* the UI is manipulated.

---

## 12. How Reusable Methods Reduce Duplicate Code

- Every raw Selenium call (`find_element`, `send_keys`, `.click()`) exists
  in exactly one place: `utilities/selenium_actions_utility.py` (or a
  sibling utility for waits/dropdowns/alerts/etc.).
- Every Page Object composes calls to those utilities rather than
  reimplementing waits or click-fallback logic.
- Every test composes calls to Page Object business methods rather than
  reimplementing UI interaction sequences.
- Assertions are centralized in `AssertionUtility` so failure messages are
  consistently formatted and consistently logged.

This three-layer composition (`utilities` → `pages` → `tests`) is what
keeps the framework's line count low relative to its test coverage, and
is the primary mechanism satisfying the "no duplicate code" requirement.

---

## 13. Best Practices Followed

- **Explicit waits only** — `WaitUtility` wraps every synchronization
  point; no `time.sleep()` exists anywhere in the framework.
- **Centralized locators** — one locators file per page, imported by
  exactly one page object.
- **No hardcoded values** — URLs come from environment JSON, credentials
  come from `${ENV_VAR}` placeholders resolved by `JsonReaderUtility`.
- **Single Responsibility** — each utility class does exactly one job
  (waits vs. actions vs. dropdowns vs. alerts, etc.).
- **DRY** — see section 12.
- **Independent, parallel-safe tests** — function-scoped `driver` fixture
  guarantees no shared browser state between tests.
- **PEP 8 + type hints** — applied consistently across all modules.
