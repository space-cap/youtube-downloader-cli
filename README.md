<div align="center">

# 🎥 YouTube Downloader CLI

**파이썬으로 개발된 강력하고 사용하기 쉬운 유튜브 동영상 다운로드 CLI 도구**

[![Python Version](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)

[기능](#-주요-기능) •
[설치](#-설치) •
[사용법](#-사용법) •
[문서](#-문서) •
[기여](#-기여하기)

</div>

---

## ✨ 주요 기능

### CLI (Command Line Interface)
- 🎬 **동영상 다운로드** - 다양한 화질 선택 (4K, 1080p, 720p, 480p 등)
- 🎵 **오디오 추출** - MP3 형식으로 오디오만 다운로드 (32~320kbps 선택 가능)
- 📊 **포맷 선택** - 사용 가능한 모든 포맷 확인 및 선택
- 📈 **실시간 진행률** - Rich 라이브러리 기반 아름다운 진행률 표시
- 📝 **메타데이터 관리** - 동영상 정보 및 썸네일 저장
- ⚙️ **설정 관리** - 사용자 정의 설정 저장 및 관리
- 🚀 **빠른 성능** - yt-dlp 기반 최적화된 다운로드
- ✂️ **오디오 자르기** - 오디오 파일의 특정 구간 추출

### 🌐 웹 인터페이스 (NEW!)
- 🖥️ **직관적인 UI** - 아름답고 사용하기 쉬운 웹 인터페이스
- 📱 **반응형 디자인** - 모바일, 태블릿, 데스크톱 모두 지원
- 🌙 **다크 모드** - 눈의 피로를 줄이는 다크 모드 지원
- ⚡ **실시간 진행률** - WebSocket 기반 실시간 다운로드 진행률
- 🎯 **미리보기** - URL 입력 시 동영상 정보 미리보기
- 🔄 **동시 다운로드** - 여러 동영상 동시 다운로드 지원

## 📸 스크린샷

```bash
$ ytdl download https://www.youtube.com/watch?v=dQw4w9WgXcQ

다운로드 시작: Rick Astley - Never Gonna Give You Up
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:00 15.2 MB/s

✓ 다운로드 완료!
저장 위치: downloads/Rick Astley - Never Gonna Give You Up.mp4
```

## 🚀 설치

### 요구사항

- **Python 3.13** 이상
- **FFmpeg** (기본 내장, 시스템 설치 시 우선 사용)
- **UV** (권장) 또는 pip

### 빠른 시작

```bash
# 1. 저장소 클론
git clone https://github.com/yourusername/YoutubeDownloaderCli.git
cd YoutubeDownloaderCli

# 2. 가상환경 생성 및 의존성 설치 (UV 사용)
uv venv
uv pip install -e .

# 3. 가상환경 활성화
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # macOS/Linux

# 4. 설치 확인
ytdl --version
```

> **💡 개발 모드**: 가상환경을 활성화하지 않고 사용하려면 `uv run ytdl` 명령어를 사용하세요.
> ```bash
> uv run ytdl --version
> uv run ytdl download <URL>
> ```

### pip 사용

```bash
# 가상환경 생성
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 설치
pip install -e .
```
```

## 📖 사용법

> **📌 참고**: 아래 예시는 가상환경이 활성화된 상태를 가정합니다.
> 
> 가상환경을 활성화하지 않았다면 모든 `ytdl` 명령어 앞에 `uv run`을 붙여주세요:
> ```bash
> uv run ytdl download <URL>
> 
> uv run ytdl download https://www.youtube.com/watch?v=XFWdfoRl_ig --quality 720p
> ```

### 기본 명령어

#### 동영상 다운로드

```bash
# 기본 다운로드 (최고 화질)
ytdl download https://www.youtube.com/watch?v=VIDEO_ID

# 특정 화질 선택
ytdl download <URL> --quality 1080p

# 다운로드 경로 지정
ytdl download <URL> --output ~/Videos
```

#### 오디오 다운로드

```bash
# MP3로 오디오만 다운로드 (기본 192kbps)
ytdl download <URL> --audio-only

# 최고 음질로 다운로드 (320kbps)
ytdl download <URL> --audio-only --audio-quality 320

# 파일 크기 절약 (128kbps)
ytdl download <URL> --audio-only --audio-quality 128

# 100MB 이하로 맞추기 (48kbps, 4시간 영상 기준 ~86MB)
ytdl download <URL> --audio-only --audio-quality 48
```

**사용 가능한 음질 옵션:** `32`, `48`, `64`, `96`, `128`, `192` (기본), `256`, `320` (kbps)

**💡 파일 크기 참고 (4시간 영상 기준):**
- `48kbps`: ~86MB (100MB 이하, 음성 명료)
- `64kbps`: ~115MB (음성 콘텐츠 권장)
- `96kbps`: ~173MB (팟캐스트/강의)
- `192kbps`: ~346MB (기본, 음악 포함)

#### 오디오 자르기

```bash
# 기본 사용법 (5분부터 10분까지 자르기)
ytdl trim input.mp3 --start 00:05:00 --end 00:10:00

# 시작부터 3분까지 자르기
ytdl trim input.mp3 --end 00:03:00

# 1시간 30분부터 끝까지 자르기
ytdl trim input.mp3 --start 01:30:00
```

#### 메타데이터 저장

```bash
# 메타데이터와 썸네일 함께 저장
ytdl download <URL> --metadata --thumbnail
```

#### 포맷 확인

```bash
# 사용 가능한 모든 포맷 확인
ytdl list-formats <URL>
```

#### 설정 관리

```bash
# 현재 설정 확인
ytdl config show

# 도움말
ytdl --help
ytdl download --help
```

### 고급 사용법

더 많은 사용 예시는 [사용자 가이드](./docs/05-사용자-가이드.md)를 참조하세요.

---

## 🌐 웹 인터페이스 사용하기

### 서버 실행

```bash
# 개발 서버 실행
uv run uvicorn youtube_downloader.web.app:app --reload --port 8000

# 또는 가상환경 활성화 후
uvicorn youtube_downloader.web.app:app --reload --port 8000
```

### 접속

브라우저에서 http://localhost:8000 을 열어주세요.

### 사용 방법

1. **URL 입력**: YouTube 동영상 URL을 입력하세요
2. **미리보기 확인**: 동영상 정보가 자동으로 표시됩니다
3. **옵션 선택**: 화질, 오디오 품질, 기타 옵션을 선택하세요
4. **다운로드 시작**: "다운로드 시작" 버튼을 클릭하세요
5. **실시간 진행률**: WebSocket을 통해 실시간으로 진행률을 확인하세요
6. **파일 다운로드**: 완료 후 "파일 다운로드" 버튼을 클릭하세요

### 주요 기능

- **다크 모드**: 우측 상단의 🌙 버튼으로 전환
- **반응형 디자인**: 모바일, 태블릿, 데스크톱 모두 지원
- **실시간 진행률**: 다운로드 속도, 남은 시간 실시간 표시
- **에러 처리**: 명확한 에러 메시지 제공

자세한 내용은 [웹 인터페이스 가이드](./docs/web/README.md)를 참조하세요.

---

## 🛠 개발

### 개발 환경 설정

```bash
# 개발 의존성 포함 설치
uv pip install -e ".[dev]"

# Pre-commit hooks 설치 (선택사항)
pre-commit install
```

### 코드 품질 검사

```bash
# 코드 포매팅
uv run ruff format .

# 린팅
uv run ruff check --fix .

# 타입 검사
uv run mypy src/

# 테스트 실행
uv run pytest

# 커버리지 포함 테스트
uv run pytest --cov
```

### 프로젝트 구조

```
YoutubeDownloaderCli/
├── src/
│   └── youtube_downloader/
│       ├── cli.py              # CLI 진입점
│       ├── downloader.py       # 다운로드 엔진
│       ├── config.py           # 설정 관리
│       ├── models.py           # 데이터 모델
│       └── utils.py            # 유틸리티
├── tests/                      # 테스트 코드
├── docs/                       # 문서
└── downloads/                  # 기본 다운로드 경로
```

## 📚 문서

- 📋 [작업 계획서](./docs/01-작업-계획서.md) - 프로젝트 로드맵 및 개발 계획
- 📖 [프로젝트 개요](./docs/02-프로젝트-개요.md) - 목표 및 아키텍처
- 🔧 [기술 스택](./docs/03-기술-스택.md) - 사용 기술 및 선택 근거
- 👨‍💻 [개발 가이드](./docs/04-개발-가이드.md) - 개발 환경 및 컨벤션
- 📘 [사용자 가이드](./docs/05-사용자-가이드.md) - 상세 사용법
- 🚀 [Phase 3 구현 가이드](./docs/06-Phase3-고급기능-구현가이드.md) - 고급 기능 개발
- ✅ [Phase 4 배포 가이드](./docs/07-Phase4-테스트및배포-가이드.md) - 테스트 및 배포

## 🗺 로드맵

### ✅ Phase 1-2: 기본 기능 (완료)
- [x] 프로젝트 구조 설정
- [x] 기본 다운로드 기능
- [x] CLI 인터페이스
- [x] 설정 관리
- [x] 기본 테스트

### 🚧 Phase 3: 고급 기능 (진행 중)
- [ ] 재생목록 다운로드
- [x] 오디오 품질 개선 (32~320kbps 선택 가능)
- [ ] 자막 다운로드
- [ ] 다운로드 이력 관리
- [ ] 동시 다운로드

### 📅 Phase 4: 테스트 및 배포 (계획)
- [ ] 통합 테스트
- [ ] CI/CD 설정
- [ ] PyPI 배포
- [ ] 문서 완성

### 🔮 향후 계획
- GUI 버전 개발
- 다중 플랫폼 지원 (Vimeo, Twitch)
- 웹 인터페이스

## 🤝 기여하기

기여를 환영합니다! 다음 방법으로 참여하실 수 있습니다:

1. 🐛 **버그 리포트** - [Issues](https://github.com/yourusername/YoutubeDownloaderCli/issues)에서 버그 제보
2. 💡 **기능 제안** - 새로운 기능 아이디어 제안
3. 🔧 **Pull Request** - 코드 기여

### 기여 절차

```bash
# 1. 저장소 포크
# 2. 기능 브랜치 생성
git checkout -b feature/amazing-feature

# 3. 변경사항 커밋
git commit -m "feat: Add amazing feature"

# 4. 브랜치 푸시
git push origin feature/amazing-feature

# 5. Pull Request 생성
```

자세한 내용은 [기여 가이드](./CONTRIBUTING.md)를 참조하세요.

## 📄 라이선스

이 프로젝트는 [MIT License](LICENSE) 하에 배포됩니다.

## ⚠️ 면책 조항

이 도구는 교육 목적으로 제공됩니다. 저작권이 있는 콘텐츠를 다운로드할 때는 해당 콘텐츠의 이용 약관과 저작권법을 준수해야 합니다.

## 🙏 감사의 말

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - 강력한 다운로드 엔진
- [Click](https://click.palletsprojects.com/) - CLI 프레임워크
- [Rich](https://rich.readthedocs.io/) - 아름다운 터미널 UI
- [Pydantic](https://docs.pydantic.dev/) - 데이터 검증

---

<div align="center">

**[⬆ 맨 위로](#-youtube-downloader-cli)**

Made with ❤️ by [Your Name](https://github.com/yourusername)

</div>
