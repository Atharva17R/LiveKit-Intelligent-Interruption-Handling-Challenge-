from src.utils_text import normalize_text, tokenize

def test_normalize_tokenize():
    s = "Yeah, wait a second!"
    assert normalize_text(s) == "yeah wait a second"
    assert tokenize(s) == ["yeah","wait","a","second"]
