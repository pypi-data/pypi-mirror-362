from ara_cli.artefact_fuzzy_search import (
    find_closest_name_matches,
    extract_artefact_names_of_classifier,
)
from ara_cli.file_classifier import FileClassifier
from ara_cli.artefact_reader import ArtefactReader
from ara_cli.artefact_models.artefact_load import artefact_from_content
from ara_cli.artefact_models.artefact_model import Artefact
from typing import Optional, Dict, List, Tuple
import difflib
import os


def read_report_file():
    file_path = "incompatible_artefacts_report.md"
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except OSError:
        print(
            'Artefact scan results file not found. Did you run the "ara scan" command?'
        )
        return None
    return content


def parse_report(content: str) -> Dict[str, List[Tuple[str, str]]]:
    """
    Parses the incompatible artefacts report and returns structured data.
    Returns a dictionary where keys are artefact classifiers, and values are lists of (file_path, reason) tuples.
    """
    lines = content.splitlines()
    issues = {}
    current_classifier = None

    if not lines or lines[0] != "# Artefact Check Report":
        return issues
        return issues

    if len(lines) >= 3 and lines[2] == "No problems found.":
        return issues
        return issues

    for line in lines[1:]:
        line = line.strip()
        if not line:
            continue

        if line.startswith("## "):
            current_classifier = line[3:].strip()
            issues[current_classifier] = []

        elif line.startswith("- ") and current_classifier is not None:
            parts = line.split("`", 2)
            if len(parts) < 3:
                continue

            file_path = parts[1]
            reason = parts[2].split(":", 1)[1].strip() if ":" in parts[2] else ""
            issues[current_classifier].append((file_path, reason))

    return issues


def read_artefact(file_path):
    """Reads the artefact text from the given file path."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None


def determine_artefact_type_and_class(classifier):
    from ara_cli.artefact_models.artefact_mapping import artefact_type_mapping
    from ara_cli.artefact_models.artefact_model import ArtefactType

    try:
        artefact_type = ArtefactType(classifier)
    except ValueError:
        print(f"Invalid classifier: {classifier}")
        return None, None

    artefact_class = artefact_type_mapping.get(artefact_type)
    if not artefact_class:
        print(f"No artefact class found for {artefact_type}")
        return None, None

    return artefact_type, artefact_class


def construct_prompt(artefact_type, reason, file_path, artefact_text):
    from ara_cli.artefact_models.artefact_model import ArtefactType

    prompt = (
        f"Correct the following {artefact_type.value} artefact to fix the issue: {reason}. "
        "Provide the corrected artefact. Do not reformulate the artefact, "
        "just fix the pydantic model errors, use correct grammar. "
        "You should follow the name of the file "
        f"from its path {file_path} for naming the artefact's title. "
        "You are not allowed to use file extention in the artefact title. "
        "You are not allowed to modify, delete or add tags. "
        "User tag should be '@user_<username>'. The pydantic model already provides the '@user_' prefix. "
        "So you should be careful to not make it @user_user_<username>. "
    )

    if artefact_type == ArtefactType.task:
        prompt += (
            "For task artefacts, if the action items looks like template or empty "
            "then just delete those action items."
        )

    prompt += "\nThe current artefact is:\n" "```\n" f"{artefact_text}\n" "```"

    return prompt


def run_agent(prompt, artefact_class):
    from pydantic_ai import Agent

    # gpt-4o
    # anthropic:claude-3-7-sonnet-20250219
    # anthropic:claude-4-sonnet-20250514
    agent = Agent(
        model="anthropic:claude-4-sonnet-20250514",
        result_type=artefact_class,
        instrument=True,
    )
    result = agent.run_sync(prompt)
    return result.data


def write_corrected_artefact(file_path, corrected_text):
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(corrected_text)
    print(f"Fixed artefact at {file_path}")


def ask_for_correct_contribution(
    artefact_info: Optional[tuple[str, str]] = None
) -> tuple[str, str]:
    """
    Ask the user to provide a valid contribution when no match can be found.

    Args:
        artefact_info: Optional tuple containing (artefact_name, artefact_classifier)

    Returns:
        A tuple of (name, classifier) for the contribution
    """

    artefact_name, artefact_classifier = (
        artefact_info if artefact_info else (None, None)
    )
    contribution_message = (
        f"of {artefact_classifier} artefact '{artefact_name}'" if artefact_name else ""
    )

    print(
        f"Can not determine a match for contribution {contribution_message}. "
        f"Please provide a valid contribution or contribution will be empty (<classifier> <file_name>)."
    )

    user_input = input().strip()

    if not user_input:
        return None, None

    parts = user_input.split(maxsplit=1)
    if len(parts) != 2:
        print("Invalid input format. Expected: <classifier> <file_name>")
        return None, None

    classifier, name = parts
    return name, classifier


def ask_for_contribution_choice(
    choices, artefact_info: Optional[tuple[str, str]] = None
) -> Optional[str]:
    artefact_name, artefact_classifier = artefact_info
    message = "Found multiple close matches for the contribution"
    if artefact_name and artefact_classifier:
        message += f" of the {artefact_classifier} '{artefact_name}'"
    print(f"{message}.")
    for i, contribution in enumerate(choices):
        print(f"{i + 1}: {contribution}")
    choice_number = input(
        "Please choose the artefact to use for contribution (enter number): "
    )
    try:
        choice_index = int(choice_number) - 1
        if choice_index < 0 or choice_index >= len(choices):
            print("Invalid choice. Aborting contribution choice.")
            return None
        choice = choices[choice_index]
    except ValueError:
        print("Invalid input. Aborting contribution choice.")
        return None
    return choice


def _has_valid_contribution(artefact: Artefact) -> bool:
    contribution = artefact.contribution
    return contribution and contribution.artefact_name and contribution.classifier


def _update_rule(
    artefact: Artefact, name: str, classifier: str, classified_file_info: dict
) -> None:
    """Updates the rule in the contribution if a close match is found."""
    rule = artefact.contribution.rule

    content, artefact_data = ArtefactReader.read_artefact(
        artefact_name=name,
        classifier=classifier,
        classified_file_info=classified_file_info,
    )

    parent = artefact_from_content(content=content)
    rules = parent.rules

    closest_rule_match = difflib.get_close_matches(rule, rules, cutoff=0.5)
    if closest_rule_match:
        artefact.contribution.rule = closest_rule_match[0]


def _set_contribution_multiple_matches(
    artefact: Artefact,
    closest_matches: list,
    artefact_tuple: tuple,
    classified_file_info: dict,
) -> tuple[Artefact, bool]:
    contribution = artefact.contribution
    classifier = contribution.classifier
    original_name = contribution.artefact_name

    closest_match = closest_matches[0]
    if len(closest_matches) > 1:
        closest_match = ask_for_contribution_choice(closest_matches, artefact_tuple)

    if not closest_match:
        print(
            f"Contribution of {artefact_tuple[1]} '{artefact_tuple[0]}' will be empty."
        )
        artefact.contribution = None
        return artefact, True

    print(
        f"Updating contribution of {artefact_tuple[1]} '{artefact_tuple[0]}' to {classifier} '{closest_match}'"
    )
    contribution.artefact_name = closest_match
    artefact.contribution = contribution

    if contribution.rule:
        _update_rule(artefact, original_name, classifier, classified_file_info)

    return artefact, True


def set_closest_contribution(
    artefact: Artefact, classified_file_info=None
) -> tuple[Artefact, bool]:
    if not _has_valid_contribution(artefact):
        return artefact, False
    contribution = artefact.contribution
    name = contribution.artefact_name
    classifier = contribution.classifier
    rule = contribution.rule

    if not classified_file_info:
        file_classifier = FileClassifier(os)
        classified_file_info = file_classifier.classify_files()

    all_artefact_names = extract_artefact_names_of_classifier(
        classified_files=classified_file_info, classifier=classifier
    )
    closest_matches = find_closest_name_matches(
        artefact_name=name, all_artefact_names=all_artefact_names
    )

    artefact_tuple = (artefact.title, artefact._artefact_type().value)

    if not closest_matches:
        name, classifier = ask_for_correct_contribution(artefact_tuple)
        if not name or not classifier:
            artefact.contribution = None
            return artefact, True
        print(f"Updating contribution of {artefact._artefact_type().value} '{artefact.title}' to {classifier} '{name}'")
        contribution.artefact_name = name
        contribution.classifier = classifier
        artefact.contribution = contribution
        return artefact, True

    if closest_matches[0] == name:
        return artefact, False

    return _set_contribution_multiple_matches(
        artefact=artefact,
        closest_matches=closest_matches,
        artefact_tuple=artefact_tuple,
        classified_file_info=classified_file_info,
    )

    print(
        f"Updating contribution of {artefact._artefact_type().value} '{artefact.title}' to {classifier} '{closest_match}'"
    )
    contribution.artefact_name = closest_match
    artefact.contribution = contribution

    if not rule:
        return artefact, True

    content, artefact = ArtefactReader.read_artefact(
        artefact_name=name,
        classifier=classifier,
        classified_file_info=classified_file_info,
    )
    parent = artefact_from_content(content=content)
    rules = parent.rules

    closest_rule_match = difflib.get_close_matches(rule, rules, cutoff=0.5)
    if closest_rule_match:
        contribution.rule = closest_rule_match
        artefact.contribution = contribution
    return artefact, True


def fix_title_mismatch(
    file_path: str, artefact_text: str, artefact_class, **kwargs
) -> str:
    """
    Deterministically fixes the title in the artefact text to match the filename.
    """
    base_name = os.path.basename(file_path)
    correct_title_underscores, _ = os.path.splitext(base_name)
    correct_title_spaces = correct_title_underscores.replace("_", " ")

    title_prefix = artefact_class._title_prefix()

    lines = artefact_text.splitlines()
    new_lines = []
    title_found_and_replaced = False

    for line in lines:
        if not title_found_and_replaced and line.strip().startswith(title_prefix):
            new_lines.append(f"{title_prefix} {correct_title_spaces}")
            title_found_and_replaced = True
        else:
            new_lines.append(line)

    if not title_found_and_replaced:
        print(
            f"Warning: Title prefix '{title_prefix}' not found in {file_path}. Title could not be fixed."
        )
        return artefact_text

    return "\n".join(new_lines)


def fix_contribution(
    file_path: str,
    artefact_text: str,
    artefact_class: str,
    classified_artefact_info: dict,
    **kwargs,
):
    if not classified_artefact_info:
        file_classifier = FileClassifier(os)
        classified_artefact_info = file_classifier.classify_files()
    artefact = artefact_class.deserialize(artefact_text)
    artefact, _ = set_closest_contribution(artefact)
    artefact_text = artefact.serialize()
    return artefact_text


def apply_autofix(
    file_path: str,
    classifier: str,
    reason: str,
    deterministic: bool = True,
    non_deterministic: bool = True,
    classified_artefact_info: Optional[Dict[str, List[Dict[str, str]]]] = None,
) -> bool:
    artefact_text = read_artefact(file_path)
    if artefact_text is None:
        return False

    artefact_type, artefact_class = determine_artefact_type_and_class(classifier)
    if artefact_type is None or artefact_class is None:
        return False

    if classified_artefact_info is None:
        file_classifier = FileClassifier(os)
        classified_file_info = file_classifier.classified_files()

    deterministic_markers_to_functions = {
        "Filename-Title Mismatch": fix_title_mismatch,
        "Invalid Contribution Reference": fix_contribution,
    }

    try:
        deterministic_issue = next(
            (
                marker
                for marker in deterministic_markers_to_functions.keys()
                if marker in reason
            ),
            None,
        )
    except StopIteration:
        pass
    is_deterministic_issue = deterministic_issue is not None

    if deterministic and is_deterministic_issue:
        print(f"Attempting deterministic fix for {file_path}...")
        corrected_text = deterministic_markers_to_functions[deterministic_issue](
            file_path=file_path,
            artefact_text=artefact_text,
            artefact_class=artefact_class,
            classified_artefact_info=classified_artefact_info,
        )
        write_corrected_artefact(file_path, corrected_text)
        return True

    # Attempt non-deterministic fix if requested and the issue is NOT deterministic
    if non_deterministic and not is_deterministic_issue:
        print(f"Attempting non-deterministic (LLM) fix for {file_path}...")
        prompt = construct_prompt(artefact_type, reason, file_path, artefact_text)
        try:
            corrected_artefact = run_agent(prompt, artefact_class)
            corrected_text = corrected_artefact.serialize()
            write_corrected_artefact(file_path, corrected_text)
            return True
        except Exception as e:
            print(f"LLM agent failed to fix artefact at {file_path}: {e}")
            return False

    # Log if a fix was skipped due to flags
    if is_deterministic_issue and not deterministic:
        print(f"Skipping deterministic fix for {file_path} as per request.")
    elif not is_deterministic_issue and not non_deterministic:
        print(f"Skipping non-deterministic fix for {file_path} as per request.")

    return False
