"""Pytest 설정 파일"""


import pytest


@pytest.fixture
def test_output_dir(tmp_path):
    """테스트용 임시 출력 디렉토리"""
    output_dir = tmp_path / "downloads"
    output_dir.mkdir()
    return output_dir


@pytest.fixture
def sample_video_url():
    """테스트용 샘플 동영상 URL (짧은 테스트 동영상)"""
    return "https://www.youtube.com/watch?v=jNQXAC9IVRw"
