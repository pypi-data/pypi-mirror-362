from ara_cli.artefact_models.artefact_model import ArtefactType, Artefact, Intent
from typing import List
from pydantic import field_validator, Field


class VisionIntent(Intent):
    for_: str = Field(
        description="Target customer description. Specify the particular group or type of customer that would benefit most from this product—such as young professionals, retirees, or small business owners."
    )
    who: str = Field(
        description="Description of the specific needs or problems the target customer is facing. What challenges do they need to overcome or desires they seek to fulfill?"
    )
    the: str = Field(
        description="Name of the product and its category. What is the product called? Give the official name that makes it easily identifiable. Must contain 'is a' or 'is an' followed by the product category"
    )
    that: str = Field(
        description="Key benefit statement, highlighting the main reason the product is valuable. What compelling benefits does it offer that would make a customer inclined to purchase?"
    )
    unlike: str = Field(
        description="Description of the primary competitive alternative. Identify what existing solutions or competitors are currently available in the market."
    )
    our_product: str = Field(
        description="Statement of primary differentiation. What unique features or qualities does this product have that sets it apart from the competition?"
    )

    @field_validator('for_')
    def validate_for_(cls, v):
        if not v:
            raise ValueError("`for_` field must be set for VisionIntent")
        return v

    @field_validator('who')
    def validate_who(cls, v):
        if not v:
            raise ValueError("`who` field must be set for VisionIntent")
        return v

    @field_validator('the')
    def validate_the(cls, v):
        if not v:
            raise ValueError("`the` field must be set for VisionIntent")
        if "is a " not in v and "is an " not in v:
            raise ValueError(
                "`the` field must contain 'is a ' or 'is an ' substring")
        return v

    @field_validator('that')
    def validate_that(cls, v):
        if not v:
            raise ValueError("`that` field must be set for VisionIntent")
        return v

    @field_validator('unlike')
    def validate_unlike(cls, v):
        if not v:
            raise ValueError("`unlike` field must be set for VisionIntent")
        return v

    @field_validator('our_product')
    def validate_our_product(cls, v):
        if not v:
            raise ValueError(
                "`our_product` field must be set for VisionIntent")
        return v

    def serialize(self):
        lines = []
        lines.append(f"For {self.for_}")
        lines.append(f"Who {self.who}")
        lines.append(f"The {self.the}")
        lines.append(f"That {self.that}")
        lines.append(f"Unlike {self.unlike}")
        lines.append(f"Our product {self.our_product}")

        return "\n".join(lines)

    @classmethod
    def deserialize_from_lines(cls, lines: List[str], start_index: int = 0) -> 'VisionIntent':
        intent_start_index = start_index

        for_ = ""
        who = ""
        the = ""
        that = ""
        unlike = ""
        our_product = ""

        for_prefix = "For "
        who_prefix = "Who "
        the_prefix = "The "
        that_prefix = "That "
        unlike_prefix = "Unlike "
        our_product_prefix = "Our product "

        for i in range(start_index, len(lines)):
            if lines[i].startswith(for_prefix):
                intent_start_index = i
                break

        index = intent_start_index
        if index < len(lines) and lines[index].startswith(for_prefix):
            for_ = lines[index][len(for_prefix):]
            index = index + 1
        if index < len(lines) and lines[index].startswith(who_prefix):
            who = lines[index][len(who_prefix):]
            index = index + 1
        if index < len(lines) and lines[index].startswith(the_prefix):
            the = lines[index][len(the_prefix):]
            index = index + 1
        if index < len(lines) and lines[index].startswith(that_prefix):
            that = lines[index][len(that_prefix):]
            index = index + 1
        if index < len(lines) and lines[index].startswith(unlike_prefix):
            unlike = lines[index][len(unlike_prefix):]
            index = index + 1
        if index < len(lines) and lines[index].startswith(our_product_prefix):
            our_product = lines[index][len(our_product_prefix):]

        return cls(
            for_=for_,
            who=who,
            the=the,
            that=that,
            unlike=unlike,
            our_product=our_product,
        )


class VisionArtefact(Artefact):
    artefact_type: ArtefactType = ArtefactType.vision
    intent: VisionIntent

    @classmethod
    def _title_prefix(cls) -> str:
        return "Vision:"

    @classmethod
    def _artefact_type(cls) -> ArtefactType:
        return ArtefactType.vision

    @classmethod
    def deserialize(cls, text) -> 'VisionArtefact':
        fields = super()._parse_common_fields(text)

        intent = VisionIntent.deserialize(text)

        fields['intent'] = intent

        return cls(**fields)

    def serialize(self) -> str:
        tags = self._serialize_tags()
        title = self._serialize_title()
        contribution = self._serialize_contribution()
        description = self._serialize_description()
        vision_intent = self.intent.serialize()

        lines = []
        if tags:
            lines.append(tags)
        lines.append(title)
        lines.append("")
        if contribution:
            lines.append(contribution)
            lines.append("")
        lines.append(vision_intent)
        lines.append("")
        lines.append(description)
        lines.append("")

        return "\n".join(lines)
