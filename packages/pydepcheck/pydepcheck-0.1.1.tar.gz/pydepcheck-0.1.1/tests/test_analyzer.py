from pydepcheck import analyze_loop_dependences
from pydepcheck.dependences import *

def test_true_dependence():
    source_code = """
for i in range(10):
    a[i+1] = a[i] + 1
"""
    result = analyze_loop_dependences(source_code)
    assert result.analyzable is True
    assert result.fail_reason is None
    assert len(result.dependences) == 1
    assert isinstance(result.dependences[0], TrueDependence)

def test_anti_dependence():
    source_code = """
for i in range(10):
    a[i] = a[i+1] + 1
"""
    result = analyze_loop_dependences(source_code)
    assert result.analyzable is True
    assert result.fail_reason is None
    assert len(result.dependences) == 1
    assert isinstance(result.dependences[0], AntiDependence)

def test_invalid_code():
    source_code = """
for i in range(10)
    a[i] = a[i-1] + 1
"""  # Missing colon
    result = analyze_loop_dependences(source_code)
    assert result.analyzable is False
    assert result.fail_reason == 'AST parsing failed'
    assert result.dependences == []

def test_empty_code():
    source_code = ""
    result = analyze_loop_dependences(source_code)
    assert result.analyzable is True
    assert result.fail_reason == 'Empty code'
    assert result.dependences == []