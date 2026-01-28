# [Phase 1] 사용자 인증 시스템 구현

## 📋 작업 개요
크레딧 시스템의 기반이 되는 사용자 인증 시스템을 구현합니다.

## 🎯 목표
- PostgreSQL 데이터베이스 설정
- SQLAlchemy 모델 정의
- 회원가입/로그인 API 구현
- JWT 토큰 기반 인증

## ✅ 작업 내용

### Day 1-2: 데이터베이스 설정
- [ ] PostgreSQL 설치 및 설정
  - Docker로 PostgreSQL 실행
  - 데이터베이스 생성
  - 연결 테스트
- [ ] SQLAlchemy 설정
  - 의존성 추가 (`sqlalchemy`, `psycopg2-binary`, `alembic`)
  - 데이터베이스 연결 설정
  - Base 모델 정의
- [ ] SQLAlchemy 모델 정의
  - `User` 모델
  - `CreditTransaction` 모델
  - `Payment` 모델
  - `Download` 모델
- [ ] Alembic 마이그레이션
  - Alembic 초기화
  - 첫 번째 마이그레이션 생성
  - 마이그레이션 실행

### Day 3-4: 인증 API
- [ ] 의존성 추가
  - `python-jose[cryptography]` (JWT)
  - `passlib[bcrypt]` (비밀번호 해싱)
  - `python-multipart` (폼 데이터)
- [ ] Pydantic 모델
  - `UserRegister` (회원가입 요청)
  - `UserLogin` (로그인 요청)
  - `UserResponse` (사용자 정보 응답)
  - `Token` (토큰 응답)
- [ ] 인증 유틸리티
  - 비밀번호 해싱 함수
  - 비밀번호 검증 함수
  - JWT 토큰 생성 함수
  - JWT 토큰 검증 함수
- [ ] 인증 API 엔드포인트
  - `POST /api/v1/auth/register` - 회원가입
  - `POST /api/v1/auth/login` - 로그인
  - `GET /api/v1/auth/me` - 사용자 정보 조회
  - `POST /api/v1/auth/logout` - 로그아웃 (선택사항)

### Day 5: 인증 미들웨어 및 테스트
- [ ] JWT 인증 의존성
  - `get_current_user` 의존성 함수
  - 토큰 검증 로직
  - 에러 처리
- [ ] 보호된 라우트 적용
  - 기존 다운로드 API에 인증 추가
  - 크레딧 API에 인증 추가
- [ ] 테스트
  - 회원가입 테스트
  - 로그인 테스트
  - 인증된 요청 테스트
  - 에러 케이스 테스트

## 📊 예상 산출물

### 생성될 파일
- `src/youtube_downloader/web/database.py` - 데이터베이스 연결
- `src/youtube_downloader/web/models_db.py` - SQLAlchemy 모델
- `src/youtube_downloader/web/auth.py` - 인증 유틸리티
- `src/youtube_downloader/web/auth_api.py` - 인증 API 라우터
- `alembic/` - 마이그레이션 파일들
- `alembic.ini` - Alembic 설정

### 수정될 파일
- `pyproject.toml` - 의존성 추가
- `src/youtube_downloader/web/app.py` - 인증 라우터 등록
- `src/youtube_downloader/web/api.py` - 인증 의존성 추가

## 🧪 테스트 방법

### 회원가입
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123"}'
```

### 로그인
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123"}'
```

### 사용자 정보 조회
```bash
curl -X GET http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## 📝 참고 문서
- [크레딧 시스템 구현 계획](../docs/web/07-크레딧-시스템-구현-계획.md)
- [FastAPI 보안 가이드](https://fastapi.tiangolo.com/tutorial/security/)
- [SQLAlchemy 문서](https://docs.sqlalchemy.org/)

## ⏱️ 예상 소요 시간
**5일** (1주)

## 🏷️ Labels
`enhancement`, `authentication`, `database`, `credit-system`, `phase-1`

## 📌 우선순위
**High** - 크레딧 시스템의 기반

## ✔️ 완료 조건
- [ ] PostgreSQL 데이터베이스 설정 완료
- [ ] SQLAlchemy 모델 정의 완료
- [ ] 회원가입 API 동작
- [ ] 로그인 API 동작
- [ ] JWT 토큰 발급 및 검증 동작
- [ ] 보호된 라우트 인증 동작
- [ ] 모든 테스트 통과
- [ ] 커밋 완료

## 🔗 관련 이슈
- 다음: #[Phase 2] 크레딧 관리 시스템
