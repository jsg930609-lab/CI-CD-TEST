"""
KREAM 검색 페이지 v1 (모달 열기 개선)
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
import time


class SearchPage(BasePage):
    """검색 페이지 POM"""
    
    # ==========================================
    # 로케이터 정의
    # ==========================================
    SEARCH_ICON = (By.CSS_SELECTOR, "button.btn_search")
    SEARCH_INPUT = (By.CSS_SELECTOR, "input.input_search")
    SEARCH_MODAL = (By.CSS_SELECTOR, "#modal-layer")  # 모달 확인용
    SEARCH_RESULTS = (By.CSS_SELECTOR, ".product_card")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.wait = WebDriverWait(driver, 10)
    
    # ==========================================
    # 액션 메서드
    # ==========================================
    
    def search_product(self, keyword):
        """상품 검색"""
        try:
            # 1. 페이지 로딩 대기
            time.sleep(1.5)
            print("⏳ 페이지 로딩 대기 중...")
            
            # 2. 검색 아이콘 찾기
            search_icon = self.wait.until(EC.element_to_be_clickable(self.SEARCH_ICON))
            print("✅ 검색 아이콘 발견")
        except:
            print("⚠️ 검색 아이콘을 찾지 못함 - 페이지 새로고침")
            self.driver.refresh()
            time.sleep(2)
        
            # 재시도
            search_icon = self.wait.until(EC.element_to_be_clickable(self.SEARCH_ICON))
            print("✅ 검색 아이콘 발견 (재시도 성공)")
            

        try:
            # 3. JavaScript로 클릭 (더 확실함)
            search_input = self.wait.until(EC.element_to_be_clickable(self.SEARCH_INPUT))
            print("✅ 검색 아이콘 클릭")
        except:
            self.driver.execute_script("arguments[0].click();", search_icon)
            print("✅ 검색 아이콘 클릭 (JavaScript)")
            time.sleep(2)
            

        try:
            # 4. 검색 모달이 열렸는지 확인
            modal = self.wait.until(EC.visibility_of_element_located(self.SEARCH_MODAL))
            print("✅ 검색 모달 열림 확인!")
        except:
            print("⚠️ 검색 모달이 안 보임 - 일반 클릭 재시도")
            search_icon.click()
            time.sleep(2)
        
        try:
            # 5. 검색창 선택
            search_input = self.wait.until(EC.visibility_of_element_located(self.SEARCH_INPUT))
            print("✅ 검색창 선택 완료")
            
            # 6. 검색창에 키워드 입력
            search_input.clear()
            search_input.send_keys(keyword)
            print(f"✅ 키워드 입력: {keyword}")
            
            # 7. 엔터 입력
            search_input.send_keys(Keys.ENTER)
            print(f"✅ 검색 실행")
            
            # 8. 검색 결과 로딩 대기
            time.sleep(3)
            
            return True
            
        except Exception as e:
            print(f"❌ 검색 실패: {e}")
            
            # 디버깅 정보 출력
            print(f"현재 URL: {self.driver.current_url}")
            
            # 에러 시 스크린샷
            try:
                self.driver.save_screenshot("search_error.png")
                print("📸 에러 스크린샷 저장: search_error.png")
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