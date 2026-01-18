# [Day 5] 프론트엔드 로직 구현

## 📋 작업 개요
JavaScript로 API 통신 및 WebSocket 연결을 구현하여 완전히 동작하는 웹 애플리케이션을 완성합니다.

## 🎯 목표
- API 통신 구현
- WebSocket 연결 및 실시간 진행률 업데이트
- 전체 다운로드 플로우 완성

## ✅ 작업 내용

### 1. 기본 JavaScript 구조
- [ ] 전역 변수 및 상수 정의
- [ ] DOM 요소 참조
- [ ] 이벤트 리스너 등록
- [ ] 초기화 함수

### 2. URL 입력 및 유효성 검사
- [ ] URL 입력 이벤트 핸들러
- [ ] URL 유효성 검사 함수
- [ ] 에러 메시지 표시
- [ ] 디바운싱 적용 (500ms)

### 3. 동영상 정보 조회
- [ ] `GET /api/v1/video/info` API 호출
- [ ] 로딩 상태 표시
- [ ] 응답 데이터 파싱
- [ ] Video Preview 렌더링
- [ ] 포맷 옵션 동적 생성

### 4. 다운로드 시작 및 WebSocket 연결
- [ ] 다운로드 버튼 클릭 핸들러
- [ ] `POST /api/v1/download` API 호출
- [ ] Task ID 저장
- [ ] WebSocket 연결 생성 (`ws://localhost:8000/ws/download/{task_id}`)
- [ ] WebSocket 메시지 핸들러
  - [ ] `progress`: 진행률 업데이트
  - [ ] `status`: 상태 변경
  - [ ] `complete`: 완료 처리
  - [ ] `error`: 에러 표시

### 5. 진행률 표시 및 파일 다운로드
- [ ] Progress Bar 업데이트 함수
- [ ] 진행률 텍스트 업데이트
- [ ] 속도 및 ETA 표시
- [ ] 완료 시 다운로드 버튼 표시
- [ ] 파일 다운로드 트리거 (`GET /api/v1/download/{task_id}/file`)
- [ ] 취소 버튼 기능

### 6. 에러 처리
- [ ] 네트워크 오류 처리
- [ ] API 오류 응답 처리
- [ ] WebSocket 연결 오류 처리
- [ ] 사용자 친화적 에러 메시지

### 7. UI 상태 관리
- [ ] 섹션 표시/숨김 함수
- [ ] 버튼 활성화/비활성화
- [ ] 로딩 스피너
- [ ] 폼 리셋 기능

## 📊 예상 산출물

### 수정될 파일
- `app.js` - 완전한 JavaScript 로직 (~500줄)

### 구현될 기능
- URL 유효성 검사
- 동영상 정보 조회 및 미리보기
- 다운로드 시작
- WebSocket 실시간 진행률
- 파일 다운로드
- 에러 처리

## 🧪 테스트 방법

### 전체 플로우 테스트
1. URL 입력
2. 동영상 정보 확인
3. 옵션 선택
4. 다운로드 시작
5. 실시간 진행률 확인
6. 파일 다운로드

### 에러 시나리오
- 잘못된 URL
- 네트워크 오류
- 서버 오류
- WebSocket 연결 끊김

## 📝 참고 문서
- [API 명세서](../docs/web/02-API-명세서.md)
- [개발 로드맵](../docs/web/04-개발-로드맵.md)
- [Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API)
- [WebSocket API](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket)

## ⏱️ 예상 소요 시간
**8시간** (1일)

## 🏷️ Labels
`enhancement`, `web-interface`, `frontend`, `javascript`, `day-5`

## 📌 우선순위
**High** - 핵심 기능 구현

## ✔️ 완료 조건
- [ ] URL 입력 및 유효성 검사 동작
- [ ] 동영상 정보 조회 동작
- [ ] 다운로드 시작 동작
- [ ] WebSocket 실시간 진행률 업데이트
- [ ] 파일 다운로드 동작
- [ ] 에러 처리 동작
- [ ] 전체 플로우 테스트 통과
- [ ] 커밋 완료

## 🔗 관련 이슈
- 이전: #[Day 4] 프론트엔드 UI 구현
- 다음: #[Day 6] 통합 테스트 및 배포
