import time
from src.interruption_handler import InterruptionHandler
try:
    from src.integration.livekit_mock import LivekitMock
except Exception:
    from src.integration.livekit_mock import LiveKitMock

def test_integration_filler_no_pause():
    mock = LivekitMock()
    h = InterruptionHandler(config={"delay_window_ms": 50})
    h.set_agent_state('SPEAKING')

    mock.on_transcription(h.on_transcription)
    mock.on_vad(h.on_vad_event)

    decisions = []
    h.on('ignore_event', lambda d: decisions.append(d))

    mock.send_stt({"text": "hmm", "is_final": True, "confidence": 0.9, "ts": int(time.time()*1000)})

    deadline = time.time() + 0.5
    while time.time() < deadline and len(decisions) == 0:
        time.sleep(0.01)

    assert any(d["decision"] == "ignore_event" for d in decisions)


def test_integration_mixed_interrupt():
    mock = LivekitMock()
    h = InterruptionHandler(config={"delay_window_ms": 50})
    h.set_agent_state('SPEAKING')

    mock.on_transcription(h.on_transcription)
    mock.on_vad(h.on_vad_event)

    decisions = []
    h.on('interrupt_event', lambda d: decisions.append(d))

    mock.send_stt({"text": "yeah wait a second", "is_final": True, "confidence": 0.95, "ts": int(time.time()*1000)})

    deadline = time.time() + 0.5
    while time.time() < deadline and len(decisions) == 0:
        time.sleep(0.01)

    assert any(d["decision"] == "interrupt_event" for d in decisions)
