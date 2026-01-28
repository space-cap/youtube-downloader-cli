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


def get_ffmpeg_path() -> str:
    """ffmpeg 실행 파일 경로 반환"""
    import shutil
    import imageio_ffmpeg  # type: ignore

    if shutil.which("ffmpeg"):
        return "ffmpeg"
    try:
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        raise RuntimeError("ffmpeg를 찾을 수 없습니다.")


def trim_audio(
    input_path: Path,
    output_path: Path,
    start: str | None = None,
    end: str | None = None,
) -> None:
    """
    오디오 파일 자르기

    Args:
        input_path: 입력 파일 경로
        output_path: 출력 파일 경로
        start: 시작 시간 (HH:MM:SS 또는 초)
        end: 종료 시간 (HH:MM:SS 또는 초)
    """
    import subprocess

    ffmpeg_path = get_ffmpeg_path()
    
    # -ss 옵션은 입력 파일(-i) 앞에 두는 것이 더 빠름 (input seeking)
    # 하지만 정확도를 위해 재인코딩이 필요할 수 있음. 
    # mp3의 경우 copy가 빠르고 보통 무난함.
    # 여기서는 input seeking을 사용하되 -c copy로 빠르게 처리
    
    cmd = [ffmpeg_path]
    
    if start:
        cmd.extend(["-ss", start])
        
    if end:
        cmd.extend(["-to", end])

    cmd.extend(["-i", str(input_path)])
    
    # 오디오 코덱 복사
    cmd.extend(["-c", "copy", str(output_path)])
    
    # 기존 파일 덮어쓰기 허용
    cmd.append("-y")

    try:
        subprocess.run(cmd, check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.decode() if e.stderr else str(e)
        raise RuntimeError(f"ffmpeg 실행 실패: {error_msg}")
