from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://kream.co.kr")

time.sleep(3)  # 페이지 로딩 대기

# 1. 로고 찾기
try:
    logo = driver.find_element(By.CSS_SELECTOR, "#wrap > div.header-wrapper > div > div > div > div > div > div > div.header_main > div > h1 > a")
    print("✅ 로고 발견!")
except:
    print("❌ 로고를 못 찾았습니다")

# 2. 네비게이션 메뉴 찾기
try:
    nav_items = driver.find_elements(By.CSS_SELECTOR, "#wrap > div.header-wrapper > div > div > div > div > div > div > div.header_main > div > div.right > div")
    print(f"✅ 메뉴 {len(nav_items)}개 발견!")
    for item in nav_items[:3]:  # 처음 3개만 출력
        print(f"  - {item.text}")
except Exception as e:
    print(f"❌ 메뉴를 못 찾았습니다: {e}")

# 3. 검색창 찾기
try:
    search_input = driver.find_element(By.CSS_SELECTOR, "#wrap > div.header-wrapper > div > div > div > div > div > div > div.header_main > div > div.right > div > button > svg")
    print("✅ 검색 버튼 발견!")
except Exception as e:
    print(f"❌ 검색 버튼을 못 찾았습니다: {e}")

# 4.로그인 버튼
try:
    search_input = driver.find_element(By.CSS_SELECTOR, "#wrap > div.header-wrapper > div > div > div > div > div > div > div.header_top > div > ul > li:nth-child(5) > a")
    print("✅ 로그인 버튼 발견!")
except Exception as e:
    print(f"❌ 로그인 버튼을 못 찾았습니다: {e}")

# 5. 상품 카드 (지금 인기)
try:
    search_input = driver.find_element(By.CSS_SELECTOR, "#wrap > div.layout__main--without-search > div > div > div.home-sd-screen > div > div.layout_list_vertical.pc\:w-fill.pc\:h-fit.pc\:maxw-1280.pc\:rgap-12.pc\:pt-40.pc\:pb-40.tablet\:w-fill.tablet\:h-fit.tablet\:maxw-960.tablet\:rgap-8.tablet\:pt-16.tablet\:pb-16.mo\:w-fill.mo\:h-fit.mo\:rgap-8.mo\:pt-16.mo\:pb-16.list-vertical-fill-available > div > div.drag-scroll.scrollable.snap.layout_grid_carousel_box.tablet\:pr-16.tablet\:pl-16.mo\:pr-16.mo\:pl-16.scroll-padding > div > a:nth-child(1) > div.shortcut-thumbnail > div > div > picture > img")
    print("✅ 상품 카드(지금 인기) 발견!")
except Exception as e:
    print(f"❌ 상품 카드(지금 인기)를 못 찾았습니다: {e}")
 
# 6. 상품 카드 (인기 뷰티)
try:
    search_input = driver.find_element(By.CSS_SELECTOR, "#wrap > div.layout__main--without-search > div > div > div.home-sd-screen > div > div.layout_list_vertical.pc\:w-fill.pc\:h-fit.pc\:maxw-1280.pc\:rgap-12.pc\:pt-40.pc\:pb-40.tablet\:w-fill.tablet\:h-fit.tablet\:maxw-960.tablet\:rgap-8.tablet\:pt-16.tablet\:pb-16.mo\:w-fill.mo\:h-fit.mo\:rgap-8.mo\:pt-16.mo\:pb-16.list-vertical-fill-available > div > div.drag-scroll.scrollable.snap.layout_grid_carousel_box.tablet\:pr-16.tablet\:pl-16.mo\:pr-16.mo\:pl-16.scroll-padding > div > a:nth-child(8) > div.shortcut-thumbnail > div > div > picture > img")
    print("✅ 상품 카드(인기 뷰티) 발견!")
except Exception as e:
    print(f"❌ 상품 카드(인기 뷰티)를 못 찾았습니다: {e}")

# 7. 푸터의 회사 정보
try:
    search_input = driver.find_element(By.CSS_SELECTOR, "#wrap > div:nth-child(4) > div > div > div > div.corporation_area > div.business_info > div > dl > dt")
    print("✅ 회사 정보 발견!")
except Exception as e:
    print(f"❌ 회사 정보를 못 찾았습니다: {e}")


time.sleep(2)
driver.quit()