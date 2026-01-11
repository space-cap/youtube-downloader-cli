# 🎥 유튜브 다운로더 CLI

파이썬으로 개발된 유튜브 동영상 다운로드 명령줄 도구입니다.

## ✨ 주요 기능

- 🎬 유튜브 동영상 다운로드
- 🎵 오디오 전용 다운로드 (MP3)
- 📊 다양한 화질 선택 (4K, 1080p, 720p 등)
- 📈 실시간 진행률 표시
- 📝 메타데이터 및 썸네일 저장
- ⚙️ 사용자 설정 관리

## 🚀 설치

### 요구사항
- Python 3.13 이상
- UV (권장) 또는 pip

### 설치 방법

```bash
# 저장소 클론
git clone <repository-url>
cd YoutubeDownloaderCli

# UV로 설치
uv venv
uv pip install -e .

# 또는 pip로 설치
pip install -e .
```

## 📖 사용법

### 기본 다운로드
```bash
ytdl download https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

### 특정 화질로 다운로드
```bash
ytdl download <URL> --quality 1080p
```

### 오디오만 다운로드
```bash
ytdl download <URL> --audio-only
```

### 메타데이터 및 썸네일 저장
```bash
ytdl download <URL> --metadata --thumbnail
```

### 사용 가능한 포맷 확인
```bash
ytdl list-formats <URL>
```

### 설정 관리
```bash
# 현재 설정 확인
ytdl config show
```

## 🛠 개발

### 개발 환경 설정
```bash
# 개발 의존성 포함 설치
uv pip install -e ".[dev]"

# 코드 포매팅
uv run ruff format .

# 린팅
uv run ruff check --fix .

# 타입 검사
uv run mypy src/

# 테스트 실행
uv run pytest
```

## 📚 문서

- [작업 계획서](./docs/01-작업-계획서.md)
- [프로젝트 개요](./docs/02-프로젝트-개요.md)
- [기술 스택](./docs/03-기술-스택.md)
- [개발 가이드](./docs/04-개발-가이드.md)
- [사용자 가이드](./docs/05-사용자-가이드.md)

## 📝 라이선스

MIT License

## 🤝 기여

이슈와 풀 리퀘스트를 환영합니다!
