# [Day 3] WebSocket 및 실시간 진행률 구현

## 📋 작업 개요
WebSocket 연결을 구현하여 실시간 다운로드 진행률을 클라이언트에 전송합니다.

## 🎯 목표
- WebSocket 엔드포인트 구현
- 실시간 진행률 업데이트
- 작업 취소 기능
- 자동 정리 시스템

## ✅ 작업 내용

### 1. WebSocket 기본 설정 (`websocket.py`)
- [ ] WebSocket 엔드포인트 생성
  ```python
  @app.websocket("/ws/download/{task_id}")
  ```
- [ ] 연결 관리 클래스 구현
  ```python
  class ConnectionManager:
      def __init__(self):
          self.active_connections: Dict[str, WebSocket] = {}
  ```
- [ ] 연결/해제 핸들러
- [ ] 메시지 브로드캐스트 함수

### 2. 진행률 업데이트 통합
- [ ] 다운로드 콜백에서 WebSocket 메시지 전송
- [ ] 진행률 메시지 포맷 (`type: "progress"`)
  ```json
  {
    "type": "progress",
    "data": {
      "percentage": 45,
      "downloaded_bytes": 15728640,
      "total_bytes": 34952533,
      "speed": "2.5 MB/s",
      "eta": "00:00:15"
    }
  }
  ```
- [ ] 상태 변경 메시지 (`type: "status"`)
- [ ] 완료 메시지 (`type: "complete"`)
- [ ] 에러 메시지 (`type: "error"`)

### 3. WebSocket 테스트 클라이언트
- [ ] 간단한 HTML 테스트 페이지 작성
- [ ] JavaScript WebSocket 연결 코드
- [ ] 메시지 수신 및 콘솔 출력
- [ ] 연결 상태 표시

**파일**: `src/youtube_downloader/web/static/test_ws.html`

### 4. 작업 취소 기능
- [ ] `DELETE /api/v1/download/{task_id}` 엔드포인트
- [ ] 다운로드 프로세스 중단 로직
- [ ] 임시 파일 정리
- [ ] 취소 메시지 WebSocket 전송

### 5. 자동 정리 시스템 (`cleanup.py`)
- [ ] 완료된 작업 자동 삭제 (1시간 후)
- [ ] 스케줄러 설정 (`APScheduler` 또는 `asyncio`)
- [ ] 임시 파일 정리 로직
- [ ] 메모리 정리

## 🧪 테스트 방법

### WebSocket 연결 테스트
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/download/{task_id}');

ws.onopen = () => console.log('연결됨');
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('메시지:', data);
};
```

### 전체 플로우 테스트
1. 다운로드 시작 (POST /api/v1/download)
2. WebSocket 연결
3. 실시간 진행률 수신
4. 완료 메시지 수신
5. 파일 다운로드

### 동시 다운로드 테스트
- 5개 동시 다운로드
- 각각 WebSocket 연결
- 진행률 독립적으로 업데이트

## 📊 예상 산출물

### 생성될 파일
```
src/youtube_downloader/web/
├── websocket.py          # WebSocket 핸들러 (신규)
├── cleanup.py            # 자동 정리 시스템 (신규)
└── static/
    └── test_ws.html      # WebSocket 테스트 페이지 (신규)
```

### 수정될 파일
- `api.py`: 작업 취소 엔드포인트 추가
- `tasks.py`: WebSocket 메시지 전송 통합
- `app.py`: WebSocket 라우터 등록

## 📝 참고 문서
- [작업 계획서](../docs/web/01-웹-인터페이스-작업-계획서.md)
- [API 명세서](../docs/web/02-API-명세서.md)
- [개발 로드맵](../docs/web/04-개발-로드맵.md)
- [FastAPI WebSocket 가이드](https://fastapi.tiangolo.com/advanced/websockets/)

## ⏱️ 예상 소요 시간
**8시간** (1일)

## 🏷️ Labels
`enhancement`, `web-interface`, `backend`, `websocket`, `day-3`

## 📌 우선순위
**High** - 실시간 진행률은 핵심 UX 기능

## ✔️ 완료 조건
- [ ] WebSocket 연결이 정상 동작
- [ ] 실시간 진행률이 클라이언트에 전송됨
- [ ] 작업 취소 기능이 동작
- [ ] 자동 정리 시스템이 동작
- [ ] 동시 다운로드 테스트 통과 (5개)
- [ ] 커밋 완료

## 🔗 관련 이슈
- 이전: #2 [Day 2] 다운로드 API 구현
- 다음: #[Day 4] 프론트엔드 UI 구현
