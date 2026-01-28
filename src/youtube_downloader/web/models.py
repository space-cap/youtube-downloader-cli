"""Pydantic 모델 정의"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, HttpUrl


# ============================================================================
# Request 모델
# ============================================================================

class VideoInfoRequest(BaseModel):
    """동영상 정보 조회 요청"""
    url: HttpUrl = Field(..., description="유튜브 동영상 URL")


class DownloadOptions(BaseModel):
    """다운로드 옵션"""
    quality: str = Field(default="best", description="화질 (best, 1080p, 720p, 480p)")
    audio_only: bool = Field(default=False, description="오디오만 다운로드")
    audio_quality: str = Field(default="192", description="오디오 비트레이트 (32-320 kbps)")
    save_metadata: bool = Field(default=False, description="메타데이터 저장")
    save_thumbnail: bool = Field(default=False, description="썸네일 저장")


class DownloadRequest(BaseModel):
    """다운로드 시작 요청"""
    url: HttpUrl = Field(..., description="유튜브 동영상 URL")
    options: DownloadOptions = Field(default_factory=DownloadOptions)


# ============================================================================
# Response 모델
# ============================================================================

class FormatInfo(BaseModel):
    """포맷 정보"""
    format_id: str
    ext: str
    quality: str
    filesize: Optional[int] = None


class VideoFormats(BaseModel):
    """사용 가능한 포맷 목록"""
    video: List[FormatInfo] = Field(default_factory=list)
    audio: List[FormatInfo] = Field(default_factory=list)


class VideoInfo(BaseModel):
    """동영상 정보"""
    url: str
    title: str
    duration: int = Field(description="동영상 길이 (초)")
    uploader: str
    thumbnail: Optional[str] = None
    description: Optional[str] = None
    formats: VideoFormats = Field(default_factory=VideoFormats)


class VideoInfoResponse(BaseModel):
    """동영상 정보 조회 응답"""
    success: bool = True
    data: VideoInfo


class DownloadProgress(BaseModel):
    """다운로드 진행률"""
    percentage: int = Field(ge=0, le=100)
    downloaded_bytes: int
    total_bytes: int
    speed: Optional[str] = None
    eta: Optional[str] = None


class DownloadFileInfo(BaseModel):
    """다운로드된 파일 정보"""
    filename: str
    size: int
    download_url: str


class DownloadStatusData(BaseModel):
    """다운로드 상태 데이터"""
    task_id: str
    status: str = Field(description="pending, downloading, processing, completed, failed")
    progress: Optional[DownloadProgress] = None
    video_info: Optional[VideoInfo] = None
    file: Optional[DownloadFileInfo] = None
    created_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    failed_at: Optional[datetime] = None
    error: Optional[Dict[str, Any]] = None


class DownloadResponse(BaseModel):
    """다운로드 시작 응답"""
    success: bool = True
    data: Dict[str, Any] = Field(
        description="task_id, status, created_at 포함"
    )


class DownloadStatusResponse(BaseModel):
    """다운로드 상태 조회 응답"""
    success: bool = True
    data: DownloadStatusData


# ============================================================================
# Error 모델
# ============================================================================

class ErrorDetail(BaseModel):
    """에러 상세 정보"""
    code: str
    message: str
    details: Optional[Dict[str, Any]] = None
    retry_after: Optional[int] = None


class ErrorResponse(BaseModel):
    """에러 응답"""
    success: bool = False
    error: ErrorDetail


# ============================================================================
# WebSocket 메시지 모델
# ============================================================================

class WebSocketMessage(BaseModel):
    """WebSocket 메시지"""
    type: str = Field(description="progress, status, complete, error")
    data: Dict[str, Any]
    timestamp: datetime = Field(default_factory=datetime.now)
