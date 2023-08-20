from ast import Dict
from linlog import LinLogClient
from dataclasses import dataclass
from typing import List
from linlog.constants import (
    ORGANISATION_ID_KEY,
    ORGANISATION_MEMBERS_KEY,
    ORGANISATION_NAME_KEY,
    ORGANISATION_SUBSCRIPTION_KEY
)


@dataclass
class Member:

    id: str
    groups: List[str]
    invitation: str
    role: str
    user: int


@dataclass
class Organisation:

    id: str
    name: str
    subscription: str
    members: List[Member]

    @classmethod
    def from_json(cls, payload: dict) -> 'Organisation':
        return cls(
            id=payload.get(ORGANISATION_ID_KEY, None),
            name=payload.get(ORGANISATION_NAME_KEY, None),
            subscription=payload.get(ORGANISATION_SUBSCRIPTION_KEY, None),
            members=[
                Member.from_json(x) for x in
                payload.get(ORGANISATION_MEMBERS_KEY, [])
            ],
        )

    def to_dict(self) -> Dict:
        return {
            ORGANISATION_ID_KEY: self.id,
            ORGANISATION_NAME_KEY: self.name,
            ORGANISATION_SUBSCRIPTION_KEY: self.subscription
        }

    @classmethod
    def get(cls, client: LinLogClient) -> 'Organisation':
        return Organisation.from_json(
            client.get_organisation()
        )

    def __eq__(self, other: 'Organisation') -> bool:
        return self.id == other.id

    def __str__(self) -> str:
        return f"Organistion(id={self.id})"
