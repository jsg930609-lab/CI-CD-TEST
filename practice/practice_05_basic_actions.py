from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import time

driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://kream.co.kr")

wait = WebDriverWait(driver, 10)

# 1. 검색 아이콘 클릭 및 텍스트 입력
try:
    search_icon = driver.find_element(By.CSS_SELECTOR, "#wrap > div.header-wrapper > div > div > div > div > div > div > div.header_main > div > div.right > div > button")

    search_bar = driver.find_element(By.CSS_SELECTOR, ".search")
    
    # 클릭
    search_icon.click()
    print("✅ 검색 아이콘 클릭")
    
    # 검색창 선택
    search_bar.click()
    print("✅ 검색창 클릭")


    # 텍스트 입력
    search_bar.send_keys("나이키 덩크")
    print("✅ '나이키 덩크' 입력")
    
    time.sleep(1)
    
    # 엔터키 입력
    search_bar.send_keys(Keys.ENTER)
    print("✅ 검색 실행")
    
    time.sleep(3)
    
    # 검색 결과 확인
    print(f"현재 URL: {driver.current_url}")
    
except Exception as e:
    print(f"❌ 오류 발생: {e}")
