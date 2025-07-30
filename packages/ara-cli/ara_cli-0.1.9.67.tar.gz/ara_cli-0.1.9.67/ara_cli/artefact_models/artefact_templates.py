from ara_cli.artefact_models.artefact_model import ArtefactType, Artefact
from ara_cli.artefact_models.vision_artefact_model import VisionArtefact, VisionIntent
from ara_cli.artefact_models.businessgoal_artefact_model import BusinessgoalArtefact, BusinessgoalIntent
from ara_cli.artefact_models.capability_artefact_model import CapabilityArtefact, CapabilityIntent
from ara_cli.artefact_models.epic_artefact_model import EpicArtefact, EpicIntent
from ara_cli.artefact_models.userstory_artefact_model import UserstoryArtefact, UserstoryIntent
from ara_cli.artefact_models.example_artefact_model import ExampleArtefact
from ara_cli.artefact_models.keyfeature_artefact_model import KeyfeatureArtefact, KeyfeatureIntent
from ara_cli.artefact_models.feature_artefact_model import FeatureArtefact, FeatureIntent, Scenario, ScenarioOutline, Example
from ara_cli.artefact_models.task_artefact_model import TaskArtefact
from ara_cli.artefact_models.issue_artefact_model import IssueArtefact


def _default_vision(title: str) -> VisionArtefact:
    intent = VisionIntent(
        for_="<target customer>",
        who="<needs something>",
        the="<product name> is a <product category>",
        that="<key benefit, compelling reason to buy>",
        unlike="<primary competitive alternative>",
        our_product="<statement of primary differentiation>"
    )
    return VisionArtefact(
        tags=["sample_tag"],
        title=title,
        description="<further optional description to understand the vision, markdown capable text formatting>",
        intent=intent
    )


def _default_businessgoal(title: str) -> BusinessgoalArtefact:
    intent = BusinessgoalIntent(
        in_order_to="<reach primarily a monetary business goal>",
        as_a="<business related role>",
        i_want="<something that helps me to reach my monetary goal>"
    )
    return BusinessgoalArtefact(
        tags=["sample_tag"],
        title=title,
        description="<further optional description to understand the vision, markdown capable text formatting>",
        intent=intent
    )


def _default_capability(title: str) -> CapabilityArtefact:
    intent = CapabilityIntent(
        in_order_to="<reach primarily a monetary business goal>",
        as_a="<business related role>",
        to_be_able_to="<something that helps me to reach my monetary goal>"
    )
    return CapabilityArtefact(
        tags=["sample_tag"],
        title=title,
        description="<further optional description to understand the capability, markdown capable text formatting>",
        intent=intent
    )


def _default_epic(title: str) -> EpicArtefact:
    intent = EpicIntent(
        in_order_to="<achieve a benefit>",
        as_a="<(user) role>",
        i_want="<a certain product behavior>"
    )
    rules = [
        "<rule needed to fulfill the wanted product behavior>",
        "<rule needed to fulfill the wanted product behavior>",
        "<rule needed to fulfill the wanted product behavior>"
    ]
    return EpicArtefact(
        tags=["sample_tag"],
        title=title,
        description="<further optional description to understand the vision, markdown capable text formatting>",
        intent=intent,
        rules=rules
    )


def _default_userstory(title: str) -> UserstoryArtefact:
    intent = UserstoryIntent(
        in_order_to="<achieve a benefit>",
        as_a="<(user) role>",
        i_want="<a certain product behavior>"
    )
    rules = [
        "<rule needed to fulfill the wanted product behavior>",
        "<rule needed to fulfill the wanted product behavior>",
        "<rule needed to fulfill the wanted product behavior>"
    ]
    return UserstoryArtefact(
        tags=["sample_tag"],
        title=title,
        description="<further optional description to understand the userstory, markdown capable text formatting>",
        intent=intent,
        rules=rules,
        estimate="<story points, scale?>"
    )


def _default_example(title: str) -> ExampleArtefact:
    return ExampleArtefact(
        tags=["sample_tag"],
        title=title,
        description="<further optional description to understand the example, markdown capable text formatting>",
    )


def _default_keyfeature(title: str) -> KeyfeatureArtefact:
    intent = KeyfeatureIntent(
        in_order_to="<support a capability or business goal>",
        as_a="<main stakeholder who will benefit>",
        i_want="<a product feature that helps me doing something so that I can achieve my named goal>"
    )
    description = """<further optional description to understand the capability, markdown capable text formatting, best practice is using
    GIVEN any precondition
    AND another precondition
    WHEN some action takes place
    THEN some result is to be expected
    AND some other result is to be expected>"""
    return KeyfeatureArtefact(
        tags=["sample_tag"],
        title=title,
        description=description,
        intent=intent
    )


def _default_feature(title: str) -> FeatureArtefact:
    intent = FeatureIntent(
        as_a="<user>",
        i_want_to="<do something | need something>",
        so_that="<I can achieve something>"
    )
    scenarios = [
        Scenario(
            title="<descriptive_scenario_title>",
            steps=[
                "Given <precondition>",
                "When <action>",
                "Then <expected result>"
            ],
        ),
        ScenarioOutline(
            title="<descriptive scenario title>",
            steps=[
                "Given <precondition>",
                "When <action>",
                "Then <expected result>"
            ],
            examples=[
                Example(
                    title=None,
                    values={
                        "descriptive scenario title": "<example title 1>",
                        "precondition": "<example precond. 1>",
                        "action": "<example action 1>",
                        "expected result": "<example result 1>"
                    }
                ),
                Example(
                    title=None,
                    values={
                        "descriptive scenario title": "<example title 2>",
                        "precondition": "<example precond. 2>",
                        "action": "<example action 2>",
                        "expected result": "<example result 2>"
                    }
                )
            ]
        )
    ]
    description = """<further optional description to understand
  the rule, no format defined, the example artefact is only a placeholder>"""

    return FeatureArtefact(
        tags=["sample_tag"],
        title=title,
        description=description,
        intent=intent,
        scenarios=scenarios
    )


def _default_task(title: str) -> TaskArtefact:
    return TaskArtefact(
        status="to-do",
        title=title,
        description="<further optional description to understand the task, no format defined>"
    )


def _default_issue(title: str) -> IssueArtefact:
    description = "<further free text description to understand the issue, no format defined>"
    additional_description = """*Optional descriptions of the issue in Gherkin style*

    Given <descriptive text of the starting conditions where the issue occurs>
    When <action under which the issues occurs>
    Then <resulting behavior in contrast to the expected behavior>

    *or optional free text description*"""

    return IssueArtefact(
        tags=["sample_tag"],
        title=title,
        description=description,
        additional_description=additional_description
    )


def template_artefact_of_type(artefact_type: ArtefactType, title: str) -> Artefact:
    default_creation_functions = {
        ArtefactType.vision: _default_vision,
        ArtefactType.businessgoal: _default_businessgoal,
        ArtefactType.capability: _default_capability,
        ArtefactType.epic: _default_epic,
        ArtefactType.userstory: _default_userstory,
        ArtefactType.example: _default_example,
        ArtefactType.keyfeature: _default_keyfeature,
        ArtefactType.feature: _default_feature,
        ArtefactType.task: _default_task,
        ArtefactType.issue: _default_issue
    }

    return default_creation_functions[artefact_type](title)
