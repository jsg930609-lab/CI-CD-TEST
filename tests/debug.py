"""
디버깅용 검색 테스트 - 단계별 확인
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 10)

try:
    print("\n" + "="*60)
    print("KREAM 검색 테스트 - 단계별 디버깅")
    print("="*60)
    
    # 1. KREAM 접속
    print("\n1️⃣ KREAM 접속...")
    driver.get("https://kream.co.kr")
    time.sleep(2)
    print(f"✅ 현재 URL: {driver.current_url}")
    
    # 2. 검색 아이콘 클릭
    print("\n2️⃣ 검색 아이콘 클릭...")
    search_btn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn_search"))
    )
    search_btn.click()
    time.sleep(1)
    print("✅ 검색 아이콘 클릭 완료")
    
    # 3. 검색창에 키워드 입력
    print("\n3️⃣ 검색어 입력...")
    search_input = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='text']"))
    )
    search_input.clear()
    search_input.send_keys("나이키")
    print("✅ '나이키' 입력 완료")
    
    # 4. 엔터
    print("\n4️⃣ 검색 실행...")
    search_input.send_keys(Keys.ENTER)
    time.sleep(3)
    print("✅ 검색 실행 완료")
    print(f"✅ 현재 URL: {driver.current_url}")
    
    # 5. 검색 결과 확인 (여러 로케이터 시도)
    print("\n5️⃣ 검색 결과 확인...")
    
    possible_selectors = [
        ".product_card",
        ".product-card",
        "[class*='product']",
        ".item_inner",
        ".search_result_item",
        "[data-product-id]",
    ]
    
    results = []
    for selector in possible_selectors:
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            if len(elements) > 0:
                print(f"✅ '{selector}' 발견: {len(elements)}개")
                results = elements
                break
            else:
                print(f"⚠️ '{selector}': 0개")
        except Exception as e:
            print(f"❌ '{selector}' 에러: {e}")
    
    if results:
        print(f"\n🎉 검색 성공! 총 {len(results)}개의 결과")
        
        # 첫 번째 상품 텍스트 출력
        try:
            first_text = results[0].text
            print(f"📦 첫 번째 상품:\n{first_text[:100]}...")
        except:
            pass
    else:
        print("\n⚠️ 검색 결과를 찾을 수 없습니다.")
        print("   페이지 소스 확인 필요!")
        
        # 스크린샷 저장
        driver.save_screenshot("debug_search_result.png")
        print("📸 스크린샷 저장: debug_search_result.png")
    
    # 6. 페이지 소스 저장 (분석용)
    with open("page_source.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    print("\n💾 페이지 소스 저장: page_source.html")
    
    print("\n" + "="*60)
    input("Enter를 누르면 종료합니다...")

except Exception as e:
    print(f"\n❌ 에러 발생: {e}")
    driver.save_screenshot("error_debug.png")
    print("📸 에러 스크린샷: error_debug.png")

finally:
    driver.quit()
    print("\n✅ 브라우저 종료")