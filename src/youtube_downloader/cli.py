"""CLI 인터페이스"""

from pathlib import Path

import click
from rich.console import Console
from rich.progress import (
    BarColumn,
    DownloadColumn,
    Progress,
    TextColumn,
    TimeRemainingColumn,
    TransferSpeedColumn,
)

from . import __version__
from .config import settings
from .downloader import Downloader
from .models import DownloadOptions

console = Console()


@click.group()
@click.version_option(version=__version__)
def cli() -> None:
    """🎥 유튜브 다운로더 CLI

    유튜브 동영상을 간편하게 다운로드하는 명령줄 도구입니다.
    """
    pass


@cli.command()
@click.argument("url")
@click.option(
    "--quality",
    "-q",
    default="best",
    help="화질 선택 (best, 1080p, 720p, 480p 등)",
)
@click.option(
    "--output",
    "-o",
    type=click.Path(path_type=Path),
    default=None,
    help="출력 디렉토리",
)
@click.option(
    "--audio-only",
    is_flag=True,
    help="오디오만 다운로드 (MP3)",
)
@click.option(
    "--metadata",
    is_flag=True,
    help="메타데이터 저장",
)
@click.option(
    "--thumbnail",
    is_flag=True,
    help="썸네일 저장",
)
def download(
    url: str,
    quality: str,
    output: Path | None,
    audio_only: bool,
    metadata: bool,
    thumbnail: bool,
) -> None:
    """동영상 다운로드

    예시:
        ytdl download https://www.youtube.com/watch?v=...
        ytdl download <URL> --quality 1080p
        ytdl download <URL> --audio-only
    """
    # 옵션 설정
    options = DownloadOptions(
        quality=quality,
        output_dir=output or settings.download.output_dir,
        audio_only=audio_only,
        save_metadata=metadata,
        save_thumbnail=thumbnail,
    )

    # 다운로더 생성
    downloader = Downloader(options)

    # 진행률 표시를 위한 Progress 설정
    with Progress(
        TextColumn("[bold blue]{task.description}"),
        BarColumn(),
        DownloadColumn(),
        TransferSpeedColumn(),
        TimeRemainingColumn(),
        console=console,
    ) as progress:
        task_id = progress.add_task("다운로드 중...", total=None)

        def progress_callback(d: dict) -> None:
            """진행률 콜백"""
            if d["status"] == "downloading":
                downloaded = d.get("downloaded_bytes", 0)
                total = d.get("total_bytes") or d.get("total_bytes_estimate")
                
                if total:
                    progress.update(task_id, completed=downloaded, total=total)
                else:
                    progress.update(task_id, completed=downloaded)
                    
            elif d["status"] == "finished":
                if "total_bytes" in d:
                    progress.update(task_id, completed=d["total_bytes"], total=d["total_bytes"])
                else:
                    progress.update(task_id, completed=100, total=100)

        def message_callback(msg: str) -> None:
            """메시지 출력 콜백"""
            progress.console.print(msg)

        # 다운로드 실행
        result = downloader.download(url, progress_callback, message_callback)

        if result.success:
            console.print("\n[green]✓ 다운로드 완료![/green]")
            if result.file_path:
                console.print(f"[cyan]저장 위치: {result.file_path}[/cyan]")
        else:
            console.print(f"\n[red]✗ 다운로드 실패: {result.error_message}[/red]")
            raise click.Abort()


@cli.command()
@click.argument("url")
def list_formats(url: str) -> None:
    """사용 가능한 포맷 목록 표시

    예시:
        ytdl list-formats https://www.youtube.com/watch?v=...
    """
    import yt_dlp

    console.print("[cyan]포맷 정보 가져오는 중...[/cyan]")

    try:
        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            if info is None:
                console.print("[red]동영상 정보를 가져올 수 없습니다.[/red]")
                raise click.Abort()

            console.print(f"\n[bold]제목:[/bold] {info.get('title', 'Unknown')}")
            console.print(f"[bold]업로더:[/bold] {info.get('uploader', 'Unknown')}\n")

            # 포맷 테이블 출력
            from rich.table import Table

            table = Table(title="사용 가능한 포맷")
            table.add_column("Format ID", style="cyan")
            table.add_column("Extension", style="magenta")
            table.add_column("Resolution", style="green")
            table.add_column("Note", style="yellow")

            formats = info.get("formats", [])
            for fmt in formats:
                format_id = fmt.get("format_id", "")
                ext = fmt.get("ext", "")
                resolution = fmt.get("resolution", "audio only")
                note = fmt.get("format_note", "")

                table.add_row(format_id, ext, resolution, note)

            console.print(table)

    except Exception as e:
        console.print(f"[red]에러 발생: {str(e)}[/red]")
        raise click.Abort() from None


@cli.group()
def config() -> None:
    """설정 관리

    예시:
        ytdl config show
        ytdl config set output_dir ~/Videos
    """
    pass


@config.command()
def show() -> None:
    """현재 설정 표시"""
    from rich.table import Table

    table = Table(title="현재 설정")
    table.add_column("설정", style="cyan")
    table.add_column("값", style="green")

    table.add_row("기본 화질", settings.download.quality)
    table.add_row("출력 디렉토리", str(settings.download.output_dir))
    table.add_row("오디오만", "예" if settings.download.audio_only else "아니오")
    table.add_row("메타데이터 저장", "예" if settings.download.save_metadata else "아니오")
    table.add_row("썸네일 저장", "예" if settings.download.save_thumbnail else "아니오")

    console.print(table)


def main() -> None:
    """CLI 진입점"""
    cli()


if __name__ == "__main__":
    main()
