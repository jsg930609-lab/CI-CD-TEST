from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

driver = webdriver.Chrome()
driver.maximize_window()

# KREAM 메인 페이지 열기
driver.get("https://kream.co.kr")

# 현재 URL 출력
print(f"현재 URL: {driver.current_url}")

# 페이지 제목 출력
print(f"페이지 제목: {driver.title}")

time.sleep(5)
driver.quit()