from ara_cli.artefact_models.artefact_model import Artefact, ArtefactType, Intent
from pydantic import Field, field_validator
from typing import List, Tuple


class UserstoryIntent(Intent):
    in_order_to: str = Field(
        description="Summary of the desired benefit or outcome. Describe what goal or result the user seeks to accomplish, focusing on the ultimate advantage they wish to achieve."
    )
    as_a: str = Field(
        description="Identification of the user role. Specify the specific persona or type of user for whom this product or feature is intended, such as a project manager, frequent traveler, or software developer."
    )
    i_want: str = Field(
        description="Description of the desired product behavior or feature. Clarify what specific action, functionality, or service the user requires to achieve their stated benefit, emphasizing how it aligns with their role."
    )

    @field_validator('in_order_to')
    def validate_in_order_to(cls, v):
        if not v:
            raise ValueError("in_order_to must be set for UserstoryIntent")
        return v

    @field_validator('as_a')
    def validate_as_a(cls, v):
        if not v:
            raise ValueError("as_a must be set for UserstoryIntent")
        return v

    @field_validator('i_want')
    def validate_i_want(cls, v):
        if not v:
            raise ValueError("i_want must be set for UserstoryIntent")
        return v

    def serialize(self):
        from ara_cli.artefact_models.serialize_helper import as_a_serializer

        lines = []

        as_a_line = as_a_serializer(self.as_a)

        lines.append(f"In order to {self.in_order_to}")
        lines.append(as_a_line)
        lines.append(f"I want {self.i_want}")

        return "\n".join(lines)

    @classmethod
    def deserialize_from_lines(cls, lines: List[str], start_index: int = 0) -> 'UserstoryIntent':
        in_order_to = None
        as_a = None
        i_want = None

        in_order_to_prefix = "In order to "
        as_a_prefix = "As a "
        as_a_prefix_alt = "As an "
        i_want_prefix = "I want "

        index = start_index
        while index < len(lines) and (not in_order_to or not as_a or not i_want):
            line = lines[index].strip()
            if line.startswith(in_order_to_prefix) and not in_order_to:
                in_order_to = line[len(in_order_to_prefix):].strip()
            elif line.startswith(as_a_prefix) and not as_a:
                as_a = line[len(as_a_prefix):].strip()
            elif line.startswith(as_a_prefix_alt) and not as_a:
                as_a = line[len(as_a_prefix_alt):].strip()
            elif line.startswith(i_want_prefix) and not i_want:
                i_want = line[len(i_want_prefix):].strip()
            index += 1

        if not in_order_to:
            raise ValueError("Could not find 'In order to' line")
        if not as_a:
            raise ValueError("Could not find 'As a' line")
        if not i_want:
            raise ValueError("Could not find 'I want' line")

        return cls(
            in_order_to=in_order_to,
            as_a=as_a,
            i_want=i_want
        )


class UserstoryArtefact(Artefact):
    artefact_type: ArtefactType = ArtefactType.userstory
    intent: UserstoryIntent
    estimate: str = Field(
        ...,
        description="Estimate of effort, usually in story points"
    )
    rules: List[str] = Field(
        default_factory=list,
        description="Rules the userstory defines. It is recommended to create rules to clarify the desired outcome")

    @field_validator('artefact_type')
    def validate_artefact_type(cls, v):
        if v != ArtefactType.userstory:
            raise ValueError(
                f"UserstoryArtefact must have artefact_type of '{ArtefactType.userstory}', not '{v}'")
        return v

    @field_validator('rules')
    def validate_rules(cls, v):    # pragma: no cover
        return v

    @classmethod
    def _title_prefix(cls) -> str:
        return "Userstory:"

    @classmethod
    def _artefact_type(cls) -> ArtefactType:
        return ArtefactType.userstory

    @classmethod
    def _deserialize_rules(cls, lines) -> Tuple[List[str], List[str]]:
        rules = []
        remaining_lines = []
        rule_line_start = "Rule: "
        for line in lines:
            if line.startswith(rule_line_start):
                rules.append(line[len(rule_line_start):])
                continue
            remaining_lines.append(line)
        return rules, remaining_lines

    @classmethod
    def _deserialize_estimate(cls, lines) -> Tuple[str, List[str]]:
        remaining_lines = []
        estimate = ""
        estimate_prefix = "Estimate: "
        for line in lines:
            if line.startswith(estimate_prefix):
                estimate = line[len(estimate_prefix):]
                continue
            remaining_lines.append(line)
        return estimate, remaining_lines

    @classmethod
    def deserialize(cls, text: str) -> 'UserstoryArtefact':
        fields = super()._parse_common_fields(text)

        intent = UserstoryIntent.deserialize(text)

        lines = [line.strip()
                 for line in text.strip().splitlines() if line.strip()]
        estimate, lines = cls._deserialize_estimate(lines)
        rules, lines = cls._deserialize_rules(lines)

        fields['intent'] = intent
        fields['estimate'] = estimate
        fields['rules'] = rules

        return cls(**fields)

    def _serialize_estimate(self) -> str:
        return f"Estimate: {self.estimate}"

    def _serialize_rules(self) -> str:
        if not self.rules:
            return None
        rules = [f"Rule: {rule}" for rule in self.rules]
        return '\n'.join(rules)

    def serialize(self) -> str:
        tags = self._serialize_tags()
        title = self._serialize_title()
        contribution = self._serialize_contribution()
        estimate = self._serialize_estimate()
        description = self._serialize_description()
        intent = self.intent.serialize()
        rules = self._serialize_rules()

        lines = []
        if self.tags:
            lines.append(tags)
        lines.append(title)
        lines.append("")
        lines.append(contribution)
        lines.append("")
        lines.append(estimate)
        lines.append("")
        if self.intent:
            lines.append(intent)
            lines.append("")
        if rules:
            lines.append(rules)
            lines.append("")
        lines.append(description)
        lines.append("")

        return '\n'.join(lines)
