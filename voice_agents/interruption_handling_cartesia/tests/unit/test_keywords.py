from src.utils_keywords import is_all_filler, contains_interrupt_keyword

def test_filler_detection():
    assert is_all_filler(['hmm'])
    assert is_all_filler(['yeah','ok'])
    assert not is_all_filler(['yeah','price'])

def test_interrupt_detection():
    assert contains_interrupt_keyword(['yeah','wait','a']) == 'wait'
    assert contains_interrupt_keyword(['what','is','this']) == 'what'
    assert contains_interrupt_keyword(['hmm']) is None
