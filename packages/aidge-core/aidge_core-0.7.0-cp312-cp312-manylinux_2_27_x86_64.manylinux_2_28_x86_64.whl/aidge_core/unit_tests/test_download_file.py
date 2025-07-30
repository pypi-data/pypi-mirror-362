import pytest
from unittest import mock
from unittest.mock import MagicMock, patch
import requests
from aidge_core.utils import download_file


@pytest.fixture
def tmp_file_path(tmp_path):
    return tmp_path / "test_file.txt"


@patch("aidge_core.utils.pathlib.Path.exists")
@patch("aidge_core.utils.Log")
def test_download_skipped_if_file_exists(mock_log, mock_exists, tmp_file_path):
    mock_exists.return_value = True
    download_file(tmp_file_path, "http://example.com/file.txt")
    mock_log.info.assert_called_once_with("test_file.txt already exists.")


@patch("aidge_core.utils.requests.get")
@patch("aidge_core.utils.pathlib.Path.exists", return_value=False)
@patch("aidge_core.utils.tqdm.tqdm")
def test_file_downloaded_with_progress(mock_tqdm, mock_exists, mock_requests, tmp_file_path):
    # Setup mock response
    content = [b"data1", b"data2"]
    mock_response = MagicMock()
    mock_response.iter_content = MagicMock(return_value=content)
    mock_response.headers = {"content-length": str(sum(len(c) for c in content))}
    mock_response.raise_for_status = MagicMock()
    mock_requests.return_value = mock_response

    # Mock tqdm context manager
    mock_progress = mock.MagicMock()
    mock_tqdm.return_value.__enter__.return_value = mock_progress

    with patch("builtins.open", mock.mock_open()) as mock_file:
        download_file(tmp_file_path, "http://example.com/file.txt", show_progress=True)

        # Check write calls
        handle = mock_file()
        expected_calls = [mock.call(b"data1"), mock.call(b"data2")]
        handle.write.assert_has_calls(expected_calls, any_order=False)

        # Check tqdm update calls
        mock_progress.update.assert_any_call(len(b"data1"))
        mock_progress.update.assert_any_call(len(b"data2"))


@patch("aidge_core.utils.requests.get")
@patch("aidge_core.utils.pathlib.Path.exists", return_value=False)
@patch("aidge_core.utils._dummy_tqdm")
def test_file_downloaded_without_progress(mock_dummy_tqdm, mock_exists, mock_requests, tmp_file_path):
    content = [b"chunk"]
    mock_response = MagicMock()
    mock_response.iter_content = MagicMock(return_value=content)
    mock_response.headers = {"content-length": str(len(b"chunk"))}
    mock_response.raise_for_status = MagicMock()
    mock_requests.return_value = mock_response

    # Mock dummy tqdm
    mock_progress = mock.MagicMock()
    mock_dummy_tqdm.return_value.__enter__.return_value = mock_progress

    with patch("builtins.open", mock.mock_open()) as mock_file:
        download_file(tmp_file_path, "http://example.com/file.txt", show_progress=False)
        handle = mock_file()
        handle.write.assert_called_once_with(b"chunk")


@patch("aidge_core.utils.Log")
@patch("aidge_core.utils.requests.get", side_effect=requests.exceptions.RequestException("Connection failed"))
@patch("aidge_core.utils.pathlib.Path.exists", return_value=False)
def test_download_fails_gracefully(mock_exists, mock_requests, mock_log, tmp_file_path):
    download_file(tmp_file_path, "http://example.com/file.txt")
    mock_log.error.assert_called_once_with("Failed to download the file: Connection failed")


def main():
    import sys

    print(
        f"{sys.argv[0]}: Warning: skipped: run with: pytest {sys.argv[0]}",
        file=sys.stderr,
)


if __name__ == "__main__":
    main()
