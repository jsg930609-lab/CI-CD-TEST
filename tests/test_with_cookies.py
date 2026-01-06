"""
쿠키를 사용한 자동 로그인 테스트 (수정 버전)
kream_cookies.pkl 파일이 필요합니다!
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pickle
import time
import os

# 쿠키 파일 확인
if not os.path.exists("kream_cookies.pkl"):
    print("❌ kream_cookies.pkl 파일이 없습니다!")
    print("   먼저 save_cookies.py를 실행해서 쿠키를 저장하세요.")
    exit()

# Chrome 옵션 설정
options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

# 비밀번호 저장 팝업 비활성화
prefs = {
    "credentials_enable_service": False,
    "profile.password_manager_enabled": False
}
options.add_experimental_option("prefs", prefs)

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
wait = WebDriverWait(driver, 10)

try:
    print("="*60)
    print("🍪 쿠키 자동 로그인 테스트 (수정 버전)")
    print("="*60)
    
    # 중요! 쿠키를 추가하기 전에 먼저 도메인에 접속해야 함
    print("\n1️⃣ KREAM 도메인 접속 중...")
    driver.get("https://kream.co.kr")
    time.sleep(2)
    
    # 2. 쿠키 로드 및 추가
    print("2️⃣ 쿠키 로드 중...")
    with open("kream_cookies.pkl", "rb") as f:
        cookies = pickle.load(f)
    
    print(f"   총 {len(cookies)}개의 쿠키 발견")
    
    # 쿠키 추가
    added_count = 0
    for cookie in cookies:
        try:
            # sameSite 속성 처리
            if 'sameSite' not in cookie:
                cookie['sameSite'] = 'Lax'
            
            # expiry 제거 (문제 발생 가능)
            if 'expiry' in cookie:
                del cookie['expiry']
            
            driver.add_cookie(cookie)
            added_count += 1
        except Exception as e:
            # 실패한 쿠키는 무시
            pass
    
    print(f"✅ {added_count}개의 쿠키 추가 완료!")
    
    # 3. 페이지 새로고침 (쿠키 적용)
    print("3️⃣ 페이지 새로고침으로 쿠키 적용...")
    driver.refresh()
    time.sleep(3)  # 조금 더 대기
    
    # 4. 로그인 상태 확인
    print("4️⃣ 로그인 상태 확인 중...")
    
    # 방법 1: 마이페이지 링크 확인
    try:
        my_link = driver.find_element(By.CSS_SELECTOR, "a[href*='/my']")
        print("✅ 로그인 성공! (마이페이지 링크 확인) 🎉")
        logged_in = True
    except:
        logged_in = False
    
    # 방법 2: 로그인 버튼 존재 확인 (로그아웃 상태면 있음)
    if not logged_in:
        try:
            login_btn = driver.find_element(By.CSS_SELECTOR, "a[href*='/login']")
            print("⚠️ 로그인 실패 - 로그인 버튼이 보입니다.")
            print("   쿠키가 만료되었거나 잘못되었을 수 있습니다.")
        except:
            print("✅ 로그인 성공! 🎉")
            logged_in = True
    
    # 5. 현재 쿠키 확인
    print("\n5️⃣ 현재 브라우저 쿠키 확인...")
    current_cookies = driver.get_cookies()
    print(f"   현재 {len(current_cookies)}개의 쿠키 활성화됨")
    
    # 중요 쿠키 확인
    important_cookies = ['_kream_session', 'remember_user_token', 'user_id']
    for cookie_name in important_cookies:
        cookie_found = any(c['name'] == cookie_name for c in current_cookies)
        status = "✅" if cookie_found else "❌"
        print(f"   {status} {cookie_name}: {'있음' if cookie_found else '없음'}")
    
    print("\n" + "="*60)
    if logged_in:
        print("✅ 자동 로그인 완료!")
        print("   이제 테스트를 진행할 수 있습니다.")
    else:
        print("⚠️ 로그인 실패")
        print("   save_cookies.py를 다시 실행해서 쿠키를 저장하세요.")
    print("="*60)
    
    input("\n브라우저를 확인하세요. Enter를 누르면 종료합니다...")

except FileNotFoundError:
    print("\n❌ kream_cookies.pkl 파일을 찾을 수 없습니다!")
    print("   먼저 save_cookies.py를 실행하세요.")

except Exception as e:
    print(f"\n❌ 오류 발생: {e}")
    import traceback
    traceback.print_exc()
    driver.save_screenshot("error.png")
    print("📸 스크린샷 저장: error.png")

finally:
    driver.quit()
    print("\n✅ 브라우저 종료")