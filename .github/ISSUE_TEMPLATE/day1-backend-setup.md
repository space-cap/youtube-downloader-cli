# [Day 1] 웹 인터페이스 백엔드 기초 설정

## 📋 작업 개요
FastAPI 기반 웹 인터페이스의 백엔드 기초를 구축합니다.

## 🎯 목표
- FastAPI 프로젝트 환경 설정
- 동영상 정보 조회 API 구현
- 기본 프로젝트 구조 생성

## ✅ 작업 내용

### 1. 프로젝트 환경 설정
- [ ] FastAPI 의존성 추가 (`fastapi`, `uvicorn`, `websockets`, `aiofiles`)
- [ ] `pyproject.toml` 업데이트
- [ ] 웹 인터페이스 디렉토리 구조 생성

### 2. Pydantic 모델 정의
- [ ] `VideoInfo` 모델
- [ ] `DownloadRequest/Response` 모델
- [ ] `ErrorResponse` 모델
- [ ] `WebSocketMessage` 모델

### 3. FastAPI 애플리케이션 설정
- [ ] 기본 앱 생성 (`app.py`)
- [ ] CORS 설정
- [ ] 정적 파일 서빙 설정
- [ ] API 라우터 등록

### 4. API 엔드포인트 구현
- [ ] `GET /`: HTML 페이지 반환
- [ ] `GET /health`: Health check
- [ ] `GET /api/v1/version`: API 버전 정보
- [ ] `GET /api/v1/video/info`: 동영상 정보 조회

### 5. 동영상 정보 조회 기능
- [ ] yt-dlp 통합
- [ ] URL 유효성 검사
- [ ] 동영상 정보 추출
- [ ] 포맷 정보 파싱
- [ ] 에러 핸들링

### 6. 정적 파일
- [ ] 기본 `index.html` 생성
- [ ] 기본 `style.css` 생성
- [ ] 기본 `app.js` 생성

## 🧪 테스트 방법

### 서버 실행
```bash
uv run uvicorn youtube_downloader.web.app:app --reload --port 8000
```

### 엔드포인트 테스트
```bash
# Health check
curl http://localhost:8000/health

# 동영상 정보 조회
curl "http://localhost:8000/api/v1/video/info?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

### Swagger UI
- http://localhost:8000/docs

## 📊 예상 산출물

### 생성될 파일
```
src/youtube_downloader/web/
├── __init__.py
├── app.py
├── models.py
├── api.py
└── static/
    ├── index.html
    ├── style.css
    └── app.js
```

### API 엔드포인트
- `GET /`: 메인 페이지
- `GET /health`: 헬스 체크
- `GET /api/v1/version`: 버전 정보
- `GET /api/v1/video/info`: 동영상 정보

## 📝 참고 문서
- [작업 계획서](../docs/web/01-웹-인터페이스-작업-계획서.md)
- [API 명세서](../docs/web/02-API-명세서.md)
- [개발 로드맵](../docs/web/04-개발-로드맵.md)

## ⏱️ 예상 소요 시간
**8시간** (1일)

## 🏷️ Labels
`enhancement`, `web-interface`, `backend`, `day-1`

## 📌 우선순위
**High** - 웹 인터페이스의 기초 작업

## ✔️ 완료 조건
- [ ] 서버가 정상적으로 실행됨
- [ ] Swagger UI에서 모든 엔드포인트 확인 가능
- [ ] 동영상 정보 조회 API가 정상 동작
- [ ] 모든 코드에 주석 추가
- [ ] 커밋 완료

## 🔗 관련 이슈
- 다음: #[Day 2] 다운로드 API 구현
