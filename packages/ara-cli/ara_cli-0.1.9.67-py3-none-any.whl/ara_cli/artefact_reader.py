from ara_cli.classifier import Classifier
from ara_cli.file_classifier import FileClassifier
from ara_cli.artefact_models.artefact_model import Artefact
from ara_cli.artefact_models.artefact_load import artefact_from_content
from ara_cli.artefact_fuzzy_search import suggest_close_name_matches_for_parent, suggest_close_name_matches
from typing import Dict, List
import os
import re


class ArtefactReader:
    @staticmethod
    def read_artefact(artefact_name, classifier) -> tuple[str, dict[str, str]]:
        if not Classifier.is_valid_classifier(classifier):
            print("Invalid classifier provided. Please provide a valid classifier.")
            return None, None

        file_classifier = FileClassifier(os)
        classified_file_info = file_classifier.classify_files()
        artefact_info_of_classifier = classified_file_info.get(classifier, [])

        for artefact_info in artefact_info_of_classifier:
            file_path = artefact_info["file_path"]
            artefact_title = artefact_info["title"]
            if artefact_title == artefact_name:
                with open(file_path, 'r') as file:
                    content = file.read()
                return content, artefact_info

        all_artefact_names = [info["title"] for info in artefact_info_of_classifier]
        suggest_close_name_matches(
            artefact_name,
            all_artefact_names
        )

        return None, None

    @staticmethod
    def read_single_artefact(artefact_name, classifier, classified_file_info=None) -> Artefact:
        if not Classifier.is_valid_classifier(classifier):
            print("Invalid classifier provided. Please provide a valid classifier.")
            return None
        if not classified_file_info:
            file_classifier = FileClassifier(os)
            classified_file_info = file_classifier.classify_files()
        artefact_info_of_classifier = classified_file_info.get(classifier, [])

        for artefact_info in artefact_info_of_classifier:
            file_path = artefact_info["file_path"]
            artefact_title = artefact_info["title"]
            if artefact_title == artefact_name:
                with open(file_path, 'r') as file:
                    content = file.read()
                artefact = artefact_from_content(content)
                artefact._file_path = file_path
                return artefact
        return None

    @staticmethod
    def extract_parent_tree(artefact_content):
        artefact_titles = Classifier.artefact_titles()
        title_segment = '|'.join(artefact_titles)

        regex_pattern = rf'(?:Contributes to|Illustrates)\s*:*\s*(.*)\s+({title_segment}).*'
        regex = re.compile(regex_pattern)
        match = re.search(regex, artefact_content)
        if not match:
            return None, None

        parent_name = match.group(1).strip()
        parent_type = match.group(2).strip()

        return parent_name, parent_type

    @staticmethod
    def merge_dicts(dict1, dict2):
        from collections import defaultdict

        merged = defaultdict(list)
        for d in [dict1, dict2]:
            for key, artefacts in d.items():
                merged[key].extend(artefacts)
        return dict(merged)

    @staticmethod
    def read_artefacts(classified_artefacts=None, file_system=os, tags=None) -> Dict[str, List[Artefact]]:
        from ara_cli.artefact_models.artefact_load import artefact_from_content

        if classified_artefacts is None:
            file_classifier = FileClassifier(file_system)
            classified_artefacts = file_classifier.classify_files()

        artefacts = {artefact_type: []
                     for artefact_type in classified_artefacts.keys()}
        for artefact_type, artefact_info_dicts in classified_artefacts.items():
            for artefact_info in artefact_info_dicts:
                try:
                    with open(artefact_info["file_path"], 'r') as file:
                        content = file.read()
                    artefact = artefact_from_content(content)
                    if not artefact:
                        continue
                    # Store the full file path in the artefact
                    artefact._file_path = artefact_info["file_path"]
                    artefacts[artefact_type].append(artefact)
                    # else:
                        # Include file path if deserialization fails
                        # FIXME: LOOK INTO IT
                        # artefacts[artefact_type].append(file_path)
                except Exception:
                    # TODO: catch only specific exceptions
                    # TODO: implament error message for deserialization or "ara scan" or "ara autofix"
                    # print(f"Warning: Could not deserialize artefact at {artefact_info}: {e}")
                    # artefacts[artefact_type].append(file_path)
                    continue
        return artefacts

    @staticmethod
    def find_children(artefact_name, classifier, artefacts_by_classifier={}, classified_artefacts=None):
        artefacts_by_classifier = artefacts_by_classifier or {}
        filtered_artefacts = {k: [] for k in artefacts_by_classifier.keys()}

        if classified_artefacts is None:
            classified_artefacts = ArtefactReader.read_artefacts()

        for artefact_classifier, artefacts in classified_artefacts.items():
            for artefact in artefacts:
                if not isinstance(artefact, Artefact):
                    continue

                try:
                    contribution = artefact.contribution
                    if (contribution and
                        contribution.artefact_name == artefact_name and
                            contribution.classifier == classifier):

                        file_classifier = artefact._file_path.split('.')[-1]

                        if file_classifier not in filtered_artefacts:
                            filtered_artefacts[file_classifier] = []
                        filtered_artefacts[file_classifier].append(artefact)

                except AttributeError as e:
                    continue

        return ArtefactReader.merge_dicts(artefacts_by_classifier, filtered_artefacts)

    @staticmethod
    def step_through_value_chain(
            artefact_name,
            classifier,
            artefacts_by_classifier={},
            classified_artefacts: dict[str, list[Artefact]] | None = None
    ):
        from ara_cli.artefact_models.artefact_load import artefact_from_content

        if classified_artefacts is None:
            classified_artefacts = ArtefactReader.read_artefacts()

        if classifier not in artefacts_by_classifier:
            artefacts_by_classifier[classifier] = []

        artefact = next(filter(
            lambda x: x.title == artefact_name, classified_artefacts[classifier]
        ))

        if not artefact:
            return
        if artefact in artefacts_by_classifier[classifier]:
            return

        artefacts_by_classifier[classifier].append(artefact)

        parent = artefact.contribution
        if parent and parent.artefact_name and parent.classifier:
            parent_name = parent.artefact_name
            parent_classifier = parent.classifier

            parent_classifier_artefacts = classified_artefacts[parent_classifier]
            all_artefact_names = [x.title for x in parent_classifier_artefacts]

            if parent_name not in all_artefact_names:
                if parent_name is not None:
                    suggest_close_name_matches_for_parent(
                        artefact_name,
                        all_artefact_names,
                        parent_name
                    )
                print()
                return

            ArtefactReader.step_through_value_chain(
                artefact_name=parent_name,
                classifier=parent_classifier,
                artefacts_by_classifier=artefacts_by_classifier,
                classified_artefacts=classified_artefacts
            )
