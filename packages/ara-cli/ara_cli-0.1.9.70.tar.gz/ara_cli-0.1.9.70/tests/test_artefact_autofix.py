import pytest
from unittest.mock import patch, mock_open, MagicMock
from ara_cli.artefact_autofix import (
    read_report_file,
    parse_report,
    apply_autofix,
    read_artefact,
    determine_artefact_type_and_class,
    run_agent,
    write_corrected_artefact,
    construct_prompt,
    fix_title_mismatch,
)
from ara_cli.artefact_models.artefact_model import ArtefactType


@pytest.fixture
def mock_artefact_type():
    """Provides a mock for the ArtefactType enum member."""
    mock_type = MagicMock()
    mock_type.value = "feature"
    return mock_type


@pytest.fixture
def mock_artefact_class():
    """Provides a mock for the Artefact class."""
    mock_class = MagicMock()
    mock_class._title_prefix.return_value = "Feature:"
    # Mock the serialize method for the agent tests
    mock_class.serialize.return_value = "llm corrected content"
    return mock_class


@pytest.fixture
def mock_classified_artefact_info():
    """Provides a mock for the classified artefact info dictionary."""
    return MagicMock()


def test_read_report_file_success():
    """Tests successful reading of the report file."""
    mock_content = "# Artefact Check Report\n- `file.feature`: reason"
    with patch("builtins.open", mock_open(read_data=mock_content)) as m:
        content = read_report_file()
        assert content == mock_content
        m.assert_called_once_with(
            "incompatible_artefacts_report.md", "r", encoding="utf-8"
        )


def test_read_report_file_not_found(capsys):
    with patch("builtins.open", side_effect=OSError("File not found")):
        content = read_report_file()
        assert content is None
        assert "Artefact scan results file not found" in capsys.readouterr().out


def test_parse_report_with_issues():
    content = (
        "# Artefact Check Report\n\n## feature\n- `path/to/file.feature`: A reason\n"
    )
    expected = {"feature": [("path/to/file.feature", "A reason")]}
    assert parse_report(content) == expected


def test_parse_report_no_issues():
    content = "# Artefact Check Report\n\nNo problems found.\n"
    assert parse_report(content) == {}


def test_parse_report_invalid_format():
    assert parse_report("This is not a valid report") == {}


def test_parse_report_invalid_line_format():
    content = "# Artefact Check Report\n\n## feature\n- an invalid line\n"
    assert parse_report(content) == {"feature": []}


def test_read_artefact_success():
    mock_content = "Feature: My Feature"
    with patch("builtins.open", mock_open(read_data=mock_content)) as m:
        content = read_artefact("file.feature")
        assert content == mock_content
        m.assert_called_once_with("file.feature", "r", encoding="utf-8")


def test_read_artefact_file_not_found(capsys):
    with patch("builtins.open", side_effect=FileNotFoundError):
        result = read_artefact("nonexistent.feature")
        assert result is None
        assert "File not found: nonexistent.feature" in capsys.readouterr().out


@patch("ara_cli.artefact_models.artefact_mapping.artefact_type_mapping")
def test_determine_artefact_type_and_class_no_class_found(mock_mapping, capsys):
    mock_mapping.get.return_value = None
    # The function returns (None, None) if the class is not in the mapping.
    artefact_type, artefact_class = determine_artefact_type_and_class("feature")
    assert artefact_type is None
    assert artefact_class is None
    # The print statement inside the function is called before returning, so this check is valid.
    assert "No artefact class found for" in capsys.readouterr().out


@patch("ara_cli.artefact_models.artefact_model.ArtefactType", side_effect=ValueError)
def test_determine_artefact_type_and_class_invalid(mock_artefact_type_enum, capsys):
    artefact_type, artefact_class = determine_artefact_type_and_class(
        "invalid_classifier"
    )
    assert artefact_type is None
    assert artefact_class is None
    assert "Invalid classifier: invalid_classifier" in capsys.readouterr().out


def test_write_corrected_artefact():
    with patch("builtins.open", mock_open()) as m:
        write_corrected_artefact("file.feature", "corrected content")
        m.assert_called_once_with("file.feature", "w", encoding="utf-8")
        m().write.assert_called_once_with("corrected content")


def test_construct_prompt_for_task():
    prompt = construct_prompt(ArtefactType.task, "some reason", "file.task", "text")
    assert (
        "For task artefacts, if the action items looks like template or empty" in prompt
    )


@patch("ara_cli.artefact_autofix.run_agent")
@patch(
    "ara_cli.artefact_autofix.determine_artefact_type_and_class",
    return_value=(None, None),
)
@patch("ara_cli.artefact_autofix.read_artefact", return_value="original text")
def test_apply_autofix_exits_when_classifier_is_invalid(
    mock_read, mock_determine, mock_run_agent, mock_classified_artefact_info
):
    """Tests that apply_autofix exits early if the classifier is invalid."""
    result = apply_autofix(
        "file.feature",
        "invalid",
        "reason",
        deterministic=True,
        non_deterministic=True,
        classified_artefact_info=mock_classified_artefact_info,
    )
    assert result is False
    mock_read.assert_called_once_with("file.feature")
    mock_determine.assert_called_once_with("invalid")
    mock_run_agent.assert_not_called()


@patch("ara_cli.artefact_autofix.run_agent")
@patch("ara_cli.artefact_autofix.write_corrected_artefact")
@patch("ara_cli.artefact_autofix.fix_title_mismatch", return_value="fixed text")
@patch("ara_cli.artefact_autofix.determine_artefact_type_and_class")
@patch("ara_cli.artefact_autofix.read_artefact", return_value="original text")
def test_apply_autofix_for_title_mismatch_with_deterministic_flag(
    mock_read,
    mock_determine,
    mock_fix_title,
    mock_write,
    mock_run_agent,
    mock_artefact_type,
    mock_artefact_class,
    mock_classified_artefact_info,
):
    """Tests that a deterministic fix is applied when the flag is True."""
    mock_determine.return_value = (mock_artefact_type, mock_artefact_class)
    reason = "Filename-Title Mismatch: some details"

    result = apply_autofix(
        "file.feature",
        "feature",
        reason,
        deterministic=True,
        non_deterministic=False,
        classified_artefact_info=mock_classified_artefact_info,
    )

    assert result is True
    mock_fix_title.assert_called_once_with(
        file_path="file.feature",
        artefact_text="original text",
        artefact_class=mock_artefact_class,
        classified_artefact_info=mock_classified_artefact_info,
    )
    mock_write.assert_called_once_with("file.feature", "fixed text")
    mock_run_agent.assert_not_called()


@patch("ara_cli.artefact_autofix.run_agent")
@patch("ara_cli.artefact_autofix.write_corrected_artefact")
@patch("ara_cli.artefact_autofix.fix_title_mismatch")
@patch("ara_cli.artefact_autofix.determine_artefact_type_and_class")
@patch("ara_cli.artefact_autofix.read_artefact", return_value="original text")
def test_apply_autofix_skips_title_mismatch_without_deterministic_flag(
    mock_read,
    mock_determine,
    mock_fix_title,
    mock_write,
    mock_run_agent,
    mock_artefact_type,
    mock_artefact_class,
    mock_classified_artefact_info,
):
    """Tests that a deterministic fix is skipped when the flag is False."""
    mock_determine.return_value = (mock_artefact_type, mock_artefact_class)
    reason = "Filename-Title Mismatch: some details"

    result = apply_autofix(
        "file.feature",
        "feature",
        reason,
        deterministic=False,
        non_deterministic=True,
        classified_artefact_info=mock_classified_artefact_info,
    )

    assert result is False
    mock_fix_title.assert_not_called()
    mock_write.assert_not_called()
    mock_run_agent.assert_not_called()


@patch("ara_cli.artefact_autofix.write_corrected_artefact")
@patch("ara_cli.artefact_autofix.run_agent")
@patch("ara_cli.artefact_autofix.determine_artefact_type_and_class")
@patch("ara_cli.artefact_autofix.read_artefact", return_value="original text")
def test_apply_autofix_for_llm_fix_with_non_deterministic_flag(
    mock_read,
    mock_determine,
    mock_run_agent,
    mock_write,
    mock_artefact_type,
    mock_artefact_class,
    mock_classified_artefact_info,
):
    """Tests that an LLM fix is applied when the non-deterministic flag is True."""
    mock_determine.return_value = (mock_artefact_type, mock_artefact_class)
    mock_run_agent.return_value = mock_artefact_class
    reason = "Pydantic validation error"

    result = apply_autofix(
        "file.feature",
        "feature",
        reason,
        deterministic=False,
        non_deterministic=True,
        classified_artefact_info=mock_classified_artefact_info,
    )

    assert result is True
    mock_run_agent.assert_called_once()
    mock_write.assert_called_once_with("file.feature", "llm corrected content")


@patch("ara_cli.artefact_autofix.write_corrected_artefact")
@patch("ara_cli.artefact_autofix.run_agent")
@patch("ara_cli.artefact_autofix.determine_artefact_type_and_class")
@patch("ara_cli.artefact_autofix.read_artefact", return_value="original text")
def test_apply_autofix_skips_llm_fix_without_non_deterministic_flag(
    mock_read,
    mock_determine,
    mock_run_agent,
    mock_write,
    mock_artefact_type,
    mock_artefact_class,
    mock_classified_artefact_info,
):
    """Tests that an LLM fix is skipped when the non-deterministic flag is False."""
    mock_determine.return_value = (mock_artefact_type, mock_artefact_class)
    reason = "Pydantic validation error"

    result = apply_autofix(
        "file.feature",
        "feature",
        reason,
        deterministic=True,
        non_deterministic=False,
        classified_artefact_info=mock_classified_artefact_info,
    )

    assert result is False
    mock_run_agent.assert_not_called()
    mock_write.assert_not_called()


@patch("ara_cli.artefact_autofix.run_agent", side_effect=Exception("LLM failed"))
@patch("ara_cli.artefact_autofix.determine_artefact_type_and_class")
@patch("ara_cli.artefact_autofix.read_artefact", return_value="original text")
def test_apply_autofix_llm_exception(
    mock_read,
    mock_determine,
    mock_run_agent,
    capsys,
    mock_artefact_type,
    mock_artefact_class,
    mock_classified_artefact_info,
):
    """Tests that an exception during an LLM fix is handled gracefully."""
    mock_determine.return_value = (mock_artefact_type, mock_artefact_class)
    reason = "Pydantic validation error"

    result = apply_autofix(
        "file.feature",
        "feature",
        reason,
        deterministic=False,
        non_deterministic=True,
        classified_artefact_info=mock_classified_artefact_info,
    )

    assert result is False
    assert (
        "LLM agent failed to fix artefact at file.feature: LLM failed"
        in capsys.readouterr().out
    )


# === Other Tests ===


def test_fix_title_mismatch_success(mock_artefact_class):
    artefact_text = "Feature: wrong title\nSome other content"
    file_path = "path/to/correct_title.feature"

    expected_text = "Feature: correct title\nSome other content"

    result = fix_title_mismatch(file_path, artefact_text, mock_artefact_class)

    assert result == expected_text
    mock_artefact_class._title_prefix.assert_called_once()


def test_fix_title_mismatch_prefix_not_found(capsys, mock_artefact_class):
    artefact_text = "No title prefix here"
    file_path = "path/to/correct_title.feature"

    result = fix_title_mismatch(file_path, artefact_text, mock_artefact_class)

    assert result == artefact_text  # Should return original text
    assert "Warning: Title prefix 'Feature:' not found" in capsys.readouterr().out


@patch("pydantic_ai.Agent")
def test_run_agent_exception_handling(mock_agent_class):
    mock_agent_instance = mock_agent_class.return_value
    mock_agent_instance.run_sync.side_effect = Exception("Agent error")
    with pytest.raises(Exception, match="Agent error"):
        run_agent("prompt", MagicMock())
