"""유튜브 동영상 다운로더"""

import json
from collections.abc import Callable
from pathlib import Path
from typing import Any

import yt_dlp
from rich.console import Console

from .models import DownloadOptions, DownloadResult, VideoInfo
from .utils import ensure_directory, sanitize_filename

console = Console()


class Downloader:
    """유튜브 동영상 다운로더"""

    def __init__(self, options: DownloadOptions | None = None):
        """
        다운로더 초기화

        Args:
            options: 다운로드 옵션
        """
        self.options = options or DownloadOptions()
        ensure_directory(self.options.output_dir)

    def download(self, url: str, progress_callback: Callable[[dict[str, Any]], None] | None = None) -> DownloadResult:
        """
        동영상 다운로드

        Args:
            url: 유튜브 동영상 URL
            progress_callback: 진행률 콜백 함수

        Returns:
            다운로드 결과
        """
        try:
            # yt-dlp 옵션 설정
            ydl_opts = self._build_ydl_options(progress_callback)

            # 동영상 정보 추출
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                if info is None:
                    return DownloadResult(
                        success=False,
                        error_message="동영상 정보를 가져올 수 없습니다."
                    )

                video_info = self._extract_video_info(info)

                # 다운로드 실행
                console.print(f"[cyan]다운로드 시작: {video_info.title}[/cyan]")
                ydl.download([url])

                # 파일 경로 찾기
                file_path = self._find_downloaded_file(video_info.title)

                # 메타데이터 저장
                if self.options.save_metadata:
                    self._save_metadata(video_info, file_path)

                return DownloadResult(
                    success=True,
                    video_info=video_info,
                    file_path=file_path
                )

        except Exception as e:
            console.print(f"[red]에러 발생: {str(e)}[/red]")
            return DownloadResult(
                success=False,
                error_message=str(e)
            )

    def _build_ydl_options(self, progress_callback: Callable[[dict[str, Any]], None] | None) -> dict[str, Any]:
        """yt-dlp 옵션 빌드"""
        opts: dict[str, Any] = {
            "outtmpl": str(self.options.output_dir / "%(title)s.%(ext)s"),
            "quiet": True,
            "no_warnings": True,
        }

        # 포맷 설정
        if self.options.audio_only:
            opts["format"] = "bestaudio/best"
            opts["postprocessors"] = [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }]
        else:
            if self.options.quality == "best":
                opts["format"] = "bestvideo+bestaudio/best"
            else:
                opts["format"] = f"bestvideo[height<={self.options.quality.rstrip('p')}]+bestaudio/best"

        # 썸네일 저장
        if self.options.save_thumbnail:
            opts["writethumbnail"] = True

        # 진행률 콜백
        if progress_callback:
            opts["progress_hooks"] = [progress_callback]

        return opts

    def _extract_video_info(self, info: dict[str, Any]) -> VideoInfo:
        """동영상 정보 추출"""
        return VideoInfo(
            url=info.get("webpage_url", ""),
            title=info.get("title", "Unknown"),
            duration=info.get("duration", 0),
            uploader=info.get("uploader", "Unknown"),
            thumbnail_url=info.get("thumbnail"),
            description=info.get("description"),
        )

    def _find_downloaded_file(self, title: str) -> Path | None:
        """다운로드된 파일 찾기"""
        safe_title = sanitize_filename(title)

        # 가능한 확장자들
        extensions = [".mp4", ".webm", ".mkv", ".mp3", ".m4a"]

        for ext in extensions:
            file_path = self.options.output_dir / f"{safe_title}{ext}"
            if file_path.exists():
                return file_path

        # 정확한 매칭이 안되면 디렉토리에서 검색
        for file in self.options.output_dir.iterdir():
            if file.is_file() and safe_title in file.stem:
                return file

        return None

    def _save_metadata(self, video_info: VideoInfo, file_path: Path | None) -> None:
        """메타데이터 JSON 파일로 저장"""
        if file_path:
            metadata_path = file_path.with_suffix(".info.json")
            with open(metadata_path, "w", encoding="utf-8") as f:
                json.dump(video_info.model_dump(), f, ensure_ascii=False, indent=2, default=str)
            console.print(f"[green]메타데이터 저장: {metadata_path.name}[/green]")
