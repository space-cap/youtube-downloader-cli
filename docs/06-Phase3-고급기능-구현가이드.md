# Phase 3: 고급 기능 구현 가이드

## 📋 개요

Phase 1-2에서 구현한 기본 다운로드 기능을 확장하여 재생목록 다운로드, 오디오 품질 개선, 메타데이터 관리 등의 고급 기능을 추가합니다.

---

## 🎯 구현할 기능

### 1. 재생목록 다운로드
- 유튜브 재생목록 전체 다운로드
- 재생목록 범위 지정 (시작/끝 인덱스)
- 개별 동영상 선택 다운로드
- 재생목록 메타데이터 저장

### 2. 오디오 다운로드 개선
- 다양한 오디오 포맷 지원 (MP3, AAC, FLAC)
- 비트레이트 선택 (128k, 192k, 320k)
- 앨범 아트 임베딩
- ID3 태그 자동 설정

### 3. 메타데이터 관리 개선
- 구조화된 메타데이터 저장
- 자막 다운로드 및 저장
- 챕터 정보 추출
- 다운로드 이력 관리

### 4. 추가 편의 기능
- 동시 다운로드 (멀티스레딩)
- 다운로드 재개 기능
- 자동 파일명 정리
- 다운로드 완료 알림

---

## 🔧 1. 재생목록 다운로드 구현

### 1.1 모델 확장

**파일: `src/youtube_downloader/models.py`**

```python
from typing import List, Optional
from pydantic import BaseModel, Field

class PlaylistInfo(BaseModel):
    """재생목록 정보 모델"""
    
    url: str
    title: str
    uploader: str
    video_count: int
    videos: List[VideoInfo] = Field(default_factory=list)

class PlaylistDownloadOptions(BaseModel):
    """재생목록 다운로드 옵션"""
    
    start_index: int = Field(default=1, description="시작 인덱스")
    end_index: Optional[int] = Field(default=None, description="끝 인덱스")
    reverse: bool = Field(default=False, description="역순 다운로드")
    skip_existing: bool = Field(default=True, description="기존 파일 건너뛰기")
```

### 1.2 다운로더 확장

**파일: `src/youtube_downloader/downloader.py`**

```python
def download_playlist(
    self,
    url: str,
    playlist_options: Optional[PlaylistDownloadOptions] = None,
    progress_callback: Optional[Callable[[dict[str, Any]], None]] = None
) -> List[DownloadResult]:
    """
    재생목록 다운로드
    
    Args:
        url: 유튜브 재생목록 URL
        playlist_options: 재생목록 다운로드 옵션
        progress_callback: 진행률 콜백 함수
        
    Returns:
        각 동영상의 다운로드 결과 리스트
    """
    options = playlist_options or PlaylistDownloadOptions()
    results = []
    
    try:
        # 재생목록 정보 추출
        ydl_opts = {
            "quiet": True,
            "extract_flat": True,  # 메타데이터만 추출
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            playlist_info = ydl.extract_info(url, download=False)
            
            if not playlist_info or "entries" not in playlist_info:
                console.print("[red]재생목록 정보를 가져올 수 없습니다.[/red]")
                return results
            
            entries = playlist_info["entries"]
            total_videos = len(entries)
            
            # 범위 설정
            start = options.start_index - 1
            end = options.end_index if options.end_index else total_videos
            
            console.print(f"[cyan]재생목록: {playlist_info.get('title', 'Unknown')}[/cyan]")
            console.print(f"[cyan]총 {total_videos}개 동영상 중 {end - start}개 다운로드[/cyan]\n")
            
            # 각 동영상 다운로드
            for idx, entry in enumerate(entries[start:end], start=start + 1):
                if entry is None:
                    continue
                
                video_url = entry.get("url") or f"https://www.youtube.com/watch?v={entry['id']}"
                console.print(f"[{idx}/{end}] {entry.get('title', 'Unknown')}")
                
                result = self.download(video_url, progress_callback)
                results.append(result)
                
                if not result.success:
                    console.print(f"[yellow]경고: 다운로드 실패, 계속 진행...[/yellow]\n")
            
            return results
            
    except Exception as e:
        console.print(f"[red]재생목록 다운로드 에러: {str(e)}[/red]")
        return results
```

### 1.3 CLI 명령어 추가

**파일: `src/youtube_downloader/cli.py`**

```python
@cli.command()
@click.argument("url")
@click.option("--quality", "-q", default="best", help="화질 선택")
@click.option("--output", "-o", type=click.Path(path_type=Path), default=None)
@click.option("--start", default=1, help="시작 인덱스")
@click.option("--end", default=None, type=int, help="끝 인덱스")
@click.option("--reverse", is_flag=True, help="역순 다운로드")
def download_playlist(
    url: str,
    quality: str,
    output: Path | None,
    start: int,
    end: int | None,
    reverse: bool,
) -> None:
    """재생목록 다운로드
    
    예시:
        ytdl download-playlist <PLAYLIST_URL>
        ytdl download-playlist <URL> --start 5 --end 10
        ytdl download-playlist <URL> --reverse
    """
    from .models import PlaylistDownloadOptions
    
    # 옵션 설정
    download_options = DownloadOptions(
        quality=quality,
        output_dir=output or settings.download.output_dir,
    )
    
    playlist_options = PlaylistDownloadOptions(
        start_index=start,
        end_index=end,
        reverse=reverse,
    )
    
    downloader = Downloader(download_options)
    results = downloader.download_playlist(url, playlist_options)
    
    # 결과 요약
    success_count = sum(1 for r in results if r.success)
    console.print(f"\n[green]✓ 완료: {success_count}/{len(results)}개 다운로드 성공[/green]")
```

---

## 🎵 2. 오디오 다운로드 개선

### 2.1 오디오 옵션 모델

**파일: `src/youtube_downloader/models.py`**

```python
class AudioOptions(BaseModel):
    """오디오 다운로드 옵션"""
    
    format: str = Field(default="mp3", description="오디오 포맷 (mp3, aac, flac)")
    bitrate: str = Field(default="192", description="비트레이트 (128, 192, 320)")
    embed_thumbnail: bool = Field(default=True, description="앨범 아트 임베딩")
    add_metadata: bool = Field(default=True, description="ID3 태그 추가")
```

### 2.2 오디오 다운로더 구현

**파일: `src/youtube_downloader/downloader.py`**

```python
def download_audio(
    self,
    url: str,
    audio_options: Optional[AudioOptions] = None,
    progress_callback: Optional[Callable[[dict[str, Any]], None]] = None
) -> DownloadResult:
    """
    오디오 전용 다운로드 (개선된 버전)
    
    Args:
        url: 유튜브 동영상 URL
        audio_options: 오디오 옵션
        progress_callback: 진행률 콜백
        
    Returns:
        다운로드 결과
    """
    audio_opts = audio_options or AudioOptions()
    
    try:
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": str(self.options.output_dir / "%(title)s.%(ext)s"),
            "quiet": True,
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": audio_opts.format,
                "preferredquality": audio_opts.bitrate,
            }],
        }
        
        # 메타데이터 추가
        if audio_opts.add_metadata:
            ydl_opts["postprocessors"].append({
                "key": "FFmpegMetadata",
                "add_metadata": True,
            })
        
        # 썸네일 임베딩
        if audio_opts.embed_thumbnail:
            ydl_opts["writethumbnail"] = True
            ydl_opts["postprocessors"].append({
                "key": "EmbedThumbnail",
            })
        
        if progress_callback:
            ydl_opts["progress_hooks"] = [progress_callback]
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            if info is None:
                return DownloadResult(success=False, error_message="동영상 정보를 가져올 수 없습니다.")
            
            video_info = self._extract_video_info(info)
            
            console.print(f"[cyan]오디오 다운로드: {video_info.title}[/cyan]")
            ydl.download([url])
            
            file_path = self._find_downloaded_file(video_info.title, [f".{audio_opts.format}"])
            
            return DownloadResult(
                success=True,
                video_info=video_info,
                file_path=file_path
            )
            
    except Exception as e:
        return DownloadResult(success=False, error_message=str(e))
```

### 2.3 CLI 명령어

```python
@cli.command()
@click.argument("url")
@click.option("--format", "-f", default="mp3", type=click.Choice(["mp3", "aac", "flac"]))
@click.option("--bitrate", "-b", default="192", type=click.Choice(["128", "192", "320"]))
@click.option("--no-thumbnail", is_flag=True, help="썸네일 임베딩 안함")
def download_audio(url: str, format: str, bitrate: str, no_thumbnail: bool) -> None:
    """고품질 오디오 다운로드
    
    예시:
        ytdl download-audio <URL>
        ytdl download-audio <URL> --format flac --bitrate 320
    """
    from .models import AudioOptions
    
    audio_options = AudioOptions(
        format=format,
        bitrate=bitrate,
        embed_thumbnail=not no_thumbnail,
    )
    
    downloader = Downloader()
    result = downloader.download_audio(url, audio_options)
    
    if result.success:
        console.print(f"\n[green]✓ 오디오 다운로드 완료![/green]")
        if result.file_path:
            console.print(f"[cyan]저장 위치: {result.file_path}[/cyan]")
```

---

## 📝 3. 메타데이터 관리 개선

### 3.1 확장된 메타데이터 모델

**파일: `src/youtube_downloader/models.py`**

```python
class ExtendedMetadata(BaseModel):
    """확장된 메타데이터"""
    
    video_info: VideoInfo
    subtitles: List[str] = Field(default_factory=list, description="사용 가능한 자막 언어")
    chapters: List[dict] = Field(default_factory=list, description="챕터 정보")
    tags: List[str] = Field(default_factory=list, description="태그")
    categories: List[str] = Field(default_factory=list, description="카테고리")
    download_date: datetime = Field(default_factory=datetime.now)
```

### 3.2 자막 다운로드

```python
def download_with_subtitles(
    self,
    url: str,
    subtitle_langs: List[str] = ["ko", "en"],
) -> DownloadResult:
    """
    자막과 함께 다운로드
    
    Args:
        url: 동영상 URL
        subtitle_langs: 다운로드할 자막 언어 리스트
    """
    ydl_opts = self._build_ydl_options(None)
    ydl_opts.update({
        "writesubtitles": True,
        "writeautomaticsub": True,
        "subtitleslangs": subtitle_langs,
        "subtitlesformat": "srt",
    })
    
    # 다운로드 실행...
```

### 3.3 다운로드 이력 관리

**파일: `src/youtube_downloader/history.py`** (새 파일)

```python
"""다운로드 이력 관리"""

import json
from pathlib import Path
from datetime import datetime
from typing import List, Optional
from .models import VideoInfo, DownloadResult

class DownloadHistory:
    """다운로드 이력 관리 클래스"""
    
    def __init__(self, history_file: Path = Path(".ytdl_history.json")):
        self.history_file = history_file
        self._load_history()
    
    def _load_history(self) -> None:
        """이력 파일 로드"""
        if self.history_file.exists():
            with open(self.history_file, "r", encoding="utf-8") as f:
                self.history = json.load(f)
        else:
            self.history = []
    
    def add_download(self, result: DownloadResult) -> None:
        """다운로드 기록 추가"""
        if result.success and result.video_info:
            record = {
                "url": result.video_info.url,
                "title": result.video_info.title,
                "download_date": datetime.now().isoformat(),
                "file_path": str(result.file_path) if result.file_path else None,
            }
            self.history.append(record)
            self._save_history()
    
    def _save_history(self) -> None:
        """이력 파일 저장"""
        with open(self.history_file, "w", encoding="utf-8") as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)
    
    def is_downloaded(self, url: str) -> bool:
        """이미 다운로드했는지 확인"""
        return any(record["url"] == url for record in self.history)
    
    def get_recent(self, limit: int = 10) -> List[dict]:
        """최근 다운로드 기록 조회"""
        return self.history[-limit:]
```

### 3.4 CLI 명령어

```python
@cli.command()
@click.option("--limit", "-n", default=10, help="표시할 개수")
def history(limit: int) -> None:
    """다운로드 이력 조회
    
    예시:
        ytdl history
        ytdl history --limit 20
    """
    from .history import DownloadHistory
    from rich.table import Table
    
    hist = DownloadHistory()
    recent = hist.get_recent(limit)
    
    if not recent:
        console.print("[yellow]다운로드 이력이 없습니다.[/yellow]")
        return
    
    table = Table(title=f"최근 다운로드 이력 ({len(recent)}개)")
    table.add_column("날짜", style="cyan")
    table.add_column("제목", style="green")
    table.add_column("경로", style="yellow")
    
    for record in reversed(recent):
        date = record["download_date"][:10]
        title = record["title"][:50]
        path = record.get("file_path", "N/A")
        table.add_row(date, title, path)
    
    console.print(table)
```

---

## ⚡ 4. 추가 편의 기능

### 4.1 동시 다운로드

```python
from concurrent.futures import ThreadPoolExecutor, as_completed

def download_multiple(
    self,
    urls: List[str],
    max_workers: int = 3,
) -> List[DownloadResult]:
    """
    여러 동영상 동시 다운로드
    
    Args:
        urls: 동영상 URL 리스트
        max_workers: 최대 동시 다운로드 수
    """
    results = []
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(self.download, url): url for url in urls}
        
        for future in as_completed(futures):
            url = futures[future]
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                console.print(f"[red]{url} 다운로드 실패: {e}[/red]")
    
    return results
```

### 4.2 파일명 자동 정리

```python
def sanitize_and_format_filename(title: str, max_length: int = 100) -> str:
    """
    파일명 정리 및 포맷팅
    
    - 특수문자 제거
    - 길이 제한
    - 공백 정리
    """
    # 특수문자 제거
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        title = title.replace(char, "")
    
    # 연속 공백 제거
    title = " ".join(title.split())
    
    # 길이 제한
    if len(title) > max_length:
        title = title[:max_length].rsplit(" ", 1)[0]
    
    return title.strip()
```

---

## 📊 구현 우선순위

### High Priority (먼저 구현)
1. ✅ 재생목록 다운로드 - 가장 많이 요청되는 기능
2. ✅ 오디오 품질 개선 - 사용자 경험 향상
3. ✅ 다운로드 이력 관리 - 중복 다운로드 방지

### Medium Priority
4. 자막 다운로드
5. 동시 다운로드
6. 파일명 자동 정리

### Low Priority
7. 다운로드 재개 기능
8. 완료 알림
9. 챕터 정보 추출

---

## 🧪 테스트 계획

### 단위 테스트

**파일: `tests/test_playlist.py`**

```python
def test_playlist_download_options():
    """재생목록 옵션 테스트"""
    options = PlaylistDownloadOptions(
        start_index=5,
        end_index=10,
        reverse=True,
    )
    assert options.start_index == 5
    assert options.end_index == 10
    assert options.reverse is True

@pytest.mark.integration
def test_download_playlist(test_output_dir):
    """재생목록 다운로드 통합 테스트"""
    # 실제 재생목록 URL로 테스트
    pass
```

**파일: `tests/test_audio.py`**

```python
def test_audio_options():
    """오디오 옵션 테스트"""
    options = AudioOptions(
        format="flac",
        bitrate="320",
        embed_thumbnail=True,
    )
    assert options.format == "flac"
    assert options.bitrate == "320"
```

**파일: `tests/test_history.py`**

```python
def test_download_history(tmp_path):
    """다운로드 이력 테스트"""
    history_file = tmp_path / "test_history.json"
    history = DownloadHistory(history_file)
    
    # 기록 추가 테스트
    # 중복 확인 테스트
    # 최근 기록 조회 테스트
```

---

## 📚 문서 업데이트

구현 완료 후 다음 문서들을 업데이트해야 합니다:

1. **README.md** - 새로운 명령어 사용법 추가
2. **사용자 가이드** - 고급 기능 사용 예시
3. **개발 가이드** - 새로운 모듈 설명
4. **작업 계획서** - Phase 3 완료 체크

---

## 🚀 배포 전 체크리스트

- [ ] 모든 테스트 통과
- [ ] 코드 품질 검사 (Ruff, Mypy)
- [ ] 문서 업데이트
- [ ] CHANGELOG 작성
- [ ] 버전 업데이트 (0.1.0 → 0.2.0)
- [ ] Git 태그 생성
- [ ] PyPI 배포 (선택사항)
