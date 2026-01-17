"""API 라우터"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional
import yt_dlp

from .models import (
    VideoInfoResponse,
    VideoInfo,
    VideoFormats,
    FormatInfo,
    ErrorResponse,
    ErrorDetail,
)

# API 라우터 생성
router = APIRouter(prefix="/api/v1", tags=["api"])


@router.get("/version")
async def get_version():
    """API 버전 정보"""
    from . import __version__
    return {
        "version": __version__,
        "api_version": "v1",
    }


@router.get(
    "/video/info",
    response_model=VideoInfoResponse,
    responses={
        400: {"model": ErrorResponse, "description": "잘못된 URL"},
        404: {"model": ErrorResponse, "description": "동영상을 찾을 수 없음"},
        500: {"model": ErrorResponse, "description": "서버 오류"},
    },
)
async def get_video_info(url: str = Query(..., description="유튜브 동영상 URL")):
    """
    동영상 정보 조회
    
    유튜브 URL로부터 동영상 정보를 가져옵니다.
    """
    try:
        # URL 유효성 검사
        if not url or not ("youtube.com" in url or "youtu.be" in url):
            raise HTTPException(
                status_code=400,
                detail={
                    "code": "INVALID_URL",
                    "message": "유효하지 않은 유튜브 URL입니다.",
                }
            )
        
        # yt-dlp 옵션 설정
        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            "extract_flat": False,
        }
        
        # 동영상 정보 추출
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            if info is None:
                raise HTTPException(
                    status_code=404,
                    detail={
                        "code": "VIDEO_NOT_FOUND",
                        "message": "동영상을 찾을 수 없습니다.",
                    }
                )
            
            # 포맷 정보 파싱
            video_formats = []
            audio_formats = []
            
            for fmt in info.get("formats", []):
                format_info = FormatInfo(
                    format_id=fmt.get("format_id", ""),
                    ext=fmt.get("ext", ""),
                    quality=fmt.get("format_note", "") or fmt.get("resolution", "audio only"),
                    filesize=fmt.get("filesize"),
                )
                
                # 비디오 포맷과 오디오 포맷 분류
                if fmt.get("vcodec") != "none":
                    video_formats.append(format_info)
                elif fmt.get("acodec") != "none":
                    audio_formats.append(format_info)
            
            # 응답 데이터 구성
            video_info = VideoInfo(
                url=info.get("webpage_url", url),
                title=info.get("title", "Unknown"),
                duration=info.get("duration", 0),
                uploader=info.get("uploader", "Unknown"),
                thumbnail=info.get("thumbnail"),
                description=info.get("description"),
                formats=VideoFormats(
                    video=video_formats[:10],  # 상위 10개만
                    audio=audio_formats[:5],   # 상위 5개만
                ),
            )
            
            return VideoInfoResponse(success=True, data=video_info)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "code": "INTERNAL_ERROR",
                "message": f"서버 오류가 발생했습니다: {str(e)}",
            }
        )
