"""
검색 기능 테스트 v1 - 기본 기능만 확인
"""

import pytest
from pages.search_page import SearchPage


class TestSearch:
    """검색 기능 테스트"""
    
    @pytest.mark.smoke
    def test_search_nike(self, driver):
        """나이키 검색 테스트"""
        driver.get("https://kream.co.kr")
        search_page = SearchPage(driver)
        
        # 검색 실행
        result = search_page.search_product("나이키")
        
        # 검색이 성공했는지만 확인
        assert result, "검색 실행 실패"
        print("✅ 나이키 검색 완료!")
    
    def test_search_jordan(self, driver):
        """조던 검색 테스트"""
        driver.get("https://kream.co.kr")
        search_page = SearchPage(driver)
        
        # 검색 실행
        result = search_page.search_product("조던")
        
        # 검색이 성공했는지만 확인
        assert result, "검색 실행 실패"
        print("✅ 조던 검색 완료!")
    
    def test_search_dunk(self, driver):
        """덩크 검색 테스트"""
        driver.get("https://kream.co.kr")
        search_page = SearchPage(driver)
        
        # 검색 실행
        result = search_page.search_product("덩크")
        
        # 검색이 성공했는지만 확인
        assert result, "검색 실행 실패"
        print("✅ 덩크 검색 완료!")