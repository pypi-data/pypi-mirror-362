from textwrap import indent
import os


def check_file(file_path, artefact_class, classified_artefact_info=None):
    from pydantic import ValidationError
    from ara_cli.artefact_fuzzy_search import extract_artefact_names_of_classifier
    from ara_cli.file_classifier import FileClassifier

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except OSError as e:
        return False, f"File error: {e}"

    if not classified_artefact_info:
        file_classifier = FileClassifier(os)
        classified_artefact_info = file_classifier.classify_files()

    try:
        artefact_instance = artefact_class.deserialize(content)

        base_name = os.path.basename(file_path)
        file_name_without_ext, _ = os.path.splitext(base_name)

        if artefact_instance.title != file_name_without_ext:
            reason = (f"Filename-Title Mismatch: The file name '{file_name_without_ext}' "
                      f"does not match the artefact title '{artefact_instance.title}'.")
            return False, reason
        
        # Check contribution reference validity
        contribution = artefact_instance.contribution
        if contribution and contribution.artefact_name and contribution.classifier:
            
            # Find all artefact names of the referenced classifier
            all_artefact_names = extract_artefact_names_of_classifier(
                classified_files=classified_artefact_info,
                classifier=contribution.classifier
            )
            
            # Check if the referenced artefact exists
            if contribution.artefact_name not in all_artefact_names:
                reason = (f"Invalid Contribution Reference: The contribution references "
                          f"'{contribution.classifier}' artefact '{contribution.artefact_name}' "
                          f"which does not exist.")
                return False, reason

        return True, None
    except (ValidationError, ValueError, AssertionError) as e:
        return False, str(e)
    except Exception as e:
        return False, f"Unexpected error: {e!r}"


def find_invalid_files(classified_artefact_info, classifier):
    from ara_cli.artefact_models.artefact_mapping import artefact_type_mapping

    artefact_class = artefact_type_mapping[classifier]
    invalid_files = []
    for artefact_info in classified_artefact_info[classifier]:
        if "templates/" in artefact_info["file_path"]:
            continue
        if ".data" in artefact_info["file_path"]:
            continue
        is_valid, reason = check_file(artefact_info["file_path"], artefact_class, classified_artefact_info)
        if not is_valid:
            invalid_files.append((artefact_info["file_path"], reason))
    return invalid_files


def show_results(invalid_artefacts):
    has_issues = False
    with open("incompatible_artefacts_report.md", "w") as report:
        report.write("# Artefact Check Report\n\n")
        for classifier, files in invalid_artefacts.items():
            if files:
                has_issues = True
                print(f"\nIncompatible {classifier} Files:")
                report.write(f"## {classifier}\n")
                for file, reason in files:
                    indented_reason = indent(reason, prefix="\t\t")
                    print(f"\t- {file}\n{indented_reason}")
                    report.write(f"- `{file}`: {reason}\n")
                report.write("\n")
        if not has_issues:
            print("All files are good!")
            report.write("No problems found.\n")