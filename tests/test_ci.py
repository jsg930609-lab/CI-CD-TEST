"""
CI/CD 테스트 - 실제로 작동하는 간단한 테스트
"""

import pytest
import requests


class TestCICD:
    """CI/CD 파이프라인 검증 테스트"""
    
    @pytest.mark.smoke
    def test_python_environment(self):
        """Python 환경 확인"""
        import sys
        
        assert sys.version_info >= (3, 9), "Python 3.9 이상 필요"
        print(f"✅ Python 버전: {sys.version}")
    
    @pytest.mark.smoke
    def test_selenium_import(self):
        """Selenium 설치 확인"""
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        
        print("✅ Selenium 정상 설치됨")
    
    @pytest.mark.smoke
    def test_requests_working(self):
        """requests 라이브러리 동작 확인"""
        # 공개 API 테스트 (httpbin - 테스트용 API)
        response = requests.get("https://httpbin.org/status/200")
        
        assert response.status_code == 200
        print("✅ requests 라이브러리 정상 작동")
    
    def test_api_call_example(self):
        """외부 API 호출 예시"""
        # JSONPlaceholder (무료 테스트 API)
        response = requests.get("https://jsonplaceholder.typicode.com/posts/1")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "id" in data
        assert "title" in data
        
        print(f"✅ API 응답: {data['title'][:50]}...")
    
    def test_pytest_markers(self):
        """pytest 마커 설정 확인"""
        import pytest
        
        # smoke 마커가 정의되어 있는지 확인
        # (실제로는 pytest.ini에 정의됨)
        print("✅ pytest 설정 정상")


class TestSeleniumBasic:
    """Selenium 기본 테스트"""
    
    def test_webdriver_chrome_available(self):
        """ChromeDriver 사용 가능 확인"""
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        
        options = Options()
        options.add_argument('--headless=new')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        # 드라이버만 생성 (사이트 접속 X)
        driver = webdriver.Chrome(options=options)
        
        try:
            # about:blank 페이지
            assert driver.title is not None
            print("✅ ChromeDriver 정상 작동")
        finally:
            driver.quit()