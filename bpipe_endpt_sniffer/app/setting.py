from __future__ import annotations
from attr import dataclass

from pydantic import BaseSettings, BaseSettings, Field
from typing import Optional, Dict

@dataclass
class IncomingRequest():
    region: str
    probe: ProbeSetting
    sniff_tags: Dict

    
    @classmethod
    def from_request(cls, data:Dict)->IncomingRequest:
        return cls(
            region = data["region"],
            probe=ProbeSetting(**data["probe"]),
            sniff_tags=data["sniff_tags"]
        )

    def write_OutputTemplate(self) -> Dict:
        return {
            "region": self.region,
            "detail": self.probe.dict()
        }

class ProbeSetting(BaseSettings):
    port: int
    authAppCredential: str
    testTicker: str
    expectedTickers: int
    max_run_seconds: int
    logBucket: Optional[str] = None

    @classmethod
    def from_request(cls, **detail)->ProbeSetting:
        return cls(**detail)