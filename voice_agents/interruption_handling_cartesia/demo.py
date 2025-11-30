# demo.py
import time
import json
from src.integration.livekit_mock import LivekitMock
from src.interruption_handler import InterruptionHandler
from src.config import DEFAULT_CONFIG

def log(decision_payload):
    # print as single-line JSON so it's easy to capture in video
    print(json.dumps({
        "t": int(time.time()*1000),
        "event": decision_payload.get("decision", "unknown"),
        "reason": decision_payload.get("reason"),
        "text": decision_payload.get("text")
    }))

def main():
    mock = LivekitMock()
    # use default config so behaviour is explicit
    h = InterruptionHandler(config=DEFAULT_CONFIG.copy())
    h.set_agent_state('SPEAKING')

    # register handlers that log decisions
    h.on('ignore_event', lambda p: log({"decision": p.decision, "reason": p.reason, "text": p.text}))
    h.on('delay_event', lambda p: log({"decision": p.decision, "reason": p.reason, "text": p.text}))
    h.on('interrupt_event', lambda p: log({"decision": p.decision, "reason": p.reason, "text": p.text}))

    mock.on_transcription(h.on_transcription)
    mock.on_vad(h.on_vad_event)

    # timeline: filler -> mixed -> idle->yeah -> stop
    now = int(time.time()*1000)
    mock.send_stt({"text":"hmm","is_final":True,"confidence":0.9,"ts":now+100})
    time.sleep(0.8)   # allow handler to decide and emit

    mock.send_stt({"text":"yeah wait a second","is_final":True,"confidence":0.95,"ts":int(time.time()*1000)})
    time.sleep(1.0)

    h.set_agent_state('IDLE')   # now agent idle, same filler should be treated as interrupt
    mock.send_stt({"text":"yeah","is_final":True,"confidence":0.95,"ts":int(time.time()*1000)})
    time.sleep(0.8)

    h.set_agent_state('SPEAKING')
    mock.send_stt({"text":"stop","is_final":True,"confidence":0.99,"ts":int(time.time()*1000)})

if __name__ == "__main__":
    main()
