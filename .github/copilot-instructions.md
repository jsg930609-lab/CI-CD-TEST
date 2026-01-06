# Copilot instructions for kream-selenium-automation

Short, actionable guidance so an AI coding assistant can be productive immediately.

- **Project purpose:** UI test automation for the Kream site using Selenium + pytest. Tests live under `tests/`, page objects under `pages/`, and small example scripts under `practice/`.

- **How tests run (quick):**
  - Activate venv (Windows PowerShell): `.venv\Scripts\Activate.ps1`
  - Install deps: `pip install -r requirements.txt`
  - Run all tests: `pytest -q`
  - Generate HTML report: `pytest --html=reports/html_reports/report.html`

- **Key dependencies:** `selenium`, `pytest`, `pytest-html`, `webdriver-manager` (see `requirements.txt`). `webdriver-manager` is used in `tests/conftest.py` via `ChromeDriverManager()` so no manual chromedriver setup is required.

- **Important fixtures & hooks:**
  - `tests/conftest.py`: provides `driver()` fixture which configures ChromeOptions and yields a Selenium `webdriver.Chrome` instance. Use the `driver` fixture in tests instead of creating drivers manually.
  - `pytest_runtest_makereport` hook in `conftest.py` saves screenshots to `reports/screenshots/{test_name}.png` on failure.

- **Project layout to reference:**
  - `pages/` — Page Object classes (e.g., `base_page.py`, `login_page.py`, `main_page.py`) — prefer adding helpers here when implementing new flows.
  - `utils/` — helpers: `driver_factory.py`, `logger.py`, `screenshot.py`.
  - `tests/` — pytest test modules that import page objects and use the `driver` fixture.
  - `config/` — `config.py` and `test_data.json` store environment settings and test data.

- **Style / conventions observed (use these when editing or adding code):**
  - Page objects encapsulate interactions and are placed in `pages/`.
  - Tests use the `driver` pytest fixture; avoid instantiating new drivers in tests.
  - Use snake_case for functions and methods; class names are PascalCase for Page Objects.
  - Screenshots and HTML reports are written to `reports/screenshots/` and `reports/html_reports/` respectively.

- **When changing or adding tests:**
  - Prefer adding new Page Object methods in `pages/` and call them from `tests/`.
  - Keep test setup minimal — rely on fixtures in `tests/conftest.py`.
  - If you need custom driver options for a particular test, add a new fixture in `conftest.py` and document it there.

- **Debugging tips specific to this repo:**
  - For local debugging, run a single test with `pytest tests/<module>.py::test_name -q` and open the screenshot saved at `reports/screenshots/` on failure.
  - Ensure the virtualenv is activated; missing packages will cause import errors.

- **Integration and IO points:**
  - External: Chrome browser (local), chromedriver managed by `webdriver-manager`.
  - File IO: tests write screenshots and report HTML into the `reports/` tree — treat these as test artifacts.

- **Examples to follow (concrete):**
  - Use the `driver` fixture from `tests/conftest.py` instead of `webdriver.Chrome(...)` in tests.
  - Look at `pages/base_page.py` for standard element-wait and action helpers before re-implementing similar logic.

- **Do NOT assume:**
  - CI-specific secrets, browsers, or remote drivers — repository uses local Chrome by default.

If any section is unclear or you want more examples (e.g., a sample test + page-object pair), say which area to expand and I'll iterate.
