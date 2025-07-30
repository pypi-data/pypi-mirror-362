from pydantic import Field, BaseModel, field_validator
from typing import Optional, List, Literal, Tuple
from ara_cli.artefact_models.artefact_model import Artefact, ArtefactType
import re


class ActionItem(BaseModel):
    model_config = {
        "validate_assignment": True
    }

    status: Literal["to-do", "in-progress", "done"] = Field(
        default="to-do",
        description="work status of the action item. Can be 'to-do', 'in-progress' or 'done'"
    )
    text: str = Field(
        ...,
        description="action item text describing the action required"
    )

    @field_validator('status', mode='before')
    def validate_status(cls, v):
        if not v:
            raise ValueError("status must be set in ActionItem. May be one of 'to-do', 'in-progress' or 'done'")
        if v not in ["to-do", "in-progress", "done"]:
            raise ValueError(f"invalid status '{v}'. Allowed values are 'to-do', 'in-progress', 'done'")
        return v

    @field_validator('text', mode='before')
    def validate_text(cls, v):
        if not v:
            raise ValueError("text must be set in ActionItem. Should describe what action is required for the task to be accomplished")
        return v

    @classmethod
    def deserialize(cls, line: str) -> Optional['ActionItem']:
        if not line:
            return None
        match = re.match(r'\[@(to-do|in-progress|done)\]\s+(.*)', line.strip())
        if not match:
            return None
        status, text = match.groups()
        return cls(status=status, text=text)

    def serialize(self) -> str:
        return f"[@{self.status}] {self.text}"


class TaskArtefact(Artefact):
    artefact_type: ArtefactType = ArtefactType.task
    action_items: List[ActionItem] = Field(default_factory=list)

    @classmethod
    def _deserialize_action_items(cls, text) -> Tuple[List[ActionItem], List[str]]:
        lines = [line.strip() for line in text.strip().splitlines() if line.strip()]

        remaining_lines = []
        action_items = []
        for line in lines:
            if line.startswith('[@'):
                action_items.append(ActionItem.deserialize(line))
                continue
            remaining_lines.append(line)
        return action_items, remaining_lines

    @classmethod
    def deserialize(cls, text: str) -> 'TaskArtefact':
        fields = super()._parse_common_fields(text)

        action_items, lines = cls._deserialize_action_items(text)

        fields['action_items'] = action_items

        return cls(**fields)

    @classmethod
    def _title_prefix(cls) -> str:
        return "Task:"

    @classmethod
    def _artefact_type(cls) -> ArtefactType:
        return ArtefactType.task

    def _serialize_action_items(self) -> str:
        action_item_lines = [action_item.serialize() for action_item in self.action_items]
        return "\n".join(action_item_lines)

    def serialize(self) -> str:
        tags = self._serialize_tags()
        title = self._serialize_title()
        contribution = self._serialize_contribution()
        description = self._serialize_description()
        action_items = self._serialize_action_items()

        lines = []
        if tags:
            lines.append(tags)
        lines.append(title)
        lines.append("")
        if contribution:
            lines.append(contribution)
            lines.append("")
        if action_items:
            lines.append(action_items)
            lines.append("")
        lines.append(description)
        lines.append("")

        return "\n".join(lines)
