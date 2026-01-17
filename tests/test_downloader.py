"""다운로더 모듈 테스트"""


import pytest

from youtube_downloader.downloader import Downloader
from youtube_downloader.models import DownloadOptions, DownloadResult


def test_downloader_initialization():
    """다운로더 초기화 테스트"""
    downloader = Downloader()
    assert downloader.options is not None
    assert downloader.options.quality == "best"


def test_downloader_with_custom_options(test_output_dir):
    """커스텀 옵션으로 다운로더 초기화"""
    options = DownloadOptions(
        quality="720p",
        output_dir=test_output_dir,
        audio_only=True,
        audio_quality="320",
    )
    downloader = Downloader(options)

    assert downloader.options.quality == "720p"
    assert downloader.options.output_dir == test_output_dir
    assert downloader.options.audio_only is True
    assert downloader.options.audio_quality == "320"


def test_audio_quality_default():
    """오디오 품질 기본값 테스트"""
    options = DownloadOptions(audio_only=True)
    assert options.audio_quality == "192"


def test_audio_quality_custom():
    """커스텀 오디오 품질 설정 테스트"""
    options = DownloadOptions(audio_only=True, audio_quality="128")
    downloader = Downloader(options)
    assert downloader.options.audio_quality == "128"


def test_download_invalid_url():
    """잘못된 URL 처리 테스트"""
    downloader = Downloader()
    result = downloader.download("invalid-url")

    assert isinstance(result, DownloadResult)
    assert result.success is False
    assert result.error_message is not None


@pytest.mark.integration
@pytest.mark.skip(reason="실제 네트워크 요청이 필요한 통합 테스트")
def test_download_real_video(test_output_dir, sample_video_url):
    """실제 동영상 다운로드 테스트"""
    options = DownloadOptions(output_dir=test_output_dir)
    downloader = Downloader(options)

    result = downloader.download(sample_video_url)

    assert result.success is True
    assert result.video_info is not None
    assert result.file_path is not None
    assert result.file_path.exists()
