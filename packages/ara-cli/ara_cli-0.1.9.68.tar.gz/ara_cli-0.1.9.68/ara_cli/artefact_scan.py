from textwrap import indent
import os


def check_file(file_path, artefact_class):
    from pydantic import ValidationError
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except OSError as e:
        return False, f"File error: {e}"
    try:
        artefact_instance = artefact_class.deserialize(content)

        base_name = os.path.basename(file_path)
        file_name_without_ext, _ = os.path.splitext(base_name)

        if artefact_instance.title != file_name_without_ext:
            reason = (f"Filename-Title Mismatch: The file name '{file_name_without_ext}' "
                      f"does not match the artefact title '{artefact_instance.title}'.")
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
        is_valid, reason = check_file(artefact_info["file_path"], artefact_class)
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