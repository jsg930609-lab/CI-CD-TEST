import pytest
from pages.search_page import SearchPage


class TestSearch:
    
    def test_search_with_valid_keyword(self, driver):
        """유효한 키워드로 검색 테스트"""
        search_page = SearchPage(driver)
        driver.get("https://kream.co.kr")
        
        # 검색 수행
        search_page.search_product("나이키 덩크")
        
        # 검증
        assert search_page.get_search_results_count() > 0, "검색 결과가 없습니다"
        assert search_page.is_keyword_in_results("나이키"), "검색 결과에 키워드가 없습니다"
    
    def test_search_with_no_results(self, driver):
        """결과 없는 검색 테스트"""
        search_page = SearchPage(driver)
        driver.get("https://kream.co.kr")
        
        search_page.search_product("xyzabc123nonexistent")
        
        assert search_page.get_search_results_count() == 0, "잘못된 검색 결과"