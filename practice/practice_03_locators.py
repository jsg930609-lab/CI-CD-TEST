from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://kream.co.kr")

time.sleep(2)

# 실습: 검색창 찾기 (F12 눌러서 요소 확인)
try:
    # CSS Selector로 검색창 찾기
    search_box = driver.find_element(By.CSS_SELECTOR, "#wrap > div.header-wrapper > div > div > div > div > div > div > div.header_main > div > div.right > div > button > svg")
    print("✅ 검색창을 찾았습니다!")
    print(f"검색창 placeholder: {search_box.get_attribute('placeholder')}")
except Exception as e:
    print(f"❌ 검색창을 못 찾았습니다: {e}")

time.sleep(2)
driver.quit()