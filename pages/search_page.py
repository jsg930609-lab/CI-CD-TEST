from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pages.base_page import BasePage


class SearchPage(BasePage):
    # 로케이터 정의
    SEARCH_INPUT = (By.CSS_SELECTOR, "input.search_input")
    SEARCH_RESULTS = (By.CSS_SELECTOR, ".product_card")
    PRODUCT_NAME = (By.CSS_SELECTOR, ".product_name")
    
    def search_product(self, keyword):
        """상품 검색"""
        self.input_text(self.SEARCH_INPUT, keyword)
        self.driver.find_element(*self.SEARCH_INPUT).send_keys(Keys.ENTER)
    
    def get_search_results_count(self):
        """검색 결과 개수 반환"""
        results = self.driver.find_elements(*self.SEARCH_RESULTS)
        return len(results)
    
    def is_keyword_in_results(self, keyword):
        """검색 결과에 키워드 포함 여부"""
        product_names = self.driver.find_elements(*self.PRODUCT_NAME)
        for name in product_names:
            if keyword.lower() in name.text.lower():
                return True
        return False