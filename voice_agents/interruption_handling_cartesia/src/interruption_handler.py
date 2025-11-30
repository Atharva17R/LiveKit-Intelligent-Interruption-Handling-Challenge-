# interruption_handler.py
import time
import json
from threading import Timer, Lock
from typing import Callable, List, Optional
from .config import DEFAULT_CONFIG
from .utils_text import normalize_text, tokenize
from .utils_keywords import is_all_filler, contains_interrupt_keyword, contains_meaningful_token
from .event_types import SttEvent, VadEvent, DecisionPayload

class InterruptionHandler:
    def __init__(self, config: dict = None):
        self.config = DEFAULT_CONFIG.copy()
        if config:
            self.config.update(config)
        self.agent_state = 'IDLE'  # 'SPEAKING' | 'IDLE'
        self.buffer: List[SttEvent] = []
        self.delay_timer: Optional[Timer] = None
        self.delay_lock = Lock()
        self._listeners = {"ignore_event": [], "delay_event": [], "interrupt_event": []}
        self.last_vad_stop_ts: Optional[int] = None

    # event registration
    def on(self, event_name: str, cb: Callable[[DecisionPayload], None]):
        if event_name in self._listeners:
            self._listeners[event_name].append(cb)

    def emit(self, event_name: str, payload: DecisionPayload):
        # structured log
        print(json.dumps({"t": int(time.time()*1000), "agentState": self.agent_state, **payload}))
        for cb in self._listeners.get(event_name, []):
            try:
                cb(payload)
            except Exception:
                pass

    def set_agent_state(self, s: str):
        self.agent_state = s

    def on_vad_event(self, e: VadEvent):
        if e.get("type") == "STOP":
            self.last_vad_stop_ts = e.get("ts")

    def on_transcription(self, e: SttEvent):
        text_norm = normalize_text(e.get("text", ""))
        tokens = tokenize(text_norm)
        now_ms = int(time.time()*1000)
        # push to rolling buffer
        self.buffer.append({**e, "text": text_norm})
        self.buffer = [x for x in self.buffer if (now_ms - x["ts"]) <= self.config["rolling_buffer_ms"]]

        if self.agent_state == 'IDLE':
            self.emit_decision('interrupt_event', 'agent-idle-forward', text_norm, e.get("ts"))
            return

        # Agent speaking:
        if e.get("is_final") and is_all_filler(tokens):
            self.clear_delay()
            self.emit_decision('ignore_event', 'all-filler', text_norm, e.get("ts"))
            return

        ik = contains_interrupt_keyword(tokens)
        if ik:
            self.clear_delay()
            self.emit_decision('interrupt_event', f'interruptKeyword:{ik}', text_norm, e.get("ts"))
            return

        if e.get("is_final") and contains_meaningful_token(tokens):
            self.clear_delay()
            self.emit_decision('interrupt_event', 'final-meaningful', text_norm, e.get("ts"))
            return

        low_conf_partial = (not e.get("is_final")) and (e.get("confidence", 0.0) < self.config["partial_confidence_threshold"])
        very_short = len(tokens) <= 1

        if (not e.get("is_final")) and (low_conf_partial or very_short):
            self.enter_delay_window(e)
            return

        if (not e.get("is_final")) and contains_meaningful_token(tokens) and e.get("confidence", 0.0) >= self.config["partial_confidence_threshold"]:
            self.clear_delay()
            self.emit_decision('interrupt_event', 'partial-meaningful-highconf', text_norm, e.get("ts"))
            return

        if e.get("is_final") and len(tokens) == 0:
            self.clear_delay()
            self.emit_decision('ignore_event', 'final-empty', text_norm, e.get("ts"))
            return

        # fallback
        self.enter_delay_window(e)

## delay window
    def enter_delay_window(self, e: SttEvent):
        with self.delay_lock:
            self.emit_decision('delay_event', 'enter-delay-window', e.get("text", normalize_text(e.get("text",""))), e.get("ts"))
            if self.delay_timer:
                self.delay_timer.cancel()
            ms = int(self.config["delay_window_ms"])
            self.delay_timer = Timer(ms/1000.0, self._on_delay_timeout, args=(e,))
            self.delay_timer.start()
            
## timeout logic
    def _on_delay_timeout(self, orig_event: SttEvent):
        with self.delay_lock:
            now_ms = int(time.time()*1000)
            last_final = None
            for x in reversed(self.buffer):
                if x.get("is_final"):
                    last_final = x
                    break
            if last_final:
                tokens = tokenize(last_final.get("text",""))
                if is_all_filler(tokens):
                    self.emit_decision('ignore_event', 'delay-timeout-all-filler', last_final.get("text",""), now_ms)
                elif contains_interrupt_keyword(tokens):
                    ik = contains_interrupt_keyword(tokens)
                    self.emit_decision('interrupt_event', f'delay-timeout-interrupt:{ik}', last_final.get("text",""), now_ms)
                elif contains_meaningful_token(tokens):
                    self.emit_decision('interrupt_event', 'delay-timeout-meaningful-final', last_final.get("text",""), now_ms)
                else:
                    self.emit_decision('ignore_event', 'delay-timeout-default-ignore', last_final.get("text",""), now_ms)
            else:
                self.emit_decision('ignore_event', 'delay-timeout-no-final', orig_event.get("text", ""), now_ms)
            self.delay_timer = None

    def clear_delay(self):
        with self.delay_lock:
            if self.delay_timer:
                self.delay_timer.cancel()
                self.delay_timer = None

    def emit_decision(self, decision: str, reason: str, text: str, ts: int):
        payload = DecisionPayload(decision=decision, reason=reason, text=text, ts=ts)
        self.emit(decision, payload)
