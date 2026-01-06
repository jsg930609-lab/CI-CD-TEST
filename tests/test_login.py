from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pynput import keyboard
from dotenv import load_dotenv
import os
import time

load_dotenv()

Naver_ACCOUNT = os.getenv("NAVER_ACCOUNT")
Naver_PASSWORD = os.getenv("NAVER_PASSWORD")

# Chrome 옵션 설정 (봇 감지 우회)
options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://kream.co.kr")

wait = WebDriverWait(driver, 10)

# 1. 로그인 버튼 선택
try:
    login_button = driver.find_element(By.CSS_SELECTOR, "#wrap > div.header-wrapper > div > div > div > div > div > div > div.header_top > div > ul > li:nth-child(5) > a")

    print("✅ 요소를 찾았습니다!")
    print(f"표시 여부: {login_button.is_displayed()}")
    
    login_button.click()
    print("✅ 클릭 완료!")

except Exception as e:
    print(f"❌ 오류 발생: {e}")

time.sleep(1)

# 2. 네이버 로그인 선택
try:
    naver_login_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#wrap > div.layout__main--without-search > div > form > div.social-login > button.btn.full.outline.btn_login_naver")))

    print("✅ 요소를 찾았습니다!")
    print(f"표시 여부: {naver_login_button.is_displayed()}")
    
    naver_login_button.click()
    print("✅ 클릭 완료!")

except Exception as e:
    print(f"❌ 오류 발생: {e}")


# 3. 네이버 아이디/패스워드 입력
try:
    # 아이디 입력창 선택, 입력
    login_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#id")))
    login_input.click()
    login_input.send_keys(Naver_ACCOUNT)
    print("✅ 아이디 입력 완료!")

    time.sleep(1)   

    # 패스워드 입력
    password_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#pw")))
    password_input.click()
    password_input.send_keys(Naver_PASSWORD)
    print("✅ 패스워드 입력 완료!")

    time.sleep(1)

    # 로그인 버튼 클릭
    login_submit_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#log\.login")))
    login_submit_button.click()
    print("✅ 네이버 로그인 시도!")

except Exception as e:
    print(f"❌ 오류 발생: {e}")

print("\n✅ 테스트 완료! 브라우저를 확인하세요.")
print("⌨️  ESC를 누르면 종료됩니다...")

input()

print("\n🛑 브라우저 종료 중...")
driver.quit() 
print("✅ 종료 완료!")