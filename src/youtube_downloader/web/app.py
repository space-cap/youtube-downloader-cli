"""FastAPI 애플리케이션"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

from . import __version__

# FastAPI 앱 생성
app = FastAPI(
    title="YouTube Downloader API",
    description="YouTube 동영상 다운로드 웹 API",
    version=__version__,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 프로덕션에서는 특정 도메인만 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API 라우터 등록
from .api import router as api_router
from .auth_api import router as auth_router
from .credit_api import router as credit_router

app.include_router(auth_router)
app.include_router(credit_router)
app.include_router(api_router)

# 정적 파일 서빙 설정
static_dir = Path(__file__).parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


@app.get("/")
async def root():
    """루트 엔드포인트 - HTML 페이지 반환"""
    from fastapi.responses import FileResponse
    
    html_path = Path(__file__).parent / "static" / "index.html"
    if html_path.exists():
        return FileResponse(html_path)
    
    return {
        "message": "YouTube Downloader API",
        "version": __version__,
        "docs": "/docs",
    }


@app.get("/health")
async def health_check():
    """헬스 체크 엔드포인트"""
    return {"status": "healthy"}


# WebSocket 엔드포인트
@app.websocket("/ws/download/{task_id}")
async def websocket_endpoint(websocket: WebSocket, task_id: str):
    """
    WebSocket 엔드포인트
    
    실시간 다운로드 진행률을 클라이언트에 전송합니다.
    """
    from .websocket import manager
    
    await manager.connect(task_id, websocket)
    
    try:
        # 연결 유지 (클라이언트로부터 메시지 수신 대기)
        while True:
            data = await websocket.receive_text()
            # 클라이언트로부터 메시지를 받을 수 있지만, 현재는 사용하지 않음
            # 필요시 ping/pong 메시지 처리 가능
    except WebSocketDisconnect:
        manager.disconnect(task_id)


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
