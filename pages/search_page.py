"""
KREAM 검색 페이지 (CI 환경 대응)
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
import time
import os


class SearchPage(BasePage):
    """검색 페이지 POM"""
    
    # ==========================================
    # 로케이터 정의
    # ==========================================
    SEARCH_ICON = (By.CSS_SELECTOR, "button.btn_search")
    SEARCH_INPUT = (By.CSS_SELECTOR, "input.input_search")
    SEARCH_MODAL = (By.CSS_SELECTOR, "#modal-layer")
    SEARCH_RESULTS = (By.CSS_SELECTOR, ".product_card")
    
    def __init__(self, driver):
        super().__init__(driver)
        # CI 환경에서는 대기 시간 증가
        wait_time = 20 if os.getenv('CI') else 10
        self.wait = WebDriverWait(driver, wait_time)
    
    # ==========================================
    # 액션 메서드
    # ==========================================
    
    def search_product(self, keyword):
        """상품 검색"""
        try:
            # 1. 페이지 로딩 대기 (CI 환경에서 더 길게)
            sleep_time = 5 if os.getenv('CI') else 2
            time.sleep(sleep_time)
            print(f"⏳ 페이지 로딩 대기 중... ({sleep_time}초)")
            
            # 2. 검색 아이콘 찾기 (재시도 포함)
            max_retries = 3
            search_icon = None
            
            for attempt in range(max_retries):
                try:
                    search_icon = self.wait.until(EC.element_to_be_clickable(self.SEARCH_ICON))
                    print(f"✅ 검색 아이콘 발견 (시도 {attempt + 1}/{max_retries})")
                    break
                except:
                    print(f"⚠️ 검색 아이콘을 찾지 못함 (시도 {attempt + 1}/{max_retries})")
                    
                    if attempt < max_retries - 1:
                        print("🔄 페이지 새로고침")
                        self.driver.refresh()
                        time.sleep(sleep_time)
                    else:
                        raise Exception("검색 아이콘을 찾을 수 없습니다")
            
            # 3. JavaScript 클릭
            self.driver.execute_script("arguments[0].click();", search_icon)
            print("✅ 검색 아이콘 클릭 (JavaScript)")
            time.sleep(2)
            
            # 4. 검색 모달 확인
            try:
                modal = self.wait.until(EC.visibility_of_element_located(self.SEARCH_MODAL))
                print("✅ 검색 모달 열림!")
            except:
                print("⚠️ 검색 모달 확인 실패 - 계속 진행")
            
            # 5. 검색창 선택
            search_input = self.wait.until(EC.visibility_of_element_located(self.SEARCH_INPUT))
            print("✅ 검색창 선택 완료")
            
            # 6. 키워드 입력
            search_input.clear()
            search_input.send_keys(keyword)
            print(f"✅ 키워드 입력: {keyword}")
            
            # 7. 엔터
            search_input.send_keys(Keys.ENTER)
            print(f"✅ 검색 실행")
            
            # 8. 결과 로딩 대기
            time.sleep(3)
            
            return True
            
        except Exception as e:
            print(f"❌ 검색 실패: {e}")
            print(f"현재 URL: {self.driver.current_url}")
            
            # 스크린샷 저장
            try:
                self.driver.save_screenshot("search_error.png")
                print("📸 에러 스크린샷: search_error.png")
            except:
                pass
            
            return False
    
    # ==========================================
    # 검증 메서드
    # ==========================================
    
    def get_search_results_count(self):
        """검색 결과 개수 반환"""
        try:
            time.sleep(2)
            results = self.driver.find_elements(*self.SEARCH_RESULTS)
            count = len(results)
            print(f"📊 검색 결과: {count}개")
            return count
        except Exception as e:
            print(f"⚠️ 검색 결과 확인 실패: {e}")
            return 0
    
    def is_search_url(self):
        """검색 결과 페이지인지 확인"""
        return "search" in self.driver.current_url.lower()