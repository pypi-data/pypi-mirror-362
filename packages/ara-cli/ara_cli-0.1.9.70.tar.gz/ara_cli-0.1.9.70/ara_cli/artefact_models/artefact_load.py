from ara_cli.artefact_models.artefact_mapping import title_prefix_to_artefact_class


def artefact_from_content(content):
    relevant_lines = content.splitlines()[:2]
    for line in relevant_lines:
        for prefix, artefact_class in title_prefix_to_artefact_class.items():
            if line.strip().startswith(prefix):
                return artefact_class.deserialize(content)
    return None
