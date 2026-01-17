"""작업 관리 시스템"""

import uuid
from datetime import datetime
from typing import Dict, Optional
from pathlib import Path

from .models import DownloadStatusData, DownloadProgress, VideoInfo


class TaskManager:
    """다운로드 작업 관리자"""
    
    def __init__(self):
        # 작업 저장소 (in-memory)
        self.tasks: Dict[str, Dict] = {}
        
        # 임시 파일 저장 경로
        self.temp_dir = Path("./downloads/temp")
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        
        # 완료된 파일 저장 경로
        self.output_dir = Path("./downloads")
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def create_task(self, url: str, options: dict) -> str:
        """
        새로운 다운로드 작업 생성
        
        Args:
            url: 유튜브 URL
            options: 다운로드 옵션
            
        Returns:
            task_id: 생성된 작업 ID
        """
        task_id = str(uuid.uuid4())
        
        self.tasks[task_id] = {
            "task_id": task_id,
            "url": url,
            "options": options,
            "status": "pending",
            "progress": None,
            "video_info": None,
            "file_path": None,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "completed_at": None,
            "failed_at": None,
            "error": None,
        }
        
        return task_id
    
    def get_task(self, task_id: str) -> Optional[Dict]:
        """
        작업 정보 조회
        
        Args:
            task_id: 작업 ID
            
        Returns:
            작업 정보 또는 None
        """
        return self.tasks.get(task_id)
    
    def update_task_status(self, task_id: str, status: str):
        """작업 상태 업데이트"""
        if task_id in self.tasks:
            self.tasks[task_id]["status"] = status
            self.tasks[task_id]["updated_at"] = datetime.now()
    
    def update_task_progress(
        self,
        task_id: str,
        percentage: int,
        downloaded_bytes: int,
        total_bytes: int,
        speed: Optional[str] = None,
        eta: Optional[str] = None,
    ):
        """진행률 업데이트"""
        if task_id in self.tasks:
            self.tasks[task_id]["progress"] = {
                "percentage": percentage,
                "downloaded_bytes": downloaded_bytes,
                "total_bytes": total_bytes,
                "speed": speed,
                "eta": eta,
            }
            self.tasks[task_id]["updated_at"] = datetime.now()
    
    def set_task_video_info(self, task_id: str, video_info: dict):
        """동영상 정보 설정"""
        if task_id in self.tasks:
            self.tasks[task_id]["video_info"] = video_info
            self.tasks[task_id]["updated_at"] = datetime.now()
    
    def set_task_file_path(self, task_id: str, file_path: Path):
        """파일 경로 설정"""
        if task_id in self.tasks:
            self.tasks[task_id]["file_path"] = str(file_path)
            self.tasks[task_id]["updated_at"] = datetime.now()
    
    def complete_task(self, task_id: str):
        """작업 완료 처리"""
        if task_id in self.tasks:
            self.tasks[task_id]["status"] = "completed"
            self.tasks[task_id]["completed_at"] = datetime.now()
            self.tasks[task_id]["updated_at"] = datetime.now()
    
    def fail_task(self, task_id: str, error: dict):
        """작업 실패 처리"""
        if task_id in self.tasks:
            self.tasks[task_id]["status"] = "failed"
            self.tasks[task_id]["error"] = error
            self.tasks[task_id]["failed_at"] = datetime.now()
            self.tasks[task_id]["updated_at"] = datetime.now()
    
    def delete_task(self, task_id: str):
        """작업 삭제"""
        if task_id in self.tasks:
            # 파일도 함께 삭제
            file_path = self.tasks[task_id].get("file_path")
            if file_path:
                try:
                    Path(file_path).unlink(missing_ok=True)
                except Exception:
                    pass
            
            del self.tasks[task_id]
    
    def get_temp_file_path(self, task_id: str, filename: str) -> Path:
        """임시 파일 경로 생성"""
        return self.temp_dir / f"{task_id}_{filename}"
    
    def get_output_file_path(self, filename: str) -> Path:
        """출력 파일 경로 생성"""
        return self.output_dir / filename


# 전역 TaskManager 인스턴스
task_manager = TaskManager()
