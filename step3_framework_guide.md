# 🚀 3단계: 실전 프레임워크 구축 (7-10일)

## ✅ 1. pytest 프레임워크 적용

### pytest란?
- Python의 **가장 인기 있는** 테스트 프레임워크
- 간단한 문법, 강력한 기능
- **자동 테스트 발견**, fixture, 리포트 생성 등

### 설치
```bash
pip install pytest
pip install pytest-html  # HTML 리포트
pip install pytest-xdist  # 병렬 실행
```

### 기본 사용법
```python
# tests/test_example.py
def test_addition():
    """간단한 테스트"""
    assert 1 + 1 == 2
    
def test_string():
    """문자열 테스트"""
    assert "hello".upper() == "HELLO"
```

```bash
# 실행
pytest tests/test_example.py -v
```

---

### 실습 19: 첫 번째 Selenium + pytest
```python
# tests/test_kream_basic.py
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def test_kream_opens():
    """KREAM 메인 페이지 오픈 테스트"""
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    
    driver.get("https://kream.co.kr")
    
    # 검증
    assert "KREAM" in driver.title
    assert driver.current_url == "https://kream.co.kr/"
    
    driver.quit()


def test_kream_search():
    """검색 기능 테스트"""
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    
    driver.get("https://kream.co.kr")
    
    # 검증: URL에 kream.co.kr 포함
    assert "kream.co.kr" in driver.current_url
    
    driver.quit()
```

```bash
# 실행
pytest tests/test_kream_basic.py -v
```

---

## ✅ 2. pytest Fixture로 setup/teardown

### Fixture란?
- 테스트 전후에 **자동으로 실행**되는 함수
- 코드 중복 제거
- 리소스 관리 (브라우저 열기/닫기)

### 실습 20: conftest.py 작성
```python
# tests/conftest.py
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture
def driver():
    """WebDriver fixture - 각 테스트마다 새 브라우저"""
    print("\n브라우저 시작...")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    driver.implicitly_wait(10)
    
    yield driver  # 테스트 실행
    
    print("\n브라우저 종료...")
    driver.quit()


@pytest.fixture
def driver_with_kream(driver):
    """KREAM 페이지까지 열어주는 fixture"""
    driver.get("https://kream.co.kr")
    return driver
```

### 사용 예시
```python
# tests/test_with_fixture.py
import pytest
from selenium.webdriver.common.by import By


def test_search_box_exists(driver_with_kream):
    """검색창 존재 확인"""
    search_box = driver_with_kream.find_element(By.CSS_SELECTOR, "input.input_search")
    assert search_box is not None
    assert search_box.is_displayed()


def test_logo_exists(driver_with_kream):
    """로고 존재 확인"""
    logo = driver_with_kream.find_element(By.CSS_SELECTOR, "a.logo")
    assert logo is not None
```

```bash
pytest tests/test_with_fixture.py -v
```

---

### 실습 21: 고급 Fixture
```python
# tests/conftest.py (추가)
import pytest
import os
from datetime import datetime


@pytest.fixture(scope="session")
def screenshot_dir():
    """스크린샷 디렉토리 생성 (전체 세션에 1번만)"""
    dir_name = f"screenshots/{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(dir_name, exist_ok=True)
    return dir_name


@pytest.fixture
def main_page(driver):
    """MainPage 객체 fixture"""
    from pages.main_page import MainPage
    page = MainPage(driver)
    page.open()
    return page


@pytest.fixture(autouse=True)
def log_test_name(request):
    """모든 테스트 전에 자동으로 실행 (테스트 이름 로깅)"""
    print(f"\n▶ 테스트 시작: {request.node.name}")
    yield
    print(f"◀ 테스트 종료: {request.node.name}")
```

---

## ✅ 3. pytest-html로 테스트 리포트 생성

### 실습 22: HTML 리포트 생성
```bash
# 기본 리포트
pytest tests/ --html=reports/report.html --self-contained-html

# verbose 모드
pytest tests/ -v --html=reports/report.html --self-contained-html

# 특정 테스트만
pytest tests/test_search.py -v --html=reports/search_report.html
```

### pytest.ini 설정
```ini
# pytest.ini
[pytest]
# 기본 옵션
addopts = -v --html=reports/report.html --self-contained-html

# 테스트 파일 패턴
python_files = test_*.py
python_classes = Test*
python_functions = test_*

# 경로
testpaths = tests

# 마커 정의
markers =
    smoke: 스모크 테스트
    regression: 회귀 테스트
    search: 검색 관련 테스트
```

### 마커 사용 예시
```python
# tests/test_with_markers.py
import pytest


@pytest.mark.smoke
def test_homepage_loads(driver):
    """홈페이지 로딩 테스트 (스모크)"""
    driver.get("https://kream.co.kr")
    assert "KREAM" in driver.title


@pytest.mark.search
@pytest.mark.regression
def test_search_function(driver):
    """검색 기능 테스트"""
    # 테스트 코드
    pass
```

```bash
# 스모크 테스트만 실행
pytest -m smoke -v

# 검색 테스트만 실행
pytest -m search -v

# 회귀 테스트 제외
pytest -m "not regression" -v
```

---

## ✅ 4. 로깅 시스템 구축

### 실습 23: Logger 유틸리티
```python
# utils/logger.py
import logging
import os
from datetime import datetime


class Logger:
    """로깅 유틸리티"""
    
    @staticmethod
    def get_logger(name="selenium_test"):
        """로거 생성"""
        # 로거 생성
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        
        # 이미 핸들러가 있으면 중복 생성 방지
        if logger.handlers:
            return logger
        
        # 로그 폴더 생성
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # 로그 파일명
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = f"{log_dir}/test_{timestamp}.log"
        
        # 파일 핸들러
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        
        # 콘솔 핸들러
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # 포맷 설정
        formatter = logging.Formatter(
            '[%(asctime)s] [%(levelname)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # 핸들러 추가
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger
```

### BasePage에 로거 추가
```python
# pages/base_page.py (업데이트)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from utils.logger import Logger


class BasePage:
    """모든 페이지 클래스의 부모 클래스"""
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.logger = Logger.get_logger()
    
    def find_element(self, locator):
        """요소 찾기"""
        try:
            self.logger.info(f"요소 찾기: {locator}")
            element = self.wait.until(EC.presence_of_element_located(locator))
            self.logger.info(f"✅ 요소 발견: {locator}")
            return element
        except TimeoutException:
            self.logger.error(f"❌ 요소를 찾지 못함: {locator}")
            raise Exception(f"Element {locator} not found")
    
    def click(self, locator):
        """클릭"""
        self.logger.info(f"클릭 시도: {locator}")
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()
        self.logger.info(f"✅ 클릭 성공: {locator}")
    
    def input_text(self, locator, text):
        """텍스트 입력"""
        self.logger.info(f"텍스트 입력: {locator} -> '{text}'")
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
        self.logger.info(f"✅ 입력 완료: '{text}'")
```

---

## ✅ 5. 실전 테스트 케이스 작성

### 실습 24: 검색 테스트 (완성형)
```python
# tests/test_search.py
import pytest
from pages.main_page import MainPage
from pages.search_page import SearchPage
from utils.logger import Logger


class TestSearch:
    """검색 기능 테스트"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """각 테스트 전에 로거 초기화"""
        self.logger = Logger.get_logger()
    
    @pytest.mark.smoke
    def test_search_with_valid_keyword(self, driver):
        """유효한 키워드로 검색 테스트"""
        self.logger.info("=== 유효한 키워드 검색 테스트 시작 ===")
        
        # 메인 페이지 열기
        main_page = MainPage(driver)
        main_page.open()
        
        # 검색 수행
        keyword = "나이키 덩크"
        main_page.search(keyword)
        
        # 검색 페이지로 이동
        search_page = SearchPage(driver)
        
        # 검증 1: 검색 결과가 있는지
        result_count = search_page.get_search_results_count()
        self.logger.info(f"검색 결과 개수: {result_count}")
        assert result_count > 0, "검색 결과가 없습니다"
        
        # 검증 2: 키워드가 결과에 포함되는지
        assert search_page.is_keyword_in_results("나이키"), "검색 결과에 키워드가 없습니다"
        
        self.logger.info("✅ 테스트 통과")
    
    @pytest.mark.regression
    def test_search_with_no_results(self, driver):
        """결과 없는 검색 테스트"""
        self.logger.info("=== 결과 없는 검색 테스트 시작 ===")
        
        main_page = MainPage(driver)
        main_page.open()
        
        # 존재하지 않을 키워드로 검색
        main_page.search("xyzabc123nonexistent")
        
        search_page = SearchPage(driver)
        result_count = search_page.get_search_results_count()
        
        self.logger.info(f"검색 결과 개수: {result_count}")
        assert result_count == 0, "잘못된 검색 결과"
        
        self.logger.info("✅ 테스트 통과")
    
    @pytest.mark.search
    @pytest.mark.parametrize("keyword", ["조던 1", "에어포스", "덩크"])
    def test_search_multiple_keywords(self, driver, keyword):
        """여러 키워드 검색 테스트 (파라미터화)"""
        self.logger.info(f"=== 키워드 '{keyword}' 검색 테스트 ===")
        
        main_page = MainPage(driver)
        main_page.open()
        main_page.search(keyword)
        
        search_page = SearchPage(driver)
        result_count = search_page.get_search_results_count()
        
        assert result_count > 0, f"'{keyword}' 검색 결과가 없습니다"
        self.logger.info(f"✅ '{keyword}' 검색 성공: {result_count}개 발견")
```

---

### 실습 25: 네비게이션 테스트
```python
# tests/test_navigation.py
import pytest
from pages.main_page import MainPage
from utils.logger import Logger


class TestNavigation:
    """네비게이션 테스트"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        self.logger = Logger.get_logger()
    
    @pytest.mark.smoke
    def test_logo_returns_home(self, driver):
        """로고 클릭 시 홈으로 돌아가는지 테스트"""
        self.logger.info("=== 로고 클릭 테스트 시작 ===")
        
        main_page = MainPage(driver)
        main_page.open()
        
        # 검색해서 다른 페이지로 이동
        main_page.search("덩크")
        self.logger.info(f"검색 후 URL: {driver.current_url}")
        
        # 로고 클릭
        main_page.click_logo()
        self.logger.info(f"로고 클릭 후 URL: {driver.current_url}")
        
        # 홈으로 돌아왔는지 확인
        assert driver.current_url == "https://kream.co.kr/" or \
               driver.current_url == "https://kream.co.kr", \
               "로고 클릭 후 홈으로 돌아가지 않음"
        
        self.logger.info("✅ 테스트 통과")
    
    @pytest.mark.regression
    def test_browser_back_button(self, driver):
        """브라우저 뒤로가기 테스트"""
        self.logger.info("=== 브라우저 뒤로가기 테스트 ===")
        
        main_page = MainPage(driver)
        main_page.open()
        
        initial_url = driver.current_url
        
        # 검색
        main_page.search("조던")
        search_url = driver.current_url
        
        # 뒤로가기
        driver.back()
        
        assert driver.current_url == initial_url, "뒤로가기가 정상 작동하지 않음"
        self.logger.info("✅ 테스트 통과")
```

---

## ✅ 6. 실패 시 스크린샷 자동 저장

### conftest.py 업데이트
```python
# tests/conftest.py (추가)
import pytest
import os
from datetime import datetime


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """테스트 실패 시 스크린샷 저장"""
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call" and report.failed:
        # driver fixture 가져오기
        driver = item.funcargs.get('driver')
        
        if driver:
            # 스크린샷 저장
            screenshot_dir = "reports/screenshots"
            os.makedirs(screenshot_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_name = f"{item.name}_{timestamp}.png"
            screenshot_path = os.path.join(screenshot_dir, screenshot_name)
            
            driver.save_screenshot(screenshot_path)
            print(f"\n📸 스크린샷 저장: {screenshot_path}")
            
            # HTML 리포트에 스크린샷 추가
            extra = getattr(report, 'extra', [])
            if screenshot_path:
                html = f'<div><img src="{screenshot_path}" style="width:600px;"/></div>'
                extra.append(pytest.html.extras.html(html))
            report.extra = extra
```

---

## ✅ 7. CI/CD 연동 준비 (GitHub Actions)

### 실습 26: GitHub Actions 워크플로우
```yaml
# .github/workflows/selenium-tests.yml
name: Selenium Tests

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Install Chrome
      run: |
        sudo apt-get update
        sudo apt-get install -y google-chrome-stable
    
    - name: Run tests
      run: |
        pytest tests/ -v --html=reports/report.html --self-contained-html
    
    - name: Upload test results
      if: always()
      uses: actions/upload-artifact@v3
      with:
        name: test-results
        path: reports/
```

---

## 📝 3단계 완료 체크리스트

- [ ] pytest 설치 및 기본 테스트 실행
- [ ] conftest.py로 fixture 구현
- [ ] pytest-html로 리포트 생성
- [ ] 로깅 시스템 구축
- [ ] 5개 이상의 실제 테스트 케이스 작성
- [ ] 테스트 실패 시 자동 스크린샷
- [ ] pytest.ini 설정 완료
- [ ] GitHub Actions 워크플로우 작성 (선택)

---

## 📂 최종 프로젝트 구조

```
kream-selenium-automation/
│
├── pages/
│   ├── __init__.py
│   ├── base_page.py
│   ├── main_page.py
│   └── search_page.py
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_search.py
│   └── test_navigation.py
│
├── utils/
│   ├── __init__.py
│   ├── logger.py
│   └── screenshot.py
│
├── config/
│   ├── config.py
│   └── test_data.json
│
├── reports/
│   ├── screenshots/
│   └── report.html
│
├── logs/
│   └── test_20240101_120000.log
│
├── .github/
│   └── workflows/
│       └── selenium-tests.yml
│
├── requirements.txt
├── pytest.ini
└── README.md
```

---

## 💡 README.md 작성 가이드

```markdown
# KREAM Selenium 자동화 테스트

## 프로젝트 소개
KREAM 웹사이트의 주요 기능을 테스트하는 Selenium 자동화 프레임워크입니다.

## 기술 스택
- Python 3.9+
- Selenium 4.x
- pytest
- Page Object Model (POM)

## 설치 및 실행

### 1. 의존성 설치
```bash
pip install -r requirements.txt
```

### 2. 테스트 실행
```bash
# 전체 테스트
pytest tests/ -v

# 스모크 테스트만
pytest -m smoke -v

# HTML 리포트 생성
pytest tests/ --html=reports/report.html
```

## 테스트 케이스
- ✅ 검색 기능 테스트
- ✅ 네비게이션 테스트
- ✅ 상품 상세 페이지 테스트

## 발견된 이슈
1. 검색 결과 로딩 시 스켈레톤 UI 부재
2. 모바일 뷰에서 햄버거 메뉴 응답 지연

## 작성자
맥스 - QA Engineer
```

---

## 🎯 포트폴리오 완성 팁

### 1. GitHub에 업로드
```bash
git init
git add .
git commit -m "Initial commit: KREAM Selenium 자동화"
git branch -M main
git remote add origin https://github.com/your-username/kream-selenium.git
git push -u origin main
```

### 2. README에 추가할 내용
- 프로젝트 배경 및 목적
- 발견한 버그/개선점
- 테스트 커버리지
- 스크린샷/GIF
- 실행 결과 예시

### 3. 차별화 포인트
- ✅ **실제 버그 발견** 문서화
- ✅ **UX 개선 제안** 포함
- ✅ **테스트 리포트** 첨부
- ✅ **CI/CD** 구축

---

## 🚀 축하합니다!

3단계까지 완료하셨다면 **실무에서 바로 사용 가능한** Selenium 프레임워크를 구축하신 겁니다!

이제 이력서에 당당히 쓸 수 있어요:
- ✅ Selenium + Python 자동화 프레임워크 구축
- ✅ Page Object Model 패턴 적용
- ✅ pytest 기반 테스트 코드 작성
- ✅ CI/CD 파이프라인 구축

**면접 때 보여줄 포트폴리오 완성!** 🎉
