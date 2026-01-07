https://github.com/jsg930609-lab/CI-CD-TEST

## 프로젝트 개요
Selenium 자동화 테스트 및 CI/CD 파이프라인 구축 학습 프로젝트

## 테스트 전략

### CI/CD 테스트 (`test_ci.py`)
- ✅ Python 환경 검증
- ✅ Selenium 설치 확인
- ✅ ChromeDriver 작동 확인
- ✅ 외부 API 호출 테스트

### UI 테스트 (`test_search.py`) - 로컬 전용
- ✅ KREAM 검색 기능 테스트
- ✅ Page Object Model 패턴
- ⚠️ CI 환경 headless 이슈로 현재 스킵

## 실행

### CI/CD 테스트
\`\`\`bash
pytest tests/test_ci.py -v
\`\`\`

### UI 테스트 (로컬)
\`\`\`bash
pytest tests/test_search.py -v -s
\`\`\`

## 기술 스택
- Python 3.9/3.10/3.11
- Selenium, pytest
- GitHub Actions