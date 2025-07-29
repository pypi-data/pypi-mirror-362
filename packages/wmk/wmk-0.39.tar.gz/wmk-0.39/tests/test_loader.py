import os
from unittest.mock import Mock, patch

import pytest

from wmk.loader import Loader


@pytest.fixture
def loader():
    return Loader()


@pytest.fixture
def mock_response():
    response = Mock()
    response.headers = {"content-length": "1024"}
    response.stream.return_value = [b"test data"] * 10
    return response


def test_loader_initialization():
    loader = Loader()
    assert loader.chunk_size == 1024 * 1024  # Default chunk size
    custom_chunk_size = 2048
    custom_loader = Loader(chunk_size=custom_chunk_size)
    assert custom_loader.chunk_size == custom_chunk_size


@patch("urllib3.PoolManager.request")
def test_successful_download(mock_request, loader, mock_response, tmp_path):
    mock_request.return_value = mock_response
    test_file = tmp_path / "test.txt"

    result = loader.download_file("http://example.com/test.txt", str(test_file))

    assert result is True
    assert test_file.exists()
    assert test_file.stat().st_size > 0


@patch("urllib3.PoolManager.request")
def test_download_with_headers(mock_request, loader, mock_response, tmp_path):
    mock_request.return_value = mock_response
    test_file = tmp_path / "test.txt"
    headers = {"Authorization": "Bearer token"}

    loader.download_file("http://example.com/test.txt", str(test_file), headers=headers)

    mock_request.assert_called_with(
        "GET", "http://example.com/test.txt", preload_content=False, headers=headers
    )


@patch("urllib3.PoolManager.request")
def test_failed_download(mock_request, loader, tmp_path):
    mock_request.side_effect = Exception("Network error")
    test_file = tmp_path / "test.txt"

    result = loader.download_file("http://example.com/test.txt", str(test_file))

    assert result is False
    assert not test_file.exists()


@patch("urllib3.PoolManager.request")
def test_size_verification_failure(mock_request, loader, tmp_path):
    response = Mock()
    response.headers = {"content-length": "2048"}  # Claim larger size
    response.stream.return_value = [b"test data"]  # Return less data
    mock_request.return_value = response

    test_file = tmp_path / "test.txt"
    result = loader.download_file("http://example.com/test.txt", str(test_file))

    assert result is False
    assert not test_file.exists()


@patch("urllib3.PoolManager.request")
def test_cleanup_on_failure(mock_request, loader, tmp_path):
    mock_request.side_effect = Exception("Network error")
    test_file = tmp_path / "test.txt"

    # Create a file that should be cleaned up
    test_file.write_text("existing content")
    assert test_file.exists()

    result = loader.download_file("http://example.com/test.txt", str(test_file))

    assert result is False
    assert not test_file.exists()


@patch("urllib3.PoolManager.request")
def test_download_multiple_files(mock_request, loader, mock_response, tmp_path):
    mock_request.return_value = mock_response

    # Create test files and URLs
    files = {
        "http://example.com/file1.txt": str(tmp_path / "file1.txt"),
        "http://example.com/file2.txt": str(tmp_path / "file2.txt"),
        "http://example.com/file3.txt": str(tmp_path / "file3.txt"),
    }

    results = loader.download_files(files)

    assert all(results.values())  # All downloads should succeed
    assert len(results) == len(files)
    assert all(os.path.exists(path) for path in files.values())


@patch("urllib3.PoolManager.request")
def test_download_files_with_failures(mock_request, loader, mock_response, tmp_path):
    def mock_download(method, url, preload_content=True, **kwargs):
        if "file2" in url:
            raise Exception("Network error")
        return mock_response

    mock_request.side_effect = mock_download

    files = {
        "http://example.com/file1.txt": str(tmp_path / "file1.txt"),
        "http://example.com/file2.txt": str(tmp_path / "file2.txt"),
        "http://example.com/file3.txt": str(tmp_path / "file3.txt"),
    }

    results = loader.download_files(files)

    assert results["http://example.com/file1.txt"] is True
    assert results["http://example.com/file2.txt"] is False
    assert results["http://example.com/file3.txt"] is True
    assert not os.path.exists(tmp_path / "file2.txt")


@patch("urllib3.PoolManager.request")
def test_download_files_with_headers(mock_request, loader, mock_response, tmp_path):
    mock_request.return_value = mock_response

    files = {
        "http://example.com/file1.txt": str(tmp_path / "file1.txt"),
        "http://example.com/file2.txt": str(tmp_path / "file2.txt"),
    }
    headers = {"Authorization": "Bearer token"}

    loader.download_files(files, headers=headers)

    # Verify headers were passed to each request
    for call in mock_request.call_args_list:
        assert call.kwargs["headers"] == headers
