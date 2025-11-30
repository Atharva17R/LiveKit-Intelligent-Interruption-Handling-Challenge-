from typing import TypedDict

class SttEvent(TypedDict):
    text: str
    is_final: bool
    confidence: float
    ts: int

class VadEvent(TypedDict):
    type: str   # 'START' | 'STOP'
    ts: int

class DecisionPayload(TypedDict):
    decision: str
    reason: str
    text: str
    ts: int
