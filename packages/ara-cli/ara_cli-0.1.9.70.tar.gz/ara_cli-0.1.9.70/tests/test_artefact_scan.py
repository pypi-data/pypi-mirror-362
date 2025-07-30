import pytest
from unittest.mock import patch, MagicMock, mock_open, call
from ara_cli.artefact_scan import check_file, find_invalid_files, show_results
from pydantic import ValidationError


def test_check_file_valid():
    """Tests the happy path where the file is valid and the title matches."""
    mock_artefact_instance = MagicMock()
    mock_artefact_instance.title = "dummy_path"
    # Mock contribution to be None to avoid contribution reference check
    mock_artefact_instance.contribution = None

    mock_artefact_class = MagicMock()
    mock_artefact_class.deserialize.return_value = mock_artefact_instance

    with patch("builtins.open", mock_open(read_data="valid content")):
        is_valid, reason = check_file("dummy_path.feature", mock_artefact_class)
        
    assert reason is None, f"Reason for invalid found, expected none to be found. The reason found: {reason}"
    assert is_valid is True, "File detected as invalid, expected to be valid"


def test_check_file_title_mismatch():
    """Tests the case where the filename and artefact title do not match."""
    mock_artefact_instance = MagicMock()
    mock_artefact_instance.title = "wrong_title"

    mock_artefact_class = MagicMock()
    mock_artefact_class.deserialize.return_value = mock_artefact_instance

    with patch("builtins.open", mock_open(read_data="content")):
        is_valid, reason = check_file("correct_path.feature", mock_artefact_class)

    assert is_valid is False
    assert "Filename-Title Mismatch" in reason

    assert "'correct_path'" in reason
    assert "'wrong_title'" in reason


def test_check_file_value_error():
    mock_artefact_class = MagicMock()
    mock_artefact_class.deserialize.side_effect = ValueError("Value error")

    with patch("builtins.open", mock_open(read_data="invalid content")):
        is_valid, reason = check_file("dummy_path", mock_artefact_class)
        assert is_valid is False
        assert "Value error" in reason


def test_check_file_assertion_error():
    mock_artefact_class = MagicMock()
    mock_artefact_class.deserialize.side_effect = AssertionError(
        "Assertion error")

    with patch("builtins.open", mock_open(read_data="invalid content")):
        is_valid, reason = check_file("dummy_path", mock_artefact_class)
        assert is_valid is False
        assert "Assertion error" in reason


def test_check_file_os_error():
    mock_artefact_class = MagicMock()

    with patch("builtins.open", side_effect=OSError("File not found")):
        is_valid, reason = check_file("dummy_path", mock_artefact_class)
        assert is_valid is False
        assert "File error: File not found" in reason


def test_check_file_unexpected_error():
    mock_artefact_class = MagicMock()
    mock_artefact_class.deserialize.side_effect = Exception("Unexpected error")

    with patch("builtins.open", mock_open(read_data="content")):
        is_valid, reason = check_file("dummy_path", mock_artefact_class)
        assert is_valid is False
        assert "Unexpected error: Exception('Unexpected error')" in reason

# Tests for find_invalid_files


def test_find_invalid_files():
    """Tests finding invalid files with proper mocking of check_file."""
    mock_artefact_class = MagicMock()
    classified_info = {
        "test_classifier": [
            {"file_path": "file1.txt"},              # Should be checked
            {"file_path": "file2.txt"},              # Should be checked
            {"file_path": "templates/file3.txt"},    # Should be skipped
            {"file_path": "some/path/file.data"}     # Should be skipped
        ]
    }
    
    with patch("ara_cli.artefact_models.artefact_mapping.artefact_type_mapping", 
              {"test_classifier": mock_artefact_class}):
        with patch("ara_cli.artefact_scan.check_file") as mock_check_file:
            mock_check_file.side_effect = [
                (True, None),              # for file1.txt
                (False, "Invalid content") # for file2.txt
            ]

            invalid_files = find_invalid_files(classified_info, "test_classifier")
            
            assert len(invalid_files) == 1
            assert invalid_files[0] == ("file2.txt", "Invalid content")
            assert mock_check_file.call_count == 2
            
            # Check that check_file was called with the correct parameters
            mock_check_file.assert_has_calls([
                call("file1.txt", mock_artefact_class, classified_info),
                call("file2.txt", mock_artefact_class, classified_info)
            ], any_order=False)


def test_show_results_no_issues(capsys):
    invalid_artefacts = {}
    with patch("builtins.open", mock_open()) as m:
        show_results(invalid_artefacts)
        captured = capsys.readouterr()
        assert captured.out == "All files are good!\n"
        m.assert_called_once_with("incompatible_artefacts_report.md", "w")
        handle = m()
        handle.write.assert_has_calls([
            call("# Artefact Check Report\n\n"),
            call("No problems found.\n")
        ], any_order=False)


def test_show_results_with_issues(capsys):
    invalid_artefacts = {
        "classifier1": [("file1.txt", "reason1"), ("file2.txt", "reason2")],
        "classifier2": [("file3.txt", "reason3")]
    }
    with patch("builtins.open", mock_open()) as m:
        show_results(invalid_artefacts)
        captured = capsys.readouterr()
        expected_output = (
            "\nIncompatible classifier1 Files:\n"
            "\t- file1.txt\n"
            "\t\treason1\n"
            "\t- file2.txt\n"
            "\t\treason2\n"
            "\nIncompatible classifier2 Files:\n"
            "\t- file3.txt\n"
            "\t\treason3\n"
        )
        assert captured.out == expected_output
        m.assert_called_once_with("incompatible_artefacts_report.md", "w")
        handle = m()
        expected_writes = [
            call("# Artefact Check Report\n\n"),
            call("## classifier1\n"),
            call("- `file1.txt`: reason1\n"),
            call("- `file2.txt`: reason2\n"),
            call("\n"),
            call("## classifier2\n"),
            call("- `file3.txt`: reason3\n"),
            call("\n")
        ]
        handle.write.assert_has_calls(expected_writes, any_order=False)


def test_check_file_with_invalid_contribution():
    """Tests file with invalid contribution reference."""
    mock_artefact_instance = MagicMock()
    mock_artefact_instance.title = "dummy_path"
    
    # Set up invalid contribution
    mock_contribution = MagicMock()
    mock_contribution.classifier = "test_classifier"
    mock_contribution.artefact_name = "non_existing_artefact"
    mock_artefact_instance.contribution = mock_contribution

    mock_artefact_class = MagicMock()
    mock_artefact_class.deserialize.return_value = mock_artefact_instance

    # Mock classified_artefact_info
    classified_info = {"test_classifier": [{"name": "existing_artefact"}]}
    
    # Mock extract_artefact_names_of_classifier to return a list without the referenced artefact
    with patch("builtins.open", mock_open(read_data="valid content")):
        with patch("ara_cli.artefact_fuzzy_search.extract_artefact_names_of_classifier", 
                  return_value=["existing_artefact"]):
            is_valid, reason = check_file("dummy_path.feature", mock_artefact_class, classified_info)
    
    assert is_valid is False
    assert "Invalid Contribution Reference" in reason
