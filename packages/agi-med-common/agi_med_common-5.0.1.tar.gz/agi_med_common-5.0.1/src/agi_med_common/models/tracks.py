from pydantic import Field

from ._base import _Base


class TrackInfo(_Base):
    track_id: str = Field(alias="TrackId")
    name: str = Field(alias="Name")
    domain_id: str = Field(alias="DomainId")


class DomainInfo(_Base):
    domain_id: str = Field(alias="DomainId")
    name: str = Field(alias="Name")
