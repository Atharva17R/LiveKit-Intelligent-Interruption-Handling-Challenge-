# 📘 Intelligent Interruption Handling – LiveKit Agent Module  
**Author:** Atharva Rekhe
**Challenge:** LiveKit Intelligent Interruption Handling  
**Folder:** `voice_agents/interruption_handling_cartesia/`

This project implements a complete **interruption-detection layer** for real-time conversational agents.  
The module classifies incoming STT events as:

- `ignore_event`  
- `delay_event`  
- `interrupt_event`

The logic is designed to handle fillers, interruption keywords, meaningful speech, confidence thresholds, timing windows, and agent state.

---

#  Project Structure

```
interruption_handling_cartesia/
│
├── src/
│   ├── interruption_handler.py
│   ├── utils_keywords.py
│   ├── utils_text.py
│   ├── config.py
│   ├── event_types.py
│   └── integration/
│       └── livekit_mock.py
│
├── demo/
│   ├── demo.py
│   └── example-logs.txt
│
├── tests/
│   ├── unit/
│   └── integration/
│
└── README.md
```
# Architecture Diagram
---
                ┌──────────────────────────┐
                │ Incoming STT + VAD Event │
                └───────────────┬──────────┘
                                │
                     Normalize & Tokenize
                                │
                    ┌───────────┴───────────┐
                    │  Agent Speaking?       │
                    └───────┬───────────────┘
                            │
              ┌─────────────┼────────────────────┐
              │             │                    │
        Filler Only?   Interrupt Keyword?   Meaningful Speech?
              │             │                    │
      ┌───────▼──────┐ ┌────▼────┐        ┌─────▼─────┐
      │ ignore_event  │ │ interrupt│        │ interrupt │
      │  (final)      │ │  event   │        │  event    │
      └───────────────┘ └──────────┘        └───────────┘
                            │
                            │
                    

# 🧠 Interruption Logic Overview

The handler evaluates STT events through:
Interruption Logic – How It Works
The goal is to determine whether a user's utterance should interrupt the agent.
The handler watches a continuous stream of STT events (final + partial) and uses the following rules:

### ✔ Agent state  
- IDLE → always interrupt  
- SPEAKING → only meaningful or keyword-based speech interrupts

### ✔ Filler detection  
“Hm”, “uh”, “um” → ignore_event

### ✔ Keyword detection  
“wait”, “stop”, “hold on” → interrupt_event

### ✔ Meaningful speech  
Any real word → interrupt_event

### ✔ Delay window  
Low-confidence or short partials enter a timing window before deciding.

### ✔ Rolling buffer  
The last N ms of STT final events used for delay-timeout decisions.

---

# 🚀 Running Tests

### CMD:

| # | Test Name                               | File Location                               | What It Verifies |
|---|-------------------------------------------|----------------------------------------------|------------------|
| 1 | test_integration_filler_no_pause         | tests/integration/test_scenarios.py          | Ignores pure filler while agent is SPEAKING |
| 2 | test_integration_mixed_interrupt         | tests/integration/test_scenarios.py          | Meaningful utterance triggers interrupt_event |
| 3 | test_ignore_pure_filler                  | tests/unit/test_interruption_handler.py      | Pure filler tokens → ignore_event |
| 4 | test_interrupt_explicit_keyword          | tests/unit/test_interruption_handler.py      | Hard-stop keywords (e.g., “stop”) trigger interrupt_event |
| 5 | test_delay_then_final_interrupt          | tests/unit/test_interruption_handler.py      | Delay window + rolling buffer produce correct final interrupt |
| 6 | test_filler_detection                    | tests/unit/test_keywords.py                  | Filler words (“um”, “hmm”, “uh”) correctly identified |
| 7 | test_interrupt_detection                 | tests/unit/test_keywords.py                  | Interrupt keywords (“wait”, “stop”, “hold on”) detected |
| 8 | test_normalize_tokenize                  | tests/unit/test_text_utils.py                | Text normalization + tokenization logic validated |

```
cd voice_agents\interruption_handling_cartesia
set PYTHONPATH=.\src
python -m pytest -q
```

---

# ▶️ Running the Demo

Generate logs:
```
python demo.py > demo/example-logs.txt
```

View logs:
```
cat demo/example-logs.txt
```

---

# 📄 Example Output

```
{"decision": "ignore_event", "reason": "all-filler", "text": "hmm"}
{"decision": "interrupt_event", "reason": "interruptKeyword:wait", "text": "yeah wait a second"}
{"decision": "interrupt_event", "reason": "agent-idle-forward", "text": "yeah"}
{"decision": "interrupt_event", "reason": "interruptKeyword:stop", "text": "stop"}
```

---

# 🎥 Video Submission

Video should show:

1. Running tests  
2. Running demo  
3. Showing logs  
 





