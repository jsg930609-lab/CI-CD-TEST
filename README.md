# KREAM Selenium Automation
> **AI(Claude)를 활용한 Selenium 자동화 테스트 및 CI/CD 파이프라인 학습 프로젝트**

## 🎯 프로젝트 개요

KREAM 웹사이트를 대상으로 한 자동화 테스트 학습 프로젝트입니다. AI(Claude)를 페어 프로그래밍 파트너로 활용하여 QA 자동화 프로세스를 구현했습니다.

## 🚀 주요 기능

### CI/CD 파이프라인
- **CI (Continuous Integration)**: 코드 push 시 자동 테스트 실행
- **CD (Continuous Deployment)**: 테스트 리포트 GitHub Pages 자동 배포
- **Python 3.11** 환경에서 테스트

### 📊 실시간 테스트 리포트
👉 **[Live Test Report](https://jsg930609-lab.github.io/CI-CD-TEST/)**

## 🧪 테스트 구성

### UI 자동화 테스트 (`test_search.py`)
- ✅ KREAM 검색 기능 테스트
- ✅ Page Object Model 패턴 적용
- ✅ JavaScript 클릭 처리
- ✅ 재시도 로직 구현
- ⚠️ CI 환경(Headless) 이슈로 현재 로컬 전용

## 🛠️ 기술 스택

### 테스트 자동화
- **Selenium WebDriver 4.15+**: 브라우저 자동화
- **pytest 7.4+**: 테스트 프레임워크
- **Page Object Model**: 테스트 코드 구조화 패턴

### CI/CD
- **GitHub Actions**: 자동화 파이프라인
- **GitHub Pages**: 테스트 리포트 호스팅

### 개발 환경
- **Python 3.11**
- **Chrome & ChromeDriver**
- **pytest-html**: HTML 리포트 생성

## 📁 프로젝트 구조

```
kream-selenium-automation/
├── .github/
│   └── workflows/
│       └── selenium-tests.yml    # CI/CD 설정
├── pages/
│   ├── __init__.py
│   ├── base_page.py              # Base Page 클래스
│   └── search_page.py            # 검색 페이지 POM
├── tests/
│   ├── __init__.py
│   ├── conftest.py               # pytest fixture 설정
│   └── test_search.py            # 검색 기능 테스트
├── reports/
│   └── index.html                # 리포트 랜딩 페이지
├── .gitignore
├── requirements.txt
├── pytest.ini
└── README.md
```

## 📊 CI/CD 워크플로우

### 자동 실행 조건
- `main` 브랜치에 코드 push
- 수동 실행 (Actions 탭에서)

### 파이프라인 단계
1. 📥 코드 체크아웃
2. 🐍 Python 3.11 환경 설정
3. 📦 의존성 설치
4. 🌐 Chrome 설치
5. 🧪 테스트 실행
6. 🚀 GitHub Pages 배포

### 결과 확인
- **리포트**: [웹 페이지](https://jsg930609-lab.github.io/CI-CD-TEST/)에서 상세 결과 확인

## 🎓 학습 내용

### 구현 및 습득 기술
- ✅ Selenium WebDriver 기본 사용법
- ✅ pytest 프레임워크 활용
- ✅ Page Object Model 패턴 이해 및 적용
- ✅ GitHub Actions CI/CD 파이프라인 구축
- ✅ Python 가상환경 및 의존성 관리

### AI 활용 역량
- ✅ Claude를 페어 프로그래밍 파트너로 활용
- ✅ 기술적 문제 해결 과정 학습
- ✅ 효과적인 질문 및 커뮤니케이션 능력
- ✅ 빠른 학습 및 프로토타입 제작

## 📌 주요 이슈 및 해결 과정

### 1. Headless 모드 로케이터 불안정
**문제**: CI 환경(Headless Chrome)에서 동적 요소 선택 실패  
**시도한 해결책**:
- 대기 시간 증가 (2초 → 8초)
- 여러 로케이터 옵션 시도
- JavaScript 직접 실행

**최종 결과**: 로컬 환경에서 안정적 작동, CI는 스킵 처리

### 2. GitHub Pages 자동 배포
**문제**: gh-pages 브랜치는 생성되나 배포 안 됨  
**해결**: 
- Workflow permissions 설정 (Read and write)
- Settings → Pages에서 수동으로 브랜치 선택


**맥스** (QA Engineer)
- GitHub: [@jsg930609-lab](https://github.com/jsg930609-lab)

---