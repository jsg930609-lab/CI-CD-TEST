# 🚀 1단계: Selenium 기초 다지기 (3-5일)

## ✅ 1. Selenium 설치 및 환경 설정

### 1-1. Python 가상환경 생성 (선택사항이지만 강력 추천)
```bash
# 프로젝트 폴더 생성
mkdir kream-selenium-test
cd kream-selenium-test

# 가상환경 생성
python -m venv venv

# 가상환경 활성화
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### 1-2. Selenium 설치
```bash
pip install selenium
pip install webdriver-manager  # ChromeDriver 자동 관리
```

### 1-3. 설치 확인
```python
# test_installation.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

print("Selenium 설치 확인 중...")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
print("✅ 설치 성공!")
driver.quit()
```

```bash
python test_installation.py
```

---

## ✅ 2. ChromeDriver 다운로드 및 설정

**좋은 소식:** `webdriver-manager`를 사용하면 자동으로 처리됩니다!

### 수동 설정이 필요한 경우:
1. 크롬 버전 확인: `chrome://version`
2. ChromeDriver 다운로드: https://chromedriver.chromium.org/
3. PATH에 추가하거나 코드에서 직접 지정

```python
# 수동 설정 예시 (비추천)
from selenium import webdriver

driver = webdriver.Chrome(executable_path='/path/to/chromedriver')
```

---

## ✅ 3. 첫 번째 스크립트 - 브라우저 열고 닫기

### 실습 1: 네이버 열기
```python
# practice_01_open_browser.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# 드라이버 초기화
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# 브라우저 최대화
driver.maximize_window()

# 네이버 열기
driver.get("https://www.naver.com")

# 5초 대기 (페이지 확인)
time.sleep(5)

# 브라우저 종료
driver.quit()

print("✅ 첫 번째 스크립트 실행 완료!")
```

### 실습 2: KREAM 열기
```python
# practice_02_open_kream.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()

# KREAM 메인 페이지 열기
driver.get("https://kream.co.kr")

# 현재 URL 출력
print(f"현재 URL: {driver.current_url}")

# 페이지 제목 출력
print(f"페이지 제목: {driver.title}")

time.sleep(5)
driver.quit()
```

---

## ✅ 4. 기본 로케이터 학습

### 로케이터란?
웹 페이지에서 **요소를 찾는 방법**입니다.

### 주요 로케이터 8가지
```python
from selenium.webdriver.common.by import By

# 1. ID
element = driver.find_element(By.ID, "search-input")

# 2. NAME
element = driver.find_element(By.NAME, "username")

# 3. CLASS_NAME
element = driver.find_element(By.CLASS_NAME, "btn-primary")

# 4. TAG_NAME
element = driver.find_element(By.TAG_NAME, "button")

# 5. LINK_TEXT (링크 텍스트 전체)
element = driver.find_element(By.LINK_TEXT, "로그인")

# 6. PARTIAL_LINK_TEXT (링크 텍스트 일부)
element = driver.find_element(By.PARTIAL_LINK_TEXT, "로그")

# 7. CSS_SELECTOR ⭐ 가장 많이 사용
element = driver.find_element(By.CSS_SELECTOR, ".search-box input")

# 8. XPATH ⭐ 복잡한 경우 사용
element = driver.find_element(By.XPATH, "//input[@placeholder='검색']")
```

### 실습 3: 로케이터 연습 (크롬 개발자도구 활용)
```python
# practice_03_locators.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()
driver.get("https://kream.co.kr")

time.sleep(2)

# 실습: 검색창 찾기 (F12 눌러서 요소 확인)
try:
    # CSS Selector로 검색창 찾기
    search_box = driver.find_element(By.CSS_SELECTOR, "input[placeholder*='검색']")
    print("✅ 검색창을 찾았습니다!")
    print(f"검색창 placeholder: {search_box.get_attribute('placeholder')}")
except Exception as e:
    print(f"❌ 검색창을 못 찾았습니다: {e}")

time.sleep(2)
driver.quit()
```

### 💡 크롬 개발자도구로 로케이터 찾는 법
1. **F12** 또는 **우클릭 → 검사**
2. **Elements 탭**에서 원하는 요소 선택 (왼쪽 위 화살표 아이콘 클릭)
3. 요소에 **우클릭 → Copy → Copy selector** (CSS Selector)
4. 또는 **Copy XPath** (XPath)

---

## ✅ 5. 웹 요소 찾기 연습 - KREAM 메인 페이지

### 실습 4: KREAM 주요 요소 찾기
```python
# practice_04_find_elements.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()
driver.get("https://kream.co.kr")

time.sleep(3)  # 페이지 로딩 대기

# 1. 로고 찾기
try:
    logo = driver.find_element(By.CSS_SELECTOR, "a.logo")
    print("✅ 로고 발견!")
except:
    print("❌ 로고를 못 찾았습니다")

# 2. 네비게이션 메뉴 찾기
try:
    nav_items = driver.find_elements(By.CSS_SELECTOR, ".gnb_menu a")
    print(f"✅ 메뉴 {len(nav_items)}개 발견!")
    for item in nav_items[:3]:  # 처음 3개만 출력
        print(f"  - {item.text}")
except Exception as e:
    print(f"❌ 메뉴를 못 찾았습니다: {e}")

# 3. 검색창 찾기
try:
    search_input = driver.find_element(By.CSS_SELECTOR, "input.input_search")
    print("✅ 검색창 발견!")
except Exception as e:
    print(f"❌ 검색창을 못 찾았습니다: {e}")

time.sleep(2)
driver.quit()
```

**연습 과제:**
- KREAM 메인 페이지에서 다음 요소들을 찾아보세요:
  - [ ] 로그인 버튼
  - [ ] 상품 카드 (여러 개)
  - [ ] 푸터의 회사 정보

---

## ✅ 6. 기본 액션 익히기 (클릭, 입력, 스크롤)

### 실습 5: 검색 기능 테스트
```python
# practice_05_basic_actions.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()
driver.get("https://kream.co.kr")

time.sleep(2)

# 1. 검색창 클릭 및 텍스트 입력
try:
    search_box = driver.find_element(By.CSS_SELECTOR, "input.input_search")
    
    # 클릭
    search_box.click()
    print("✅ 검색창 클릭")
    
    # 텍스트 입력
    search_box.send_keys("나이키 덩크")
    print("✅ '나이키 덩크' 입력")
    
    time.sleep(1)
    
    # 엔터키 입력
    search_box.send_keys(Keys.ENTER)
    print("✅ 검색 실행")
    
    time.sleep(3)
    
    # 검색 결과 확인
    print(f"현재 URL: {driver.current_url}")
    
except Exception as e:
    print(f"❌ 오류 발생: {e}")

driver.quit()
```

### 실습 6: 스크롤 연습
```python
# practice_06_scroll.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()
driver.get("https://kream.co.kr")

time.sleep(2)

# 1. 페이지 아래로 스크롤
driver.execute_script("window.scrollTo(0, 1000);")
print("✅ 1000px 아래로 스크롤")
time.sleep(2)

# 2. 페이지 맨 아래로 스크롤
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
print("✅ 페이지 맨 아래로 스크롤")
time.sleep(2)

# 3. 페이지 맨 위로 스크롤
driver.execute_script("window.scrollTo(0, 0);")
print("✅ 페이지 맨 위로 스크롤")
time.sleep(2)

driver.quit()
```

### 실습 7: 종합 연습
```python
# practice_07_comprehensive.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()
driver.get("https://kream.co.kr")

time.sleep(2)

# 시나리오: 상품 검색 → 첫 번째 상품 클릭 → 정보 확인
try:
    # 1. 검색
    search_box = driver.find_element(By.CSS_SELECTOR, "input.input_search")
    search_box.send_keys("조던 1")
    search_box.send_keys(Keys.ENTER)
    print("✅ 검색 완료")
    
    time.sleep(3)
    
    # 2. 첫 번째 상품 클릭
    first_product = driver.find_element(By.CSS_SELECTOR, ".product_card a")
    product_name = first_product.find_element(By.CSS_SELECTOR, ".name").text
    print(f"✅ 클릭할 상품: {product_name}")
    
    first_product.click()
    time.sleep(3)
    
    # 3. 상품 상세 정보 확인
    print(f"현재 URL: {driver.current_url}")
    print(f"페이지 제목: {driver.title}")
    
except Exception as e:
    print(f"❌ 오류: {e}")

time.sleep(2)
driver.quit()
```

---

## 📝 1단계 완료 체크리스트

완료하면 체크하세요:

- [ ] Selenium 설치 및 첫 스크립트 실행
- [ ] ChromeDriver 설정 확인
- [ ] 8가지 로케이터 종류 이해
- [ ] 크롬 개발자도구로 로케이터 찾기 연습
- [ ] KREAM 메인 페이지에서 5개 이상 요소 찾기
- [ ] 검색 기능 자동화 성공
- [ ] 스크롤 제어 연습 완료

---

## 💡 실무 팁

### 자주 하는 실수
1. **driver.quit() 빼먹기** → 브라우저가 계속 열려있음
2. **time.sleep() 너무 짧게** → 요소를 못 찾음
3. **로케이터 잘못 복사** → NoSuchElementException 발생

### 디버깅 팁
```python
# 요소를 못 찾을 때
try:
    element = driver.find_element(By.CSS_SELECTOR, ".some-class")
except Exception as e:
    print(f"에러: {e}")
    driver.save_screenshot("error.png")  # 스크린샷 저장
    print(f"현재 URL: {driver.current_url}")
    print(f"페이지 소스: {driver.page_source[:500]}")  # 처음 500자만
```

---

## 🎯 다음 단계 준비

1단계를 완료했다면:
- [ ] 각 실습 코드를 **직접 타이핑**해서 실행해보기
- [ ] KREAM 외에 **네이버, 쿠팡 등**에서도 연습
- [ ] 로케이터 찾는 속도 높이기 (개발자도구 숙달)

**준비되면 2단계로 넘어가세요!** 🚀
