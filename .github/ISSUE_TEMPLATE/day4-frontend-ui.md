# [Day 4] 프론트엔드 UI 구현

## 📋 작업 개요
HTML 구조 및 CSS 스타일링을 완성하여 아름답고 반응형인 사용자 인터페이스를 구현합니다.

## 🎯 목표
- 완전한 HTML 구조 작성
- CSS 디자인 시스템 구현
- 반응형 레이아웃
- 다크 모드 지원

## ✅ 작업 내용

### 1. HTML 구조 (`index.html`)
- [ ] 기본 HTML 템플릿 (시맨틱 마크업)
- [ ] Header (로고 + 다크 모드 토글)
- [ ] Hero Section (제목 + 부제목)
- [ ] Download Form
  - [ ] URL 입력 필드
  - [ ] 화질 선택 드롭다운
  - [ ] 오디오 품질 선택 드롭다운
  - [ ] 체크박스 옵션 (오디오만, 메타데이터, 썸네일)
  - [ ] 다운로드 버튼
- [ ] Video Preview Card (숨김 상태)
- [ ] Progress Section (숨김 상태)
- [ ] Success/Error Alerts (숨김 상태)
- [ ] Footer

### 2. CSS 디자인 시스템 (`style.css`)
- [ ] CSS 변수 정의
  - [ ] 색상 (Primary, Secondary, Background, Text)
  - [ ] 타이포그래피 (폰트, 크기, 굵기)
  - [ ] 간격 (Spacing)
  - [ ] 모서리 (Border Radius)
  - [ ] 그림자 (Shadows)
- [ ] 라이트/다크 모드 변수
- [ ] 리셋 & 기본 스타일
- [ ] 컨테이너 레이아웃
- [ ] 컴포넌트 스타일링
  - [ ] Header
  - [ ] Input Fields (포커스/에러 상태)
  - [ ] Select Dropdowns
  - [ ] Checkboxes
  - [ ] Buttons (Primary/Secondary)
  - [ ] Progress Bar
  - [ ] Video Preview Card
  - [ ] Alerts (Success/Error)
  - [ ] Footer
- [ ] 반응형 디자인
  - [ ] 모바일 (<768px)
  - [ ] 태블릿 (768px-1024px)
  - [ ] 데스크톱 (>1024px)
- [ ] 애니메이션 (fadeIn, slideIn, pulse)

### 3. JavaScript 기본 기능 (`app.js`)
- [ ] 다크 모드 토글
- [ ] localStorage에 테마 저장
- [ ] 테마 아이콘 자동 변경

## 📊 예상 산출물

### 생성/수정될 파일
- `index.html` - 완전히 새로 작성 (~200줄)
- `style.css` - 완전히 새로 작성 (~800줄)
- `app.js` - 다크 모드 토글 추가 (~30줄)

### 구현될 기능
- 완전한 HTML 구조
- CSS 디자인 시스템
- 반응형 레이아웃
- 다크 모드 지원

## 🧪 테스트 방법

### 서버 실행
```bash
uv run uvicorn youtube_downloader.web.app:app --reload --port 8000
```

### 접속
```
http://localhost:8000
```

### 확인 사항
- [ ] 페이지 로드
- [ ] 다크 모드 토글 동작
- [ ] 반응형 레이아웃 (모바일/태블릿/데스크톱)
- [ ] 모든 컴포넌트 시각적 확인

## 📝 참고 문서
- [UI/UX 디자인 명세서](../docs/web/03-UI-UX-디자인-명세서.md)
- [개발 로드맵](../docs/web/04-개발-로드맵.md)

## ⏱️ 예상 소요 시간
**6시간** (1일)

## 🏷️ Labels
`enhancement`, `web-interface`, `frontend`, `ui`, `day-4`

## 📌 우선순위
**High** - 사용자 인터페이스 구현

## ✔️ 완료 조건
- [ ] HTML 구조 완성
- [ ] CSS 스타일링 완성
- [ ] 반응형 디자인 동작
- [ ] 다크 모드 전환 동작
- [ ] 모든 컴포넌트 시각적으로 완성
- [ ] 커밋 완료

## 🔗 관련 이슈
- 이전: #3 [Day 3] WebSocket 및 실시간 진행률
- 다음: #[Day 5] 프론트엔드 로직 구현
