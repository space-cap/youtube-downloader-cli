"""데이터 모델 정의"""

from datetime import datetime
from pathlib import Path

from pydantic import BaseModel, Field


class VideoInfo(BaseModel):
    """동영상 정보 모델"""

    url: str
    title: str
    duration: int = Field(description="동영상 길이 (초)")
    uploader: str
    upload_date: datetime | None = None
    thumbnail_url: str | None = None
    description: str | None = None


class DownloadOptions(BaseModel):
    """다운로드 옵션 모델"""

    quality: str = Field(default="best", description="화질 설정")
    output_dir: Path = Field(default=Path("./downloads"), description="출력 디렉토리")
    audio_only: bool = Field(default=False, description="오디오만 다운로드")
    audio_quality: str = Field(default="192", description="오디오 비트레이트 (kbps)")
    save_metadata: bool = Field(default=False, description="메타데이터 저장")
    save_thumbnail: bool = Field(default=False, description="썸네일 저장")


class DownloadResult(BaseModel):
    """다운로드 결과 모델"""

    success: bool
    video_info: VideoInfo | None = None
    file_path: Path | None = None
    error_message: str | None = None
