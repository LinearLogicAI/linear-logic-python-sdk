from ast import Dict
from dataclasses import dataclass, field
from typing import List
from linlog.constants import (
    PROJECT_ATTRIBUTE_ALLOW_MULTIPLE_KEY,
    PROJECT_ATTRIBUTE_ID_KEY,
    PROJECT_ATTRIBUTE_KEY_KEY,
    PROJECT_ATTRIBUTE_OPTIONS_KEY,
    PROJECT_ATTRIBUTE_TYPE_KEY,
    PROJECT_ATTRIBUTE_IS_GLOBAL_KEY
)


class AttributeType:

    Binary = 'binary'
    Categorical = 'categorical'
    Text = 'text'
    DirectionalVector = 'directional_vector'
    InstanceID = 'id'


@dataclass
class ProjectAttribute:
    id: str
    key: str
    attribute_type: str
    is_global: bool

    # applicable to categorical attributes only
    allow_multiple: bool = False
    options: List[str] = field(default_factory=list)

    @classmethod
    def from_json(cls, payload: dict) -> 'ProjectAttribute':
        return cls(
            id=payload.get(PROJECT_ATTRIBUTE_ID_KEY, None),
            key=payload.get(PROJECT_ATTRIBUTE_KEY_KEY, None),
            attribute_type=payload.get(PROJECT_ATTRIBUTE_TYPE_KEY, None),
            is_global=payload.get(PROJECT_ATTRIBUTE_IS_GLOBAL_KEY, False),
            allow_multiple=payload
                .get(PROJECT_ATTRIBUTE_ALLOW_MULTIPLE_KEY, False),
            options=payload.get(PROJECT_ATTRIBUTE_OPTIONS_KEY, []),
        )

    def to_dict(self) -> Dict:
        return {
            PROJECT_ATTRIBUTE_ID_KEY: self.id,
            PROJECT_ATTRIBUTE_KEY_KEY: self.key,
            PROJECT_ATTRIBUTE_TYPE_KEY: self.attribute_type,
            PROJECT_ATTRIBUTE_IS_GLOBAL_KEY: self.is_global,
            PROJECT_ATTRIBUTE_ALLOW_MULTIPLE_KEY: self.allow_multiple,
            PROJECT_ATTRIBUTE_OPTIONS_KEY: self.options
        }

    def __eq__(self, other: 'ProjectAttribute') -> bool:
        return self.id == other.id \
            and self.key == other.key \
            and self.attribute_type == other.attribute_type \
            and self.is_global == other.is_global \
            and len(self.options) == len(other.options)
