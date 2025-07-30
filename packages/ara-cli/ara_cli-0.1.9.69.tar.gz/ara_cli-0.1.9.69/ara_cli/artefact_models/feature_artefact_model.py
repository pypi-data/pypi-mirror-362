from pydantic import BaseModel, field_validator, model_validator, Field
from typing import List, Dict, Tuple, Union, Optional
from ara_cli.artefact_models.artefact_model import Artefact, ArtefactType, Intent
import re


class FeatureIntent(Intent):
    as_a: str = Field(
        description="Role or identity of the user. Specify who is interacting with the product or feature—for example, a project manager, or a student."
    )
    i_want_to: str = Field(
        description="Specific action or need of the user. Outline what the user is looking to accomplish or the problem they are trying to solve. What task or goal motivates their interaction with the product?"
    )
    so_that: str = Field(
        description="The desired outcome or benefit the user wishes to attain. What is the ultimate result they are hoping to achieve by using the product or feature? This should highlight the end benefit or solution provided."
    )

    @field_validator('as_a')
    def validate_in_order_to(cls, v):
        if not v:
            raise ValueError("as_a must be set for FeatureIntent")
        return v

    @field_validator('i_want_to')
    def validate_as_a(cls, v):
        if not v:
            raise ValueError("i_want_to must be set for FeatureIntent")
        return v

    @field_validator('so_that')
    def validate_i_want(cls, v):
        if not v:
            raise ValueError("so_that must be set for FeatureIntent")
        return v

    def serialize(self):
        from ara_cli.artefact_models.serialize_helper import as_a_serializer

        lines = []

        as_a_line = as_a_serializer(self.as_a)

        lines.append(as_a_line)
        lines.append(f"I want to {self.i_want_to}")
        lines.append(f"So that {self.so_that}")

        return "\n".join(lines)

    @classmethod
    def deserialize_from_lines(cls, lines: List[str], start_index: int = 0) -> 'FeatureIntent':
        as_a = None
        i_want_to = None
        so_that = None

        as_a_prefix = "As a "
        as_a_prefix_alt = "As an "
        i_want_to_prefix = "I want to "
        so_that_prefix = "So that "

        index = start_index
        while index < len(lines) and (not as_a or not i_want_to or not so_that):
            line = lines[index]
            if line.startswith(as_a_prefix) and not as_a:
                as_a = line[len(as_a_prefix):].strip()
            if line.startswith(as_a_prefix_alt) and not as_a:
                as_a = line[len(as_a_prefix_alt):].strip()
            if line.startswith(i_want_to_prefix) and not i_want_to:
                i_want_to = line[len(i_want_to_prefix):].strip()
            if line.startswith(so_that_prefix) and not so_that:
                so_that = line[len(so_that_prefix):].strip()
            index += 1

        if not as_a:
            raise ValueError("Could not find 'As a' line")
        if not i_want_to:
            raise ValueError("Could not find 'I want to' line")
        if not so_that:
            raise ValueError("Could not find 'So that' line")

        return cls(
            as_a=as_a,
            i_want_to=i_want_to,
            so_that=so_that
        )


class Example(BaseModel):
    values: Dict[str, str] = Field(
        description="A set of placeholder names and their values from the example row, used to fill in the scenario outline’s steps."
    )

    @classmethod
    def from_row(cls, headers: List[str], row: List[str]) -> 'Example':
        if len(row) != len(headers):
            raise ValueError(
                f"Row has {len(row)} cells, but expected {len(headers)}.\nFound row: {row}")
        values = {header: value.strip() for header, value in zip(headers, row)}
        return cls(values=values)


class Background(BaseModel):
    steps: List[str] = Field(
        description="A list of Gherkin 'Given' type steps that describe what the background does."
    )

    @field_validator('steps', mode='before')
    def validate_steps(cls, v: List[str]) -> List[str]:
        """Ensure steps are non-empty and stripped."""
        steps = [step.strip() for step in v if step.strip()]
        if not steps:
            raise ValueError("steps list must not be empty")
        return steps

    @classmethod
    def from_lines(cls, lines: List[str], start_idx: int) -> Tuple['Background', int]:
        """Parse a Background from a list of lines starting at start_idx."""
        if not lines[start_idx].startswith('Background:'):
            raise ValueError("Expected 'Background:' at start index")

        steps = []
        idx = start_idx + 1
        while idx < len(lines) and not lines[idx].startswith('Background:'):
            step = lines[idx].strip()
            if step:
                steps.append(step)
            idx += 1
        return cls(steps=steps), idx


class Scenario(BaseModel):
    title: str = Field(
        description="The name of the scenario, giving a short summary of the test case. It comes from the 'Scenario:' line in the feature file."
    )
    steps: List[str] = Field(
        description="A list of Gherkin steps (like 'Given', 'When', 'Then') that describe what the scenario does."
    )

    @field_validator('title')
    def validate_title(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("title must not be empty")
        return v

    @field_validator('steps', mode='before')
    def validate_steps(cls, v: List[str]) -> List[str]:
        """Ensure steps are non-empty and stripped."""
        steps = [step.strip() for step in v if step.strip()]
        if not steps:
            raise ValueError("steps list must not be empty")
        return steps

    @classmethod
    def from_lines(cls, lines: List[str], start_idx: int) -> Tuple['Scenario', int]:
        """Parse a Scenario from a list of lines starting at start_idx."""
        if not lines[start_idx].startswith('Scenario:'):
            raise ValueError("Expected 'Scenario:' at start index")
        title = lines[start_idx][len('Scenario:'):].strip()
        steps = []
        idx = start_idx + 1
        while idx < len(lines) and not (lines[idx].startswith('Scenario:') or lines[idx].startswith('Scenario Outline:')):
            step = lines[idx].strip()
            if step:
                steps.append(step)
            idx += 1
        return cls(title=title, steps=steps), idx


class ScenarioOutline(BaseModel):
    title: str = Field(
        description="The name of the scenario outline, summarizing the test case that uses placeholders. It comes from the 'Scenario Outline:' line in the feature file."
    )
    steps: List[str] = Field(
        description="A list of Gherkin steps with placeholders (like '<name>'), which get filled in by example values."
    )
    examples: List[Example] = Field(
        description="A list of examples that provide values for the placeholders in the steps, sometimes with an optional title for clarity."
    )

    @field_validator('title')
    def validate_title(cls, v: str) -> str:
        if not v:
            raise ValueError("title must not be empty in a ScenarioOutline")
        return v

    @field_validator('steps', mode='before')
    def validate_steps(cls, v: List[str]) -> List[str]:
        if not v:
            raise ValueError("steps list must not be empty in a ScenarioOutline")
        return v

    @field_validator('examples')
    def validate_examples(cls, v: List[Example]) -> List[Example]:
        if not v:
            raise ValueError("examples must not be empty in a ScenarioOutline")
        return v

    @model_validator(mode='after')
    def check_placeholders(cls, values: 'ScenarioOutline') -> 'ScenarioOutline':
        """Ensure all placeholders in steps have corresponding values in examples."""
        placeholders = set()
        for step in values.steps:
            found = re.findall(r'<([^>]+)>', step)
            placeholders.update(found)
        for example in values.examples:
            missing = placeholders - set(example.values.keys())
            if missing:
                raise ValueError(
                    f"Example is missing values for placeholders: {missing}")
        return values

    @classmethod
    def from_lines(cls, lines: List[str], start_idx: int) -> Tuple['ScenarioOutline', int]:
        """Parse a ScenarioOutline from a list of lines starting at start_idx."""

        if not lines[start_idx].startswith('Scenario Outline:'):
            raise ValueError("Expected 'Scenario Outline:' at start index")
        title = lines[start_idx][len('Scenario Outline:'):].strip()
        steps = []
        idx = start_idx + 1
        while idx < len(lines) and not lines[idx].strip().startswith('Examples:'):
            if lines[idx].strip():
                steps.append(lines[idx].strip())
            idx += 1
        examples = []
        if idx < len(lines) and lines[idx].strip() == 'Examples:':
            idx += 1
            headers = [h.strip() for h in lines[idx].split('|') if h.strip()]
            idx += 1
            while idx < len(lines) and lines[idx].strip():
                if lines[idx].strip().startswith("Scenario:") or lines[idx].strip().startswith("Scenario Outline:"):
                    break
                row = [cell.strip()
                       for cell in lines[idx].split('|') if cell.strip()]
                example = Example.from_row(headers, row)
                examples.append(example)
                idx += 1
        return cls(title=title, steps=steps, examples=examples), idx


class FeatureArtefact(Artefact):
    artefact_type: ArtefactType = ArtefactType.feature
    intent: FeatureIntent
    scenarios: List[Union[Scenario, ScenarioOutline]] = Field(default=None)
    background: Optional[Background] = Field(
        default=None, description="Highly optional background Gherkin steps for Feature Artefacts. This steps apply for all scenarios and scenario outlines in this feature file.")

    @field_validator('artefact_type')
    def validate_artefact_type(cls, v):
        if v != ArtefactType.feature:
            raise ValueError(
                f"FeatureArtefact must have artefact_type of '{ArtefactType.feature}', not '{v}'")
        return v

    @classmethod
    def _title_prefix(cls) -> str:
        return "Feature:"

    @classmethod
    def _artefact_type(cls) -> ArtefactType:
        return ArtefactType.feature

    def _serialize_background(self) -> str:
        """Helper method to dispatch background serialization."""
        if not self.background:
            return ""
        lines = []
        lines.append("  Background:")
        for step in self.background.steps:
            lines.append(f"    {step}")
        return "\n".join(lines)

    def _serialize_scenario(self, scenario: Union[Scenario, ScenarioOutline]) -> str:
        """Helper method to dispatch scenario serialization."""
        if isinstance(scenario, Scenario):
            return self._serialize_regular_scenario(scenario)
        elif isinstance(scenario, ScenarioOutline):
            return self._serialize_scenario_outline(scenario)
        else:   # pragma: no cover
            raise ValueError("Unknown scenario type")

    def _serialize_regular_scenario(self, scenario: Scenario) -> str:
        """Serialize a regular Scenario."""
        lines = []
        lines.append(f"  Scenario: {scenario.title}")
        for step in scenario.steps:
            lines.append(f"    {step}")
        return "\n".join(lines)

    def _serialize_scenario_outline(self, scenario: ScenarioOutline) -> str:
        """Serialize a ScenarioOutline with aligned examples."""
        lines = []
        lines.append(f"  Scenario Outline: {scenario.title}")
        for step in scenario.steps:
            lines.append(f"    {step}")

        if scenario.examples:
            headers = self._extract_placeholders(scenario.steps)

            rows = [headers]

            # Build rows for each example
            for example in scenario.examples:
                row = [str(example.values.get(ph, "")) for ph in headers]
                rows.append(row)

            # Calculate column widths for alignment
            column_widths = [max(len(str(row[i])) for row in rows)
                             for i in range(len(headers))]

            # Format rows with padding
            formatted_rows = []
            for row in rows:
                padded = [str(cell).ljust(width)
                          for cell, width in zip(row, column_widths)]
                formatted_rows.append("| " + " | ".join(padded) + " |")

            lines.append("")
            lines.append("    Examples:")
            for formatted_row in formatted_rows:
                lines.append(f"      {formatted_row}")

        return "\n".join(lines)

    def _extract_placeholders(self, steps):
        placeholders = []
        for step in steps:
            found = re.findall(r'<([^>]+)>', step)
            for ph in found:
                if ph not in placeholders:
                    placeholders.append(ph)
        return placeholders

    def serialize(self) -> str:
        tags = self._serialize_tags()
        title = self._serialize_title()
        contribution = self._serialize_contribution()
        description = self._serialize_description()
        intent = self.intent.serialize()

        lines = []
        if tags:
            lines.append(tags)
        lines.append(title)
        lines.append("")
        lines.append(intent)
        lines.append("")
        lines.append(contribution)
        lines.append("")
        lines.append(description)
        lines.append("")

        if self.background:
            lines.append(self._serialize_background())
            lines.append("")

        if self.scenarios:
            for scenario in self.scenarios:
                lines.append(self._serialize_scenario(scenario))
                lines.append("")

        return "\n".join(lines)

    @classmethod
    def deserialize(cls, text: str) -> 'FeatureArtefact':
        fields = super()._parse_common_fields(text)

        intent = FeatureIntent.deserialize(text)
        background = cls.deserialize_background(text)
        scenarios = cls.deserialize_scenarios(text)

        fields['scenarios'] = scenarios
        fields['background'] = background
        fields['intent'] = intent

        return cls(**fields)

    @classmethod
    def deserialize_scenarios(cls, text):
        lines = [line.strip()
                 for line in text.strip().splitlines() if line.strip()]

        scenarios = []
        idx = 0
        while idx < len(lines):
            line = lines[idx].strip()
            if line.startswith('Scenario:'):
                scenario, next_idx = Scenario.from_lines(lines, idx)
                scenarios.append(scenario)
                idx = next_idx
            elif line.startswith('Scenario Outline:'):
                scenario, next_idx = ScenarioOutline.from_lines(lines, idx)
                scenarios.append(scenario)
                idx = next_idx
            else:
                idx += 1
        return scenarios

    @classmethod
    def deserialize_background(cls, text):
        lines = [line.strip()
                 for line in text.strip().splitlines() if line.strip()]

        background = None
        idx = 0
        while idx < len(lines):
            line = lines[idx].strip()
            if line.startswith('Background:'):
                background, next_idx = Background.from_lines(lines, idx)
                break
            else:
                idx += 1
        return background
