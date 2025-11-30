# demo.py
import time
from src.integration.livekit_mock import LivekitMock
# new — import from package so PYTHONPATH=./src works
from src.interruption_handler import InterruptionHandler


def main():
    mock = LivekitMock()
    h = InterruptionHandler()
    h.set_agent_state('SPEAKING')

    h.on('ignore_event', lambda p: None)
    h.on('delay_event', lambda p: None)
    h.on('interrupt_event', lambda p: print("** HANDOVER TO USER **", p))

    mock.on_transcription(h.on_transcription)
    mock.on_vad(h.on_vad_event)

    now = int(time.time()*1000)
    # sequence: filler -> mixed -> idle->yeah -> stop
    mock.send_stt({"text":"hmm","is_final":True,"confidence":0.9,"ts":now+100})
    time.sleep(0.7)
    mock.send_stt({"text":"yeah wait a second","is_final":True,"confidence":0.95,"ts":int(time.time()*1000)})
    time.sleep(1.0)
    h.set_agent_state('IDLE')
    mock.send_stt({"text":"yeah","is_final":True,"confidence":0.95,"ts":int(time.time()*1000)})
    time.sleep(0.8)
    h.set_agent_state('SPEAKING')
    mock.send_stt({"text":"stop","is_final":True,"confidence":0.99,"ts":int(time.time()*1000)})

if __name__ == "__main__":
    main()
