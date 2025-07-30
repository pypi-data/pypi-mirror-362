import os
from ara_cli.list_filter import ListFilter, filter_list
from ara_cli.artefact_lister import ArtefactLister


class TagExtractor:
    def __init__(self, file_system=None):
        self.file_system = file_system or os

    def extract_tags(
        self,
        navigate_to_target=False,
        filtered_extra_column=False,
        list_filter: ListFilter | None = None
    ):
        from ara_cli.template_manager import DirectoryNavigator
        from ara_cli.artefact_reader import ArtefactReader

        navigator = DirectoryNavigator()
        if navigate_to_target:
            navigator.navigate_to_target()

        artefacts = ArtefactReader.read_artefacts()

        filtered_artefacts = filter_list(
            list_to_filter=artefacts,
            list_filter=list_filter,
            content_retrieval_strategy=ArtefactLister.artefact_content_retrieval,
            file_path_retrieval=ArtefactLister.artefact_path_retrieval,
            tag_retrieval=ArtefactLister.artefact_tags_retrieval
        )

        unique_tags = set()

        if filtered_extra_column:
            status_tags = {"to-do", "in-progress", "review", "done", "closed"}
            artefacts_to_process = []

            for artefact_list in filtered_artefacts.values():
                for artefact in artefact_list:
                    tags = artefact.tags + \
                        [artefact.status] if artefact.status else artefact.tags
                    tag_set = set(tag for tag in tags if tag is not None)
                    if not tag_set & status_tags:
                        artefacts_to_process.append(artefact)

            for artefact in artefacts_to_process:
                tags = [tag for tag in (
                    artefact.tags + [artefact.status]) if tag is not None]
                for tag in tags:
                    if (
                        tag in status_tags
                        or tag.startswith("priority_")
                        or tag.startswith("user_")
                    ):
                        continue
                    unique_tags.add(tag)

        else:
            for artefact_list in filtered_artefacts.values():
                for artefact in artefact_list:
                    user_tags = [f"user_{tag}" for tag in artefact.users]
                    tags = [tag for tag in (artefact.tags + [artefact.status] + user_tags) if tag is not None]
                    unique_tags.update(tags)

        sorted_tags = sorted(unique_tags)
        return sorted_tags
