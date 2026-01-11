"""유틸리티 함수"""

from pathlib import Path


def sanitize_filename(filename: str) -> str:
    """
    파일명에서 사용할 수 없는 문자 제거

    Args:
        filename: 원본 파일명

    Returns:
        정제된 파일명
    """
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, "_")
    return filename


def format_duration(seconds: int) -> str:
    """
    초 단위 시간을 HH:MM:SS 형식으로 변환

    Args:
        seconds: 초 단위 시간

    Returns:
        포맷된 시간 문자열
    """
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60

    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"


def format_filesize(bytes_size: int) -> str:
    """
    바이트를 읽기 쉬운 형식으로 변환

    Args:
        bytes_size: 바이트 크기

    Returns:
        포맷된 파일 크기 문자열
    """
    for unit in ["B", "KB", "MB", "GB"]:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.2f} TB"


def ensure_directory(path: Path) -> None:
    """
    디렉토리가 존재하지 않으면 생성

    Args:
        path: 디렉토리 경로
    """
    path.mkdir(parents=True, exist_ok=True)
