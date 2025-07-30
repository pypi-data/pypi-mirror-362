from datetime import datetime
from typing import Any, List

from agi_med_common.models.widget import Widget
from pydantic import Field, ConfigDict

from ._base import _Base


_DT_FORMAT: str = "%Y-%m-%d-%H-%M-%S"
_EXAMPLE_DT_0 = datetime(1970, 1, 1, 0, 0, 0)
_EXAMPLE_DT: str = _EXAMPLE_DT_0.strftime(_DT_FORMAT)


def now_pretty() -> str:
    return datetime.now().strftime(ReplicaItem.DATETIME_FORMAT())


class OuterContextItem(_Base):
    # remove annoying warning for protected `model_` namespace
    model_config = ConfigDict(protected_namespaces=())

    sex: bool = Field(False, alias="Sex", description="True = male, False = female", examples=[True])
    age: int = Field(0, alias="Age", examples=[20])
    user_id: str = Field("", alias="UserId", examples=["123456789"])
    parent_session_id: str | None = Field(None, alias="ParentSessionId", examples=["987654320"])
    session_id: str = Field("", alias="SessionId", examples=["987654321"])
    client_id: str = Field("", alias="ClientId", examples=["543216789"])
    track_id: str = Field(default="Consultation", alias="TrackId")
    entrypoint_key: str = Field("", alias="EntrypointKey", examples=["giga"])
    language_code: str = Field("ru", alias="LanguageCode", examples=["ru"])

    def create_id(self, short: bool = False) -> str:
        uid, sid, cid = self.user_id, self.session_id, self.client_id
        if short:
            return f"{uid}_{sid}_{cid}"
        return f"user_{uid}_session_{sid}_client_{cid}"

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump(by_alias=True)


class ReplicaItem(_Base):
    body: str = Field("", alias="Body", examples=["Привет"])
    resource_id: str | None = Field(None, alias="ResourceId", examples=["<link-id>"])
    widget: Widget | None = Field(None, alias="Widget", examples=[None])
    command: dict | None = Field(None, alias="Command", examples=[None])
    role: bool = Field(False, alias="Role", description="True = ai, False = client", examples=[False])
    date_time: str = Field(
        default_factory=now_pretty, alias="DateTime", examples=[_EXAMPLE_DT], description=f"Format: {_DT_FORMAT}"
    )
    state: str = Field("", alias="State", description="chat manager fsm state", examples=["COLLECTION"])
    action: str = Field("", alias="Action", description="chat manager fsm action", examples=["DIAGNOSIS"])
    # todo fix: support loading from `moderation: int`
    moderation: str = Field("OK", alias="Moderation", description="moderation outcome", examples=["OK"])
    extra: dict | None = Field(None, alias="Extra", examples=[None])

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump(by_alias=True)

    @staticmethod
    def DATETIME_FORMAT() -> str:
        return _DT_FORMAT

    def with_now_datetime(self):
        return self.model_copy(update=dict(date_time=now_pretty()))


class InnerContextItem(_Base):
    replicas: list[ReplicaItem] = Field(alias="Replicas")
    attrs: dict[str, str | int] | None = Field(default={}, alias="Attrs")

    def to_dict(self) -> dict[str, list]:
        return self.model_dump(by_alias=True)


class ChatItem(_Base):
    outer_context: OuterContextItem = Field(alias="OuterContext")
    inner_context: InnerContextItem = Field(alias="InnerContext")

    def create_id(self, short: bool = False) -> str:
        return self.outer_context.create_id(short)

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump(by_alias=True)

    def add_replica(self, replica: ReplicaItem):
        self.inner_context.replicas.append(replica)

    def add_replicas(self, replicas: List[ReplicaItem]):
        for replica in replicas:
            self.inner_context.replicas.append(replica)

    def zip_history(self, field: str) -> list[Any]:
        return [replica.to_dict().get(field, None) for replica in self.inner_context.replicas]
