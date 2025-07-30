from ara_cli.ara_config import ensure_directory_exists, read_data, ARAconfig
from unittest.mock import patch, mock_open
import json
import pytest


@pytest.fixture
def default_config_data():
    return ARAconfig().model_dump()


def test_ensure_directory_exists_when_directory_does_not_exist():
    directory = "/some/non/existent/directory"

    with patch("ara_cli.ara_config.exists", return_value=False) as mock_exists:
        with patch("ara_cli.ara_config.os.makedirs") as mock_makedirs:
            result = ensure_directory_exists(directory)

            mock_exists.assert_called_once_with(directory)
            mock_makedirs.assert_called_once_with(directory)
            assert result == directory


def test_ensure_directory_exists_when_directory_exists():
    directory = "/some/existent/directory"

    with patch("ara_cli.ara_config.exists", return_value=True) as mock_exists:
        with patch("ara_cli.ara_config.os.makedirs") as mock_makedirs:
            result = ensure_directory_exists(directory)

            mock_exists.assert_called_once_with(directory)
            mock_makedirs.assert_not_called()
            assert result == directory


@pytest.mark.parametrize("file_exists", [False, True])
def test_read_data(file_exists, default_config_data):
    filepath = '/path/to/ara_config.json'

    with patch('ara_cli.ara_config.exists', return_value=file_exists):

        if file_exists:
            with patch('ara_cli.ara_config.open', mock_open(read_data=json.dumps(default_config_data))) as mock_file:
                result = read_data(filepath)
        else:
            m_open = mock_open()
            m_open.return_value.read.return_value = json.dumps(default_config_data)

            with patch('ara_cli.ara_config.open', m_open) as mock_file:
                with patch('ara_cli.ara_config.json.dump') as mock_json_dump, \
                     patch('ara_cli.ara_config.exit') as mock_exit:

                    result = read_data(filepath)

                    mock_json_dump.assert_called_once_with(default_config_data, mock_file(), indent=4)
                    mock_exit.assert_called_once()

    # Validate the returned configuration
    assert result.model_dump() == default_config_data
