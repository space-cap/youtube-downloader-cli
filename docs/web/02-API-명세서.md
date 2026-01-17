# API 명세서

## 📋 개요

YouTube Downloader 웹 인터페이스의 REST API 및 WebSocket API 명세서입니다.

**Base URL**: `http://localhost:8000`

**API Version**: `v1`

---

## 🔐 인증

현재 버전에서는 인증이 필요하지 않습니다. (향후 추가 예정)

---

## 📡 REST API

### 1. 동영상 정보 조회

유튜브 URL로부터 동영상 정보를 가져옵니다.

#### Endpoint
```
GET /api/v1/video/info
```

#### Query Parameters
| 파라미터 | 타입 | 필수 | 설명 |
|---------|------|------|------|
| url | string | ✅ | 유튜브 동영상 URL |

#### Request Example
```http
GET /api/v1/video/info?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

#### Response (200 OK)
```json
{
  "success": true,
  "data": {
    "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "title": "Rick Astley - Never Gonna Give You Up",
    "duration": 212,
    "uploader": "Rick Astley",
    "thumbnail": "https://i.ytimg.com/vi/dQw4w9WgXcQ/maxresdefault.jpg",
    "description": "The official video for...",
    "formats": {
      "video": [
        {
          "format_id": "137",
          "ext": "mp4",
          "quality": "1080p",
          "filesize": 45678901
        },
        {
          "format_id": "136",
          "ext": "mp4",
          "quality": "720p",
          "filesize": 23456789
        },
        {
          "format_id": "135",
          "ext": "mp4",
          "quality": "480p",
          "filesize": 12345678
        }
      ],
      "audio": [
        {
          "format_id": "140",
          "ext": "m4a",
          "quality": "128kbps",
          "filesize": 3456789
        }
      ]
    }
  }
}
```

#### Error Responses

**400 Bad Request** - 잘못된 URL
```json
{
  "success": false,
  "error": {
    "code": "INVALID_URL",
    "message": "유효하지 않은 유튜브 URL입니다."
  }
}
```

**404 Not Found** - 동영상을 찾을 수 없음
```json
{
  "success": false,
  "error": {
    "code": "VIDEO_NOT_FOUND",
    "message": "동영상을 찾을 수 없습니다."
  }
}
```

**500 Internal Server Error** - 서버 오류
```json
{
  "success": false,
  "error": {
    "code": "INTERNAL_ERROR",
    "message": "서버 오류가 발생했습니다."
  }
}
```

---

### 2. 다운로드 시작

동영상 다운로드를 시작합니다.

#### Endpoint
```
POST /api/v1/download
```

#### Request Body
```json
{
  "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
  "options": {
    "quality": "1080p",
    "audio_only": false,
    "audio_quality": "192",
    "save_metadata": false,
    "save_thumbnail": false
  }
}
```

#### Request Body Parameters
| 파라미터 | 타입 | 필수 | 기본값 | 설명 |
|---------|------|------|--------|------|
| url | string | ✅ | - | 유튜브 동영상 URL |
| options.quality | string | ❌ | "best" | 화질 (best, 1080p, 720p, 480p) |
| options.audio_only | boolean | ❌ | false | 오디오만 다운로드 |
| options.audio_quality | string | ❌ | "192" | 오디오 비트레이트 (32, 48, 64, 96, 128, 192, 256, 320) |
| options.save_metadata | boolean | ❌ | false | 메타데이터 저장 |
| options.save_thumbnail | boolean | ❌ | false | 썸네일 저장 |

#### Response (202 Accepted)
```json
{
  "success": true,
  "data": {
    "task_id": "abc123def456",
    "status": "pending",
    "created_at": "2026-01-18T04:00:00Z"
  }
}
```

#### Error Responses

**400 Bad Request** - 잘못된 요청
```json
{
  "success": false,
  "error": {
    "code": "INVALID_REQUEST",
    "message": "잘못된 요청입니다.",
    "details": {
      "url": ["유효하지 않은 URL입니다."]
    }
  }
}
```

**429 Too Many Requests** - 요청 제한 초과
```json
{
  "success": false,
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "요청 제한을 초과했습니다. 잠시 후 다시 시도해주세요.",
    "retry_after": 60
  }
}
```

---

### 3. 다운로드 상태 조회

다운로드 작업의 현재 상태를 조회합니다.

#### Endpoint
```
GET /api/v1/download/{task_id}/status
```

#### Path Parameters
| 파라미터 | 타입 | 설명 |
|---------|------|------|
| task_id | string | 다운로드 작업 ID |

#### Request Example
```http
GET /api/v1/download/abc123def456/status
```

#### Response (200 OK) - 다운로드 중
```json
{
  "success": true,
  "data": {
    "task_id": "abc123def456",
    "status": "downloading",
    "progress": {
      "percentage": 45,
      "downloaded_bytes": 15728640,
      "total_bytes": 34952533,
      "speed": "2.5 MB/s",
      "eta": "00:00:15"
    },
    "video_info": {
      "title": "Rick Astley - Never Gonna Give You Up",
      "thumbnail": "https://i.ytimg.com/vi/dQw4w9WgXcQ/maxresdefault.jpg"
    }
  }
}
```

#### Response (200 OK) - 완료
```json
{
  "success": true,
  "data": {
    "task_id": "abc123def456",
    "status": "completed",
    "progress": {
      "percentage": 100,
      "downloaded_bytes": 34952533,
      "total_bytes": 34952533
    },
    "file": {
      "filename": "Rick Astley - Never Gonna Give You Up.mp4",
      "size": 34952533,
      "download_url": "/api/v1/download/abc123def456/file"
    },
    "completed_at": "2026-01-18T04:05:00Z"
  }
}
```

#### Response (200 OK) - 실패
```json
{
  "success": true,
  "data": {
    "task_id": "abc123def456",
    "status": "failed",
    "error": {
      "code": "DOWNLOAD_FAILED",
      "message": "다운로드에 실패했습니다."
    },
    "failed_at": "2026-01-18T04:03:00Z"
  }
}
```

#### Status Values
| 상태 | 설명 |
|------|------|
| pending | 대기 중 |
| downloading | 다운로드 중 |
| processing | 후처리 중 (변환 등) |
| completed | 완료 |
| failed | 실패 |

---

### 4. 파일 다운로드

완료된 파일을 다운로드합니다.

#### Endpoint
```
GET /api/v1/download/{task_id}/file
```

#### Path Parameters
| 파라미터 | 타입 | 설명 |
|---------|------|------|
| task_id | string | 다운로드 작업 ID |

#### Request Example
```http
GET /api/v1/download/abc123def456/file
```

#### Response (200 OK)
- **Content-Type**: `video/mp4` 또는 `audio/mpeg`
- **Content-Disposition**: `attachment; filename="Rick Astley - Never Gonna Give You Up.mp4"`
- **Body**: Binary file stream

#### Error Responses

**404 Not Found** - 파일을 찾을 수 없음
```json
{
  "success": false,
  "error": {
    "code": "FILE_NOT_FOUND",
    "message": "파일을 찾을 수 없습니다. 다운로드가 완료되지 않았거나 파일이 만료되었습니다."
  }
}
```

---

### 5. 작업 취소

진행 중인 다운로드 작업을 취소합니다.

#### Endpoint
```
DELETE /api/v1/download/{task_id}
```

#### Path Parameters
| 파라미터 | 타입 | 설명 |
|---------|------|------|
| task_id | string | 다운로드 작업 ID |

#### Response (200 OK)
```json
{
  "success": true,
  "data": {
    "task_id": "abc123def456",
    "status": "cancelled"
  }
}
```

---

## 🔌 WebSocket API

실시간 다운로드 진행률을 받기 위한 WebSocket 연결입니다.

### Endpoint
```
WS /ws/download/{task_id}
```

### Connection Example
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/download/abc123def456');

ws.onopen = () => {
  console.log('WebSocket 연결됨');
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('메시지 수신:', data);
};

ws.onerror = (error) => {
  console.error('WebSocket 오류:', error);
};

ws.onclose = () => {
  console.log('WebSocket 연결 종료');
};
```

### Message Types

#### 1. Progress Update
다운로드 진행률 업데이트

```json
{
  "type": "progress",
  "data": {
    "percentage": 45,
    "downloaded_bytes": 15728640,
    "total_bytes": 34952533,
    "speed": "2.5 MB/s",
    "eta": "00:00:15"
  },
  "timestamp": "2026-01-18T04:02:30Z"
}
```

#### 2. Status Change
작업 상태 변경

```json
{
  "type": "status",
  "data": {
    "status": "processing",
    "message": "파일 변환 중..."
  },
  "timestamp": "2026-01-18T04:04:00Z"
}
```

#### 3. Complete
다운로드 완료

```json
{
  "type": "complete",
  "data": {
    "filename": "Rick Astley - Never Gonna Give You Up.mp4",
    "size": 34952533,
    "download_url": "/api/v1/download/abc123def456/file"
  },
  "timestamp": "2026-01-18T04:05:00Z"
}
```

#### 4. Error
오류 발생

```json
{
  "type": "error",
  "data": {
    "code": "DOWNLOAD_FAILED",
    "message": "다운로드에 실패했습니다.",
    "details": "Network error"
  },
  "timestamp": "2026-01-18T04:03:00Z"
}
```

---

## 🚨 에러 코드

| 코드 | HTTP 상태 | 설명 |
|------|-----------|------|
| INVALID_URL | 400 | 유효하지 않은 URL |
| INVALID_REQUEST | 400 | 잘못된 요청 |
| VIDEO_NOT_FOUND | 404 | 동영상을 찾을 수 없음 |
| FILE_NOT_FOUND | 404 | 파일을 찾을 수 없음 |
| TASK_NOT_FOUND | 404 | 작업을 찾을 수 없음 |
| RATE_LIMIT_EXCEEDED | 429 | 요청 제한 초과 |
| DOWNLOAD_FAILED | 500 | 다운로드 실패 |
| INTERNAL_ERROR | 500 | 서버 내부 오류 |

---

## 📊 Rate Limiting

### 제한 정책
- **IP당 요청 제한**: 시간당 60회
- **동시 다운로드**: 최대 5개

### Rate Limit Headers
```http
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1705550400
```

---

## 🔍 예제 시나리오

### 전체 다운로드 플로우

```javascript
// 1. 동영상 정보 조회
const infoResponse = await fetch(
  '/api/v1/video/info?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ'
);
const info = await infoResponse.json();

// 2. 다운로드 시작
const downloadResponse = await fetch('/api/v1/download', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    url: 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
    options: {
      quality: '1080p',
      audio_only: false
    }
  })
});
const { data: { task_id } } = await downloadResponse.json();

// 3. WebSocket 연결로 실시간 진행률 수신
const ws = new WebSocket(`ws://localhost:8000/ws/download/${task_id}`);

ws.onmessage = (event) => {
  const message = JSON.parse(event.data);
  
  if (message.type === 'progress') {
    console.log(`진행률: ${message.data.percentage}%`);
  } else if (message.type === 'complete') {
    // 4. 파일 다운로드
    window.location.href = message.data.download_url;
    ws.close();
  } else if (message.type === 'error') {
    console.error('다운로드 실패:', message.data.message);
    ws.close();
  }
};
```

---

## 📝 참고사항

### CORS 설정
개발 환경에서는 모든 origin 허용:
```
Access-Control-Allow-Origin: *
```

프로덕션 환경에서는 특정 도메인만 허용 권장

### 파일 만료
- 다운로드 완료 후 **1시간** 뒤 자동 삭제
- 삭제 전 경고 메시지 표시 권장

### 최대 파일 크기
- **제한 없음** (현재)
- 향후 2GB 제한 추가 예정
