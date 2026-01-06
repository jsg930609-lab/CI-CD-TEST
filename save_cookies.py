"""
첫 로그인 후 쿠키 저장
한 번만 실행하면 됩니다!
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pickle
import time

# Chrome 옵션 설정
options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

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

try:
    print("="*60)
    print("🍪 쿠키 저장 프로그램")
    print("="*60)
    
    # KREAM 접속
    print("\n1️⃣ KREAM 접속 중...")
    driver.get("https://kream.co.kr")
    time.sleep(2)
    
    print("\n✅ KREAM 메인 페이지 열림!")
    print("\n📌 이제 수동으로 네이버 로그인을 해주세요!")
    print("   1. 로그인 버튼 클릭")
    print("   2. 네이버로 로그인 선택")
    print("   3. 네이버 계정으로 로그인")
    print("   4. KREAM 메인 페이지로 돌아올 때까지 대기")
    
    input("\n✅ 로그인 완료 후 Enter를 누르세요...")
    
    # 로그인 확인
    if "kream.co.kr" in driver.current_url:
        print("\n✅ KREAM 페이지 확인!")
        
        # 쿠키 저장
        print("\n💾 쿠키 저장 중...")
        cookies = driver.get_cookies()
        
        with open("kream_cookies.pkl", "wb") as f:
            pickle.dump(cookies, f)
        
        print(f"✅ 쿠키 저장 완료! ({len(cookies)}개)")
        print("📁 파일: kream_cookies.pkl")
        
        print("\n" + "="*60)
        print("🎉 성공! 이제 kream_cookies.pkl 파일이 생성되었습니다!")
        print("   다음부터는 자동으로 로그인됩니다!")
        print("="*60)
    else:
        print("\n⚠️ KREAM 페이지가 아닙니다. 다시 시도해주세요.")
    
    input("\n브라우저를 확인하세요. Enter를 누르면 종료합니다...")

except Exception as e:
    print(f"\n❌ 오류 발생: {e}")

finally:
    driver.quit()
    print("\n✅ 브라우저 종료")