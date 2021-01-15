from __future__ import annotations
from dataclasses import dataclass

from pydantic import BaseModel, BaseSettings, Field
from typing import Optional, Dict

class ProbeSetting(BaseSettings):
    port: int
    authAppCredential: str
    testTicker: str
    expectedTickers: int
    max_run_seconds: int

    @classmethod
    def from_request(cls, **detail) -> ProbeSetting:
        return cls(**detail)

class IncomingRequest(BaseModel):
    region: str
    provider: str
    probe: ProbeSetting
    discover_tags: dict

    @classmethod
    def from_request(cls, data: dict) -> IncomingRequest:
        return cls(
            region=data["region"],
            provider=data["provider"],
            probe=ProbeSetting(**data["probe"]),
            discover_tags=data["discover_tags"]
        )

    def write_output_template(self) -> dict:
        return {
            "region": self.region,
            "provider": self.provider,
            "detail": self.probe.dict()
        }

