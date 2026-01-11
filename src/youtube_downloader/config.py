"""설정 관리"""

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DownloadSettings(BaseSettings):
    """다운로드 기본 설정"""

    quality: str = Field(default="best", description="기본 화질")
    output_dir: Path = Field(default=Path("./downloads"), description="기본 출력 디렉토리")
    audio_only: bool = Field(default=False, description="오디오만 다운로드")
    save_metadata: bool = Field(default=False, description="메타데이터 저장")
    save_thumbnail: bool = Field(default=False, description="썸네일 저장")


class Settings(BaseSettings):
    """애플리케이션 전체 설정"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        case_sensitive=False,
    )

    download: DownloadSettings = Field(default_factory=DownloadSettings)


# 싱글톤 인스턴스
settings = Settings()
