# Interruption Handling — Salescode Assignment

## What this module does
A lightweight interruption-handling layer that listens to STT/VAD events and decides:
- `ignore_event` — user backchannel/filler; **do not pause** agent speech
- `delay_event` — short internal soft-listen window (~300ms); **do not pause** TTS
- `interrupt_event` — user intent detected; stop TTS and handover

## Run (local)
```bash
cd voice_agents/interruption_handling_cartesia
# set PYTHONPATH so imports work
$env:PYTHONPATH = ".\src"
pip install pytest
pytest -q
python -m demo
