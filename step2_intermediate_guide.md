# 🚀 2단계: Selenium 중급 기술 습득 (5-7일)

## ✅ 1. 대기 전략 (Wait Strategies)

### 왜 대기가 필요한가?
- 웹 페이지는 **비동기적으로 로딩**됨 (AJAX, JavaScript)
- `time.sleep()`은 **비효율적**이고 **불안정**함
- **명시적 대기**가 훨씬 안정적!

### 3가지 대기 방법

#### 1) Implicit Wait (전역 대기)
```python
# practice_08_implicit_wait.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# 모든 find_element에 최대 10초 대기 적용
driver.implicitly_wait(10)

driver.get("https://kream.co.kr")

# 요소가 나타날 때까지 최대 10초 기다림
search_box = driver.find_element(By.CSS_SELECTOR, "input.input_search")
print("✅ 검색창 찾음!")

driver.quit()
```

**주의:** 전역으로 적용되므로 디버깅이 어려움. **비추천!**

---

#### 2) Explicit Wait (명시적 대기) ⭐ 추천
```python
# practice_09_explicit_wait.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()
driver.get("https://kream.co.kr")

# WebDriverWait 객체 생성
wait = WebDriverWait(driver, 10)

# 요소가 나타날 때까지 대기
search_box = wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "input.input_search"))
)
print("✅ 검색창이 DOM에 존재함!")

# 요소가 클릭 가능할 때까지 대기
search_box = wait.until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "input.input_search"))
)
search_box.click()
print("✅ 검색창 클릭 가능!")

driver.quit()
```

---

#### 3) 주요 Expected Conditions
```python
from selenium.webdriver.support import expected_conditions as EC

# 1. 요소가 존재할 때까지
EC.presence_of_element_located((By.ID, "element"))

# 2. 요소가 보일 때까지
EC.visibility_of_element_located((By.CLASS_NAME, "visible"))

# 3. 요소가 클릭 가능할 때까지
EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn"))

# 4. 텍스트가 포함될 때까지
EC.text_to_be_present_in_element((By.ID, "msg"), "성공")

# 5. URL에 특정 문자열이 포함될 때까지
EC.url_contains("search")

# 6. 제목이 특정 값일 때까지
EC.title_is("KREAM")

# 7. 요소가 사라질 때까지
EC.invisibility_of_element_located((By.ID, "loading"))

# 8. 여러 요소가 존재할 때까지
EC.presence_of_all_elements_located((By.CLASS_NAME, "product"))
```

### 실습 10: 검색 결과 대기
```python
# practice_10_wait_search_results.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()
driver.get("https://kream.co.kr")

wait = WebDriverWait(driver, 10)

# 검색창이 클릭 가능할 때까지 대기
search_box = wait.until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "input.input_search"))
)
search_box.send_keys("에어포스")
search_box.send_keys(Keys.ENTER)

# URL에 'search' 문자열이 포함될 때까지 대기
wait.until(EC.url_contains("search"))
print(f"✅ 검색 완료! 현재 URL: {driver.current_url}")

# 검색 결과가 로딩될 때까지 대기
products = wait.until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".product_card"))
)
print(f"✅ {len(products)}개의 상품 발견!")

driver.quit()
```

---

## ✅ 2. 예외 처리 (Exception Handling)

### 주요 예외 종류
```python
from selenium.common.exceptions import (
    NoSuchElementException,      # 요소를 못 찾음
    TimeoutException,            # 대기 시간 초과
    ElementNotInteractableException,  # 요소와 상호작용 불가
    StaleElementReferenceException,   # 요소가 DOM에서 사라짐
    WebDriverException           # 일반적인 WebDriver 에러
)
```

### 실습 11: 안전한 요소 찾기
```python
# practice_11_exception_handling.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()
driver.get("https://kream.co.kr")

wait = WebDriverWait(driver, 5)

# 방법 1: try-except 사용
try:
    search_box = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input.input_search"))
    )
    print("✅ 검색창 발견!")
except TimeoutException:
    print("❌ 검색창을 5초 내에 찾지 못했습니다.")
    driver.save_screenshot("error_search_box.png")
except Exception as e:
    print(f"❌ 예상치 못한 에러: {e}")
finally:
    driver.quit()
```

### 실습 12: 재사용 가능한 유틸 함수
```python
# practice_12_utility_functions.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def safe_find_element(driver, by, value, timeout=10):
    """안전하게 요소 찾기"""
    try:
        wait = WebDriverWait(driver, timeout)
        element = wait.until(EC.presence_of_element_located((by, value)))
        return element
    except TimeoutException:
        print(f"❌ 요소를 찾지 못했습니다: {value}")
        driver.save_screenshot(f"error_{value}.png")
        return None


def safe_click(driver, by, value, timeout=10):
    """안전하게 클릭"""
    try:
        wait = WebDriverWait(driver, timeout)
        element = wait.until(EC.element_to_be_clickable((by, value)))
        element.click()
        return True
    except Exception as e:
        print(f"❌ 클릭 실패: {e}")
        return False


# 사용 예시
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()
driver.get("https://kream.co.kr")

search_box = safe_find_element(driver, By.CSS_SELECTOR, "input.input_search")
if search_box:
    search_box.send_keys("덩크")
    print("✅ 검색어 입력 성공!")

driver.quit()
```

---

## ✅ 3. Page Object Model (POM) 패턴

### POM이란?
- 각 **페이지를 클래스로** 관리
- **로케이터**와 **메서드**를 한 곳에 모음
- **유지보수성** 대폭 향상!

### 프로젝트 구조 생성
```bash
kream-selenium-test/
├── pages/
│   ├── __init__.py
│   ├── base_page.py
│   └── main_page.py
├── tests/
│   └── test_main.py
└── practice_13_pom.py
```

### 실습 13: BasePage 작성
```python
# pages/base_page.py
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class BasePage:
    """모든 페이지 클래스의 부모 클래스"""
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def find_element(self, locator):
        """요소 찾기"""
        try:
            return self.wait.until(EC.presence_of_element_located(locator))
        except TimeoutException:
            raise Exception(f"Element {locator} not found")
    
    def find_elements(self, locator):
        """여러 요소 찾기"""
        try:
            return self.wait.until(EC.presence_of_all_elements_located(locator))
        except TimeoutException:
            return []
    
    def click(self, locator):
        """클릭"""
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()
    
    def input_text(self, locator, text):
        """텍스트 입력"""
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
    
    def get_text(self, locator):
        """텍스트 가져오기"""
        return self.find_element(locator).text
    
    def is_element_visible(self, locator, timeout=5):
        """요소가 보이는지 확인"""
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False
    
    def take_screenshot(self, filename):
        """스크린샷 저장"""
        self.driver.save_screenshot(f"screenshots/{filename}")
```

---

### 실습 14: MainPage 작성
```python
# pages/main_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pages.base_page import BasePage


class MainPage(BasePage):
    """KREAM 메인 페이지"""
    
    # 로케이터 정의
    SEARCH_INPUT = (By.CSS_SELECTOR, "input.input_search")
    LOGO = (By.CSS_SELECTOR, "a.logo")
    NAV_MENU_ITEMS = (By.CSS_SELECTOR, ".gnb_menu a")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "https://kream.co.kr"
    
    def open(self):
        """페이지 열기"""
        self.driver.get(self.url)
    
    def search(self, keyword):
        """상품 검색"""
        self.input_text(self.SEARCH_INPUT, keyword)
        search_box = self.find_element(self.SEARCH_INPUT)
        search_box.send_keys(Keys.ENTER)
    
    def click_logo(self):
        """로고 클릭"""
        self.click(self.LOGO)
    
    def get_nav_menu_items(self):
        """네비게이션 메뉴 아이템 가져오기"""
        return self.find_elements(self.NAV_MENU_ITEMS)
    
    def is_search_box_visible(self):
        """검색창이 보이는지 확인"""
        return self.is_element_visible(self.SEARCH_INPUT)
```

---

### 실습 15: POM 사용 예시
```python
# practice_13_use_pom.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pages.main_page import MainPage
import time

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()

# MainPage 객체 생성
main_page = MainPage(driver)

# 페이지 열기
main_page.open()
time.sleep(2)

# 검색창이 보이는지 확인
if main_page.is_search_box_visible():
    print("✅ 검색창이 보입니다!")
    
    # 검색 수행
    main_page.search("조던 1")
    time.sleep(3)
    
    print(f"현재 URL: {driver.current_url}")
else:
    print("❌ 검색창이 보이지 않습니다!")

driver.quit()
```

---

## ✅ 4. 스크린샷 캡처 기능

### 실습 16: 스크린샷 유틸리티
```python
# utils/screenshot.py
import os
from datetime import datetime


class ScreenshotUtil:
    """스크린샷 유틸리티"""
    
    def __init__(self, driver, screenshot_dir="screenshots"):
        self.driver = driver
        self.screenshot_dir = screenshot_dir
        
        # 폴더가 없으면 생성
        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)
    
    def take_screenshot(self, name=None):
        """스크린샷 저장"""
        if name is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            name = f"screenshot_{timestamp}.png"
        elif not name.endswith('.png'):
            name += '.png'
        
        filepath = os.path.join(self.screenshot_dir, name)
        self.driver.save_screenshot(filepath)
        print(f"✅ 스크린샷 저장: {filepath}")
        return filepath
    
    def take_element_screenshot(self, element, name):
        """특정 요소만 스크린샷"""
        filepath = os.path.join(self.screenshot_dir, name)
        element.screenshot(filepath)
        print(f"✅ 요소 스크린샷 저장: {filepath}")
        return filepath
```

### 사용 예시
```python
# practice_14_screenshot.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from utils.screenshot import ScreenshotUtil
import time

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()
driver.get("https://kream.co.kr")

# 스크린샷 유틸 초기화
screenshot = ScreenshotUtil(driver)

time.sleep(2)

# 전체 페이지 스크린샷
screenshot.take_screenshot("kream_main_page")

# 검색 후 스크린샷
search_box = driver.find_element(By.CSS_SELECTOR, "input.input_search")
search_box.send_keys("덩크")
screenshot.take_screenshot("after_search_input")

driver.quit()
```

---

## ✅ 5. 테스트 데이터 분리

### 실습 17: Config 파일 생성
```python
# config/config.py
class Config:
    """설정 관리"""
    
    # URL
    BASE_URL = "https://kream.co.kr"
    
    # 타임아웃
    DEFAULT_TIMEOUT = 10
    ELEMENT_TIMEOUT = 5
    
    # 브라우저 옵션
    HEADLESS = False
    MAXIMIZE_WINDOW = True
    
    # 스크린샷
    SCREENSHOT_DIR = "screenshots"
    
    # 로그
    LOG_FILE = "logs/test.log"
```

### 실습 18: 테스트 데이터 JSON
```json
// config/test_data.json
{
  "search_keywords": [
    "나이키 덩크",
    "조던 1",
    "에어포스 1",
    "뉴발란스 530"
  ],
  "invalid_keywords": [
    "xyznonexistent123",
    "!@#$%^&*()"
  ],
  "users": {
    "valid_user": {
      "email": "test@example.com",
      "password": "test1234"
    },
    "invalid_user": {
      "email": "wrong@example.com",
      "password": "wrongpass"
    }
  }
}
```

### 데이터 사용 예시
```python
# practice_15_use_test_data.py
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pages.main_page import MainPage
from config.config import Config
import time

# 테스트 데이터 로드
with open('config/test_data.json', 'r', encoding='utf-8') as f:
    test_data = json.load(f)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()

main_page = MainPage(driver)
main_page.open()
time.sleep(2)

# 테스트 데이터 사용
for keyword in test_data['search_keywords'][:2]:
    print(f"검색어: {keyword}")
    main_page.search(keyword)
    time.sleep(3)
    print(f"현재 URL: {driver.current_url}")
    driver.back()
    time.sleep(2)

driver.quit()
```

---

## 📝 2단계 완료 체크리스트

- [ ] WebDriverWait를 사용한 명시적 대기 구현
- [ ] 5가지 이상의 Expected Conditions 사용
- [ ] try-except로 예외 처리 구현
- [ ] BasePage 클래스 작성
- [ ] 2개 이상의 Page 클래스 작성
- [ ] 스크린샷 유틸리티 구현
- [ ] Config와 테스트 데이터 분리

---

## 💡 실무 팁

### POM 작성 시 주의사항
1. **로케이터는 클래스 변수로** 정의 (수정 편의성)
2. **메서드명은 명확하게** (`search()` > `do_search()`)
3. **한 메서드는 한 가지 일만** (단일 책임 원칙)

### 디버깅 체크리스트
```python
# 요소를 못 찾을 때
1. time.sleep(2) 추가해서 페이지 로딩 대기
2. driver.save_screenshot("debug.png")
3. print(driver.current_url)
4. print(driver.page_source)
5. 크롬 개발자도구로 로케이터 재확인
```

---

## 🎯 다음 단계 준비

2단계 완료 후:
- [ ] LoginPage, SearchPage 클래스 추가 작성
- [ ] 유틸리티 함수 5개 이상 작성
- [ ] 실제 테스트 시나리오 3개 작성해보기

**준비되면 3단계(pytest 프레임워크)로!** 🚀
