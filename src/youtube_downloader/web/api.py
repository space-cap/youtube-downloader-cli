"""API 라우터"""

from fastapi import APIRouter, HTTPException, Query, BackgroundTasks
from fastapi.responses import FileResponse
from typing import Optional
from pathlib import Path
import yt_dlp

from .models import (
    VideoInfoResponse,
    VideoInfo,
    VideoFormats,
    FormatInfo,
    ErrorResponse,
    ErrorDetail,
    DownloadRequest,
    DownloadResponse,
    DownloadStatusResponse,
    DownloadStatusData,
    DownloadProgress,
    DownloadFileInfo,
)
from .tasks import task_manager
from ..downloader import Downloader
from ..models import DownloadOptions as CLIDownloadOptions

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


@router.post(
    "/download",
    response_model=DownloadResponse,
    status_code=202,
    responses={
        400: {"model": ErrorResponse, "description": "잘못된 요청"},
        429: {"model": ErrorResponse, "description": "요청 제한 초과"},
    },
)
async def start_download(request: DownloadRequest, background_tasks: BackgroundTasks):
    """
    다운로드 시작
    
    백그라운드에서 다운로드를 시작하고 task_id를 반환합니다.
    """
    try:
        # Task 생성
        task_id = task_manager.create_task(
            url=str(request.url),
            options=request.options.model_dump()
        )
        
        # 백그라운드 작업 추가
        background_tasks.add_task(
            download_task,
            task_id=task_id,
            url=str(request.url),
            options=request.options
        )
        
        task = task_manager.get_task(task_id)
        
        return DownloadResponse(
            success=True,
            data={
                "task_id": task_id,
                "status": "pending",
                "created_at": task["created_at"].isoformat(),
            }
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "code": "INTERNAL_ERROR",
                "message": f"다운로드 시작 실패: {str(e)}",
            }
        )


@router.get(
    "/download/{task_id}/status",
    response_model=DownloadStatusResponse,
    responses={
        404: {"model": ErrorResponse, "description": "작업을 찾을 수 없음"},
    },
)
async def get_download_status(task_id: str):
    """다운로드 상태 조회"""
    task = task_manager.get_task(task_id)
    
    if not task:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "TASK_NOT_FOUND",
                "message": "작업을 찾을 수 없습니다.",
            }
        )
    
    # 응답 데이터 구성
    status_data = DownloadStatusData(
        task_id=task["task_id"],
        status=task["status"],
        progress=DownloadProgress(**task["progress"]) if task["progress"] else None,
        video_info=VideoInfo(**task["video_info"]) if task["video_info"] else None,
        file=DownloadFileInfo(
            filename=Path(task["file_path"]).name,
            size=Path(task["file_path"]).stat().st_size,
            download_url=f"/api/v1/download/{task_id}/file"
        ) if task["file_path"] and task["status"] == "completed" else None,
        created_at=task["created_at"],
        completed_at=task.get("completed_at"),
        failed_at=task.get("failed_at"),
        error=task.get("error"),
    )
    
    return DownloadStatusResponse(success=True, data=status_data)


@router.get(
    "/download/{task_id}/file",
    responses={
        404: {"model": ErrorResponse, "description": "파일을 찾을 수 없음"},
    },
)
async def download_file(task_id: str):
    """파일 다운로드"""
    task = task_manager.get_task(task_id)
    
    if not task:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "TASK_NOT_FOUND",
                "message": "작업을 찾을 수 없습니다.",
            }
        )
    
    if task["status"] != "completed" or not task["file_path"]:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "FILE_NOT_FOUND",
                "message": "파일을 찾을 수 없습니다. 다운로드가 완료되지 않았거나 파일이 만료되었습니다.",
            }
        )
    
    file_path = Path(task["file_path"])
    
    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail={
                "code": "FILE_NOT_FOUND",
                "message": "파일이 존재하지 않습니다.",
            }
        )
    
    return FileResponse(
        path=str(file_path),
        filename=file_path.name,
        media_type="application/octet-stream",
    )


def download_task(task_id: str, url: str, options):
    """
    백그라운드 다운로드 작업
    
    Args:
        task_id: 작업 ID
        url: 유튜브 URL
        options: 다운로드 옵션
    """
    import asyncio
    from .websocket import (
        send_progress_update,
        send_status_update,
        send_complete_message,
        send_error_message,
    )
    
    # 비동기 함수를 동기 컨텍스트에서 실행하기 위한 헬퍼
    def run_async(coro):
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        if loop.is_running():
            # 이미 실행 중인 루프가 있으면 태스크 생성
            asyncio.create_task(coro)
        else:
            # 루프가 없으면 실행
            loop.run_until_complete(coro)
    
    try:
        # 상태 업데이트: downloading
        task_manager.update_task_status(task_id, "downloading")
        run_async(send_status_update(task_id, "downloading", "다운로드를 시작합니다..."))
        
        # CLI Downloader 옵션 변환
        cli_options = CLIDownloadOptions(
            quality=options.quality,
            output_dir=task_manager.output_dir,
            audio_only=options.audio_only,
            audio_quality=options.audio_quality,
            save_metadata=options.save_metadata,
            save_thumbnail=options.save_thumbnail,
        )
        
        # Downloader 생성
        downloader = Downloader(cli_options)
        
        # 진행률 콜백
        def progress_callback(d: dict):
            if d["status"] == "downloading":
                downloaded = d.get("downloaded_bytes", 0)
                total = d.get("total_bytes") or d.get("total_bytes_estimate", 0)
                
                if total > 0:
                    percentage = int((downloaded / total) * 100)
                    
                    # TaskManager 업데이트
                    task_manager.update_task_progress(
                        task_id=task_id,
                        percentage=percentage,
                        downloaded_bytes=downloaded,
                        total_bytes=total,
                        speed=d.get("_speed_str", ""),
                        eta=d.get("_eta_str", ""),
                    )
                    
                    # WebSocket으로 진행률 전송
                    run_async(send_progress_update(
                        task_id=task_id,
                        percentage=percentage,
                        downloaded_bytes=downloaded,
                        total_bytes=total,
                        speed=d.get("_speed_str", ""),
                        eta=d.get("_eta_str", ""),
                    ))
        
        # 다운로드 실행
        result = downloader.download(url, progress_callback)
        
        if result.success:
            # 처리 중 상태
            task_manager.update_task_status(task_id, "processing")
            run_async(send_status_update(task_id, "processing", "파일 처리 중..."))
            
            # 동영상 정보 저장
            if result.video_info:
                task_manager.set_task_video_info(
                    task_id,
                    result.video_info.model_dump()
                )
            
            # 파일 경로 저장
            if result.file_path:
                task_manager.set_task_file_path(task_id, result.file_path)
            
            # 작업 완료
            task_manager.complete_task(task_id)
            
            # WebSocket으로 완료 메시지 전송
            if result.file_path:
                from pathlib import Path
                file_path = Path(result.file_path)
                run_async(send_complete_message(
                    task_id=task_id,
                    filename=file_path.name,
                    size=file_path.stat().st_size if file_path.exists() else 0,
                    download_url=f"/api/v1/download/{task_id}/file"
                ))
        else:
            # 작업 실패
            error_msg = result.error_message or "다운로드 실패"
            task_manager.fail_task(
                task_id,
                {
                    "code": "DOWNLOAD_FAILED",
                    "message": error_msg,
                }
            )
            
            # WebSocket으로 에러 메시지 전송
            run_async(send_error_message(
                task_id=task_id,
                error_code="DOWNLOAD_FAILED",
                error_message=error_msg
            ))
    
    except Exception as e:
        # 예외 발생 시 실패 처리
        error_msg = str(e)
        task_manager.fail_task(
            task_id,
            {
                "code": "DOWNLOAD_FAILED",
                "message": error_msg,
            }
        )
        
        # WebSocket으로 에러 메시지 전송
        run_async(send_error_message(
            task_id=task_id,
            error_code="DOWNLOAD_FAILED",
            error_message=error_msg
        ))


