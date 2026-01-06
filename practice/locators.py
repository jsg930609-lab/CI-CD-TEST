from selenium import webdriver
from selenium.webdriver.common.by import By
from pynput import keyboard
import time

driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://kream.co.kr")

time.sleep(2)

try:
    element = driver.find_element(By.CSS_SELECTOR, "button.btn_search")
    print("✅ 요소를 찾았습니다!")
    print(f"표시 여부: {element.is_displayed()}")
    
    element.click()
    print("✅ 클릭 완료!")
    
except Exception as e:
    print(f"❌ 에러: {e}")

print("\n✅ 테스트 완료! 브라우저를 확인하세요.")
print("⌨️  ESC를 누르면 종료됩니다...")

keyboard.wait('esc')

print("\n🛑 브라우저 종료 중...")
driver.quit()
print("✅ 종료 완료!")