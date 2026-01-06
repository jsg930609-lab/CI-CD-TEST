from selenium import webdriver
import time

# 드라이버 초기화
driver = webdriver.Chrome()

# 브라우저 최대화
driver.maximize_window()

# 네이버 열기
driver.get("https://www.naver.com")

# 5초 대기 (페이지 확인)
time.sleep(5)

# 브라우저 종료
driver.quit()

print("✅ 첫 번째 스크립트 실행 완료!")