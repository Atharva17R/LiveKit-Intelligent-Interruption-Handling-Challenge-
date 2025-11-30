# config.py
DEFAULT_CONFIG = {
    "ignore_list": ['hmm','mm','uh-huh','uh','yeah','yep','okay','ok','right','mhm','mmh'],
    "interrupt_keywords": ['stop','wait','pause','repeat','again','what','why','how','who','where','when','tell','ask','question','hold'],
    "question_words": ['what','why','how','who','where','when'],
    "min_meaningful_tokens": 1,
    "delay_window_ms": 300,
    "partial_confidence_threshold": 0.50,
    "rolling_buffer_ms": 1500,
    "overlap_threshold_ms": 300
}
