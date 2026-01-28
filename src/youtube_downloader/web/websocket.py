"""WebSocket 연결 관리"""

from typing import Dict
from fastapi import WebSocket, WebSocketDisconnect
import json
import asyncio


class ConnectionManager:
    """WebSocket 연결 관리자"""
    
    def __init__(self):
        # task_id별 WebSocket 연결 저장
        self.active_connections: Dict[str, WebSocket] = {}
    
    async def connect(self, task_id: str, websocket: WebSocket):
        """
        WebSocket 연결 수락
        
        Args:
            task_id: 작업 ID
            websocket: WebSocket 연결
        """
        await websocket.accept()
        self.active_connections[task_id] = websocket
        print(f"WebSocket 연결: task_id={task_id}")
    
    def disconnect(self, task_id: str):
        """
        WebSocket 연결 해제
        
        Args:
            task_id: 작업 ID
        """
        if task_id in self.active_connections:
            del self.active_connections[task_id]
            print(f"WebSocket 연결 해제: task_id={task_id}")
    
    async def send_message(self, task_id: str, message: dict):
        """
        특정 task_id에 메시지 전송
        
        Args:
            task_id: 작업 ID
            message: 전송할 메시지 (dict)
        """
        if task_id in self.active_connections:
            try:
                await self.active_connections[task_id].send_text(
                    json.dumps(message, ensure_ascii=False)
                )
            except Exception as e:
                print(f"메시지 전송 실패: {e}")
                self.disconnect(task_id)
    
    async def broadcast(self, message: dict):
        """
        모든 연결에 메시지 브로드캐스트
        
        Args:
            message: 전송할 메시지 (dict)
        """
        disconnected = []
        
        for task_id, connection in self.active_connections.items():
            try:
                await connection.send_text(
                    json.dumps(message, ensure_ascii=False)
                )
            except Exception:
                disconnected.append(task_id)
        
        # 연결 실패한 클라이언트 제거
        for task_id in disconnected:
            self.disconnect(task_id)


# 전역 ConnectionManager 인스턴스
manager = ConnectionManager()


async def send_progress_update(
    task_id: str,
    percentage: int,
    downloaded_bytes: int,
    total_bytes: int,
    speed: str = "",
    eta: str = ""
):
    """
    진행률 업데이트 메시지 전송
    
    Args:
        task_id: 작업 ID
        percentage: 진행률 (0-100)
        downloaded_bytes: 다운로드된 바이트
        total_bytes: 전체 바이트
        speed: 다운로드 속도
        eta: 예상 남은 시간
    """
    message = {
        "type": "progress",
        "data": {
            "percentage": percentage,
            "downloaded_bytes": downloaded_bytes,
            "total_bytes": total_bytes,
            "speed": speed,
            "eta": eta,
        }
    }
    await manager.send_message(task_id, message)


async def send_status_update(task_id: str, status: str, message: str = ""):
    """
    상태 변경 메시지 전송
    
    Args:
        task_id: 작업 ID
        status: 상태 (downloading, processing, etc.)
        message: 상태 메시지
    """
    msg = {
        "type": "status",
        "data": {
            "status": status,
            "message": message,
        }
    }
    await manager.send_message(task_id, msg)


async def send_complete_message(task_id: str, filename: str, size: int, download_url: str):
    """
    완료 메시지 전송
    
    Args:
        task_id: 작업 ID
        filename: 파일명
        size: 파일 크기
        download_url: 다운로드 URL
    """
    message = {
        "type": "complete",
        "data": {
            "filename": filename,
            "size": size,
            "download_url": download_url,
        }
    }
    await manager.send_message(task_id, message)


async def send_error_message(task_id: str, error_code: str, error_message: str):
    """
    에러 메시지 전송
    
    Args:
        task_id: 작업 ID
        error_code: 에러 코드
        error_message: 에러 메시지
    """
    message = {
        "type": "error",
        "data": {
            "code": error_code,
            "message": error_message,
        }
    }
    await manager.send_message(task_id, message)
