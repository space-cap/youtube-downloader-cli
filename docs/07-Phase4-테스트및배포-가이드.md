# Phase 4: 테스트 및 배포 가이드

## 📋 개요

Phase 3 고급 기능 구현 후 진행할 테스트, 문서화, 배포 작업에 대한 가이드입니다.

---

## 🧪 1. 테스트 전략

### 1.1 테스트 커버리지 목표

- **목표 커버리지**: 80% 이상
- **핵심 모듈**: 90% 이상 (downloader, cli)
- **유틸리티**: 70% 이상

### 1.2 테스트 유형

#### 단위 테스트 (Unit Tests)
- 각 함수/메서드의 독립적인 동작 검증
- Mock 객체 사용하여 외부 의존성 제거
- 빠른 실행 속도

#### 통합 테스트 (Integration Tests)
- 실제 유튜브 API와의 통합 테스트
- 네트워크 요청 포함
- CI/CD에서 선택적 실행

#### E2E 테스트 (End-to-End Tests)
- 실제 사용자 시나리오 테스트
- CLI 명령어 전체 플로우 검증

---

## 📝 2. 테스트 코드 작성

### 2.1 Pytest 설정 확장

**파일: `pyproject.toml`**

```toml
[tool.pytest.ini_options]
markers = [
    "unit: 단위 테스트",
    "integration: 통합 테스트 (네트워크 필요)",
    "slow: 느린 테스트",
]
```

### 2.2 Mock 사용 예시

**파일: `tests/test_downloader_mock.py`**

```python
from unittest.mock import Mock, patch
import pytest
from youtube_downloader.downloader import Downloader

@patch('youtube_downloader.downloader.yt_dlp.YoutubeDL')
def test_download_with_mock(mock_ytdl):
    """Mock을 사용한 다운로드 테스트"""
    # Mock 설정
    mock_instance = Mock()
    mock_ytdl.return_value.__enter__.return_value = mock_instance
    mock_instance.extract_info.return_value = {
        'title': 'Test Video',
        'duration': 120,
        'uploader': 'Test Channel',
    }
    
    # 테스트 실행
    downloader = Downloader()
    result = downloader.download("https://test.url")
    
    # 검증
    assert result.success is True
    mock_instance.download.assert_called_once()
```

### 2.3 Fixture 확장

**파일: `tests/conftest.py`**

```python
import pytest
from pathlib import Path
from youtube_downloader.models import DownloadOptions, AudioOptions

@pytest.fixture
def download_options(tmp_path):
    """테스트용 다운로드 옵션"""
    return DownloadOptions(
        output_dir=tmp_path / "downloads",
        quality="720p",
    )

@pytest.fixture
def audio_options():
    """테스트용 오디오 옵션"""
    return AudioOptions(
        format="mp3",
        bitrate="192",
    )

@pytest.fixture
def mock_video_info():
    """Mock 동영상 정보"""
    from youtube_downloader.models import VideoInfo
    return VideoInfo(
        url="https://test.url",
        title="Test Video",
        duration=120,
        uploader="Test Channel",
    )
```

---

## 🔍 3. 코드 품질 검증

### 3.1 Ruff 설정 강화

**파일: `pyproject.toml`**

```toml
[tool.ruff.lint]
select = [
    "E",   # pycodestyle errors
    "F",   # pyflakes
    "I",   # isort
    "N",   # pep8-naming
    "W",   # pycodestyle warnings
    "UP",  # pyupgrade
    "B",   # flake8-bugbear
    "C4",  # flake8-comprehensions
    "SIM", # flake8-simplify
    "TCH", # flake8-type-checking
]

[tool.ruff.lint.per-file-ignores]
"tests/**/*.py" = ["S101"]  # pytest에서 assert 사용 허용
```

### 3.2 Mypy 설정 강화

```toml
[tool.mypy]
python_version = "3.13"
strict = true
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_any_generics = true
check_untyped_defs = true
files = ["src/youtube_downloader"]

[[tool.mypy.overrides]]
module = "yt_dlp.*"
ignore_missing_imports = true
```

### 3.3 Pre-commit 설정

**파일: `.pre-commit-config.yaml`** (새 파일)

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.7.0
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
```

---

## 📚 4. 문서화

### 4.1 API 문서 생성

**Sphinx 설정**

```bash
# Sphinx 설치
uv pip install sphinx sphinx-rtd-theme

# 문서 초기화
sphinx-quickstart docs/api

# 자동 API 문서 생성
sphinx-apidoc -o docs/api/source src/youtube_downloader
```

### 4.2 CHANGELOG 작성

**파일: `CHANGELOG.md`** (새 파일)

```markdown
# Changelog

## [0.2.0] - 2026-01-XX

### Added
- 재생목록 다운로드 기능
- 고품질 오디오 다운로드 (FLAC, 320kbps 지원)
- 다운로드 이력 관리
- 자막 다운로드 기능
- 동시 다운로드 지원

### Changed
- 메타데이터 저장 형식 개선
- 파일명 정리 로직 개선
- 진행률 표시 개선

### Fixed
- 특수문자 파일명 처리 버그 수정
- 재시도 로직 개선

## [0.1.0] - 2026-01-11

### Added
- 기본 동영상 다운로드 기능
- CLI 인터페이스
- 설정 관리
- 기본 테스트
```

### 4.3 기여 가이드

**파일: `CONTRIBUTING.md`** (새 파일)

```markdown
# 기여 가이드

## 개발 환경 설정

1. 저장소 포크 및 클론
2. 의존성 설치: `uv pip install -e ".[dev]"`
3. Pre-commit 설치: `pre-commit install`

## 코드 스타일

- Ruff로 포매팅: `uv run ruff format .`
- 린팅 통과: `uv run ruff check .`
- 타입 체킹: `uv run mypy src/`

## 테스트

- 모든 테스트 실행: `uv run pytest`
- 커버리지 확인: `uv run pytest --cov`

## Pull Request

1. 기능 브랜치 생성
2. 테스트 작성
3. 문서 업데이트
4. PR 생성
```

---

## 🚀 5. 배포 프로세스

### 5.1 버전 관리

**Semantic Versioning 사용**
- MAJOR.MINOR.PATCH (예: 0.2.0)
- MAJOR: 호환성 깨지는 변경
- MINOR: 새 기능 추가
- PATCH: 버그 수정

### 5.2 빌드 및 배포

**파일: `scripts/release.sh`** (새 파일)

```bash
#!/bin/bash
# 릴리스 스크립트

set -e

VERSION=$1

if [ -z "$VERSION" ]; then
    echo "사용법: ./scripts/release.sh <version>"
    exit 1
fi

echo "🔍 테스트 실행..."
uv run pytest

echo "🔍 코드 품질 검사..."
uv run ruff check .
uv run mypy src/

echo "📦 빌드..."
python -m build

echo "🏷️  Git 태그 생성..."
git tag -a "v$VERSION" -m "Release v$VERSION"
git push origin "v$VERSION"

echo "✅ 릴리스 v$VERSION 완료!"
```

### 5.3 PyPI 배포

```bash
# TestPyPI에 먼저 배포
uv run twine upload --repository testpypi dist/*

# 테스트 설치
pip install --index-url https://test.pypi.org/simple/ youtubedownloadercli

# 문제 없으면 PyPI에 배포
uv run twine upload dist/*
```

### 5.4 GitHub Release

1. GitHub에서 새 Release 생성
2. 태그 선택
3. CHANGELOG 내용 복사
4. 빌드 파일 첨부 (wheel, tar.gz)

---

## 🔄 6. CI/CD 설정

### 6.1 GitHub Actions

**파일: `.github/workflows/test.yml`** (새 파일)

```yaml
name: Tests

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        python-version: ["3.13"]

    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install UV
      run: pip install uv
    
    - name: Install dependencies
      run: uv pip install -e ".[dev]"
    
    - name: Run tests
      run: uv run pytest --cov
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
```

**파일: `.github/workflows/lint.yml`**

```yaml
name: Lint

on: [push, pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: "3.13"
    
    - name: Install UV
      run: pip install uv
    
    - name: Install dependencies
      run: uv pip install -e ".[dev]"
    
    - name: Run Ruff
      run: uv run ruff check .
    
    - name: Run Mypy
      run: uv run mypy src/
```

---

## 📊 7. 성능 테스트

### 7.1 벤치마크

**파일: `tests/benchmark.py`**

```python
import time
from youtube_downloader.downloader import Downloader

def benchmark_download():
    """다운로드 성능 벤치마크"""
    downloader = Downloader()
    
    start = time.time()
    # 테스트 동영상 다운로드
    result = downloader.download("test_url")
    elapsed = time.time() - start
    
    print(f"다운로드 시간: {elapsed:.2f}초")
    return elapsed

if __name__ == "__main__":
    benchmark_download()
```

### 7.2 메모리 프로파일링

```bash
# memory_profiler 설치
uv pip install memory-profiler

# 프로파일링 실행
python -m memory_profiler tests/benchmark.py
```

---

## ✅ 8. 릴리스 체크리스트

### Phase 4 완료 전 확인사항

- [ ] 모든 단위 테스트 통과
- [ ] 통합 테스트 통과
- [ ] 코드 커버리지 80% 이상
- [ ] Ruff 린팅 통과
- [ ] Mypy 타입 체킹 통과
- [ ] 문서 업데이트 완료
- [ ] CHANGELOG 작성
- [ ] README 업데이트
- [ ] 버전 번호 업데이트
- [ ] Git 태그 생성
- [ ] GitHub Release 생성
- [ ] PyPI 배포 (선택)

---

## 🎯 9. 향후 계획

### v0.3.0 계획
- GUI 버전 개발 (Tkinter/PyQt)
- 웹 인터페이스 (FastAPI)
- 다중 플랫폼 지원 (Vimeo, Twitch)

### v1.0.0 계획
- 안정화 및 최적화
- 전체 문서 완성
- 커뮤니티 피드백 반영
- 프로덕션 준비 완료
