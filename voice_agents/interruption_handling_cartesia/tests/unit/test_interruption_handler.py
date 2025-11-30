import time
from src.interruption_handler import InterruptionHandler

def test_ignore_pure_filler():
    h = InterruptionHandler(config={"delay_window_ms":50})
    h.set_agent_state('SPEAKING')
    events = []
    h.on('ignore_event', lambda p: events.append(p))
    h.on_transcription({"text":"hmm","is_final":True,"confidence":0.9,"ts":int(time.time()*1000)})
    assert any(e["decision"]=="ignore_event" for e in events)

def test_interrupt_explicit_keyword():
    h = InterruptionHandler(config={"delay_window_ms":50})
    h.set_agent_state('SPEAKING')
    events=[]
    h.on('interrupt_event', lambda p: events.append(p))
    h.on_transcription({"text":"stop","is_final":True,"confidence":0.99,"ts":int(time.time()*1000)})
    assert any(e["decision"]=="interrupt_event" for e in events)

def test_delay_then_final_interrupt():
    h = InterruptionHandler(config={"delay_window_ms":80})
    h.set_agent_state('SPEAKING')
    events=[]
    h.on('delay_event', lambda p: events.append(p))
    h.on('interrupt_event', lambda p: events.append(p))
    h.on_transcription({"text":"uh","is_final":False,"confidence":0.3,"ts":int(time.time()*1000)})
    assert any(e["decision"]=="delay_event" for e in events)
    h.on_transcription({"text":"stop","is_final":True,"confidence":0.95,"ts":int(time.time()*1000)})
    assert any(e["decision"]=="interrupt_event" for e in events)
