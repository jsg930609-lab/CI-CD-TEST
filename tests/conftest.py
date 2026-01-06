"""
pytest fixture with cookie-based auto-login
"""
import sys
import pytest
import os
import pickle
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from datetime import datetime


@pytest.fixture
def driver():
    """WebDriver fixture - CI/CD 환경 대응"""
    
    # Chrome 옵션 설정
    options = Options()
    
    # CI 환경에서는 headless 모드
    if os.getenv('CI'):
        options.add_argument('--headless=new')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
    
    # 봇 감지 우회
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    
    # 비밀번호 저장 팝업 비활성화
    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False
    }
    options.add_experimental_option("prefs", prefs)
    
    # 드라이버 초기화
    driver = webdriver.Chrome(options=options)
    
    # navigator.webdriver 제거
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
        'source': '''
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
        '''
    })
    
    driver.maximize_window()
    driver.implicitly_wait(10)
    
    print(f"\n브라우저 시작 (Headless: {os.getenv('CI') is not None})")
    
    yield driver
    
    print("\n브라우저 종료")
    driver.quit()


@pytest.fixture
def logged_in_driver(driver):
    """쿠키를 사용한 자동 로그인 fixture"""
    
    cookie_file = "kream_cookies.pkl"
    
    # 쿠키 파일이 없으면 로그인 없이 진행
    if not os.path.exists(cookie_file):
        print(f"\n⚠️ {cookie_file} 파일이 없습니다. 로그인 없이 진행합니다.")
        driver.get("https://kream.co.kr")
        return driver
    
    # KREAM 접속
    driver.get("https://kream.co.kr")
    
    # 쿠키 로드 및 추가
    try:
        with open(cookie_file, "rb") as f:
            cookies = pickle.load(f)
        
        added_count = 0
        for cookie in cookies:
            try:
                if 'sameSite' not in cookie:
                    cookie['sameSite'] = 'Lax'
                if 'expiry' in cookie:
                    del cookie['expiry']
                
                driver.add_cookie(cookie)
                added_count += 1
            except:
                pass
        
        print(f"\n✅ {added_count}개의 쿠키 로드 완료")
        
        # 페이지 새로고침으로 쿠키 적용
        driver.refresh()
        
    except Exception as e:
        print(f"\n⚠️ 쿠키 로드 실패: {e}")
    
    return driver


@pytest.fixture(scope="session")
def screenshot_dir():
    """스크린샷 디렉토리 생성"""
    dir_name = "reports/screenshots"
    os.makedirs(dir_name, exist_ok=True)
    return dir_name


@pytest.fixture(scope="session")
def reports_dir():
    """리포트 디렉토리 생성"""
    dir_name = "reports"
    os.makedirs(dir_name, exist_ok=True)
    return dir_name


@pytest.fixture(scope="session")
def logs_dir():
    """로그 디렉토리 생성"""
    dir_name = "logs"
    os.makedirs(dir_name, exist_ok=True)
    return dir_name


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """테스트 실패 시 스크린샷 저장"""
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call" and report.failed:
        driver = item.funcargs.get('driver') or item.funcargs.get('logged_in_driver')
        
        if driver:
            # 스크린샷 저장
            screenshot_dir = "reports/screenshots"
            os.makedirs(screenshot_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_name = f"{item.name}_{timestamp}.png"
            screenshot_path = os.path.join(screenshot_dir, screenshot_name)
            
            driver.save_screenshot(screenshot_path)
            print(f"\n📸 스크린샷 저장: {screenshot_path}")
            print(f"📍 현재 URL: {driver.current_url}")


@pytest.fixture(autouse=True)
def test_info(request):
    """각 테스트 전후에 정보 출력"""
    print(f"\n{'='*60}")
    print(f"▶ 테스트 시작: {request.node.name}")
    print(f"{'='*60}")
    
    yield
    
    print(f"\n{'='*60}")
    print(f"◀ 테스트 종료: {request.node.name}")
    print(f"{'='*60}")


def pytest_configure(config):
    """pytest 설정 - 마커 등록"""
    config.addinivalue_line("markers", "smoke: 스모크 테스트")
    config.addinivalue_line("markers", "regression: 회귀 테스트")
    config.addinivalue_line("markers", "search: 검색 기능 테스트")
    config.addinivalue_line("markers", "login_required: 로그인 필요 테스트")