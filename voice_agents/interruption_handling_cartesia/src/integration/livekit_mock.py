# livekit_mock.py
from typing import Callable, List, Any

class LivekitMock:
    def __init__(self):
        self._on_transcription: List[Callable[[Any], None]] = []
        self._on_vad: List[Callable[[Any], None]] = []

    def on_transcription(self, cb: Callable[[dict], None]):
        self._on_transcription.append(cb)

    def on_vad(self, cb: Callable[[dict], None]):
        self._on_vad.append(cb)

    def send_stt(self, e: dict):
        for cb in self._on_transcription:
            cb(e)

    def send_vad(self, e: dict):
        for cb in self._on_vad:
            cb(e)
