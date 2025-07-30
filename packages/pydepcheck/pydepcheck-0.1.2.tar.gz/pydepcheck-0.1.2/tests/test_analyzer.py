from pydepcheck import analyze_loop_dependences
from pydepcheck.dependences import *

def test_true_dependence():
    """
    for i in range(10):
        a[i+1] = a[i] + 1
    Loop-carried true dependence: write to a[i+1], read a[i].
    """
    source_code = """
for i in range(10):
    a[i+1] = a[i] + 1
"""
    result = analyze_loop_dependences(source_code)
    assert result.analyzable is True
    assert result.fail_reason is None
    assert len(result.dependences) == 1
    assert isinstance(result.dependences[0], TrueDependence)

def test_no_true_dependence():
    """
    for i in range(10):
        a[i+10] = a[i] + 1
    No loop-carried dependences because read and write regions do not overlap.
    """
    source_code = """
for i in range(10):
    a[i+10] = a[i] + 1
"""
    result = analyze_loop_dependences(source_code)
    assert result.analyzable is True
    assert result.fail_reason is None
    assert len(result.dependences) == 0

def test_anti_dependence():
    """
    for i in range(10):
        a[i] = a[i+1] + 1
    Loop-carried anti dependence: write a[i], read a[i+1].
    """
    source_code = """
for i in range(10):
    a[i] = a[i+1] + 1
"""
    result = analyze_loop_dependences(source_code)
    assert result.analyzable is True
    assert result.fail_reason is None
    assert len(result.dependences) == 1
    assert isinstance(result.dependences[0], AntiDependence)

def test_no_anti_dependence():
    """
    for i in range(10):
        a[i] = a[i+10] + 1
    No loop-carried dependence because accessed indices do not overlap across iterations.
    """
    source_code = """
for i in range(10):
    a[i] = a[i+10] + 1
"""
    result = analyze_loop_dependences(source_code)
    assert result.analyzable is True
    assert result.fail_reason is None
    assert len(result.dependences) == 0

def test_output_dependence():
    """
    for i in range(10):
        y[i % 4] += x[i]
    Multiple loop-carried output dependences occur due to repeated writes to y indices.
    """
    source_code = """
for i in range(10):
    y[i % 4] += x[i]
"""
    result = analyze_loop_dependences(source_code)
    assert result.analyzable is True
    assert result.fail_reason is None
    assert len(result.dependences) >= 1
    assert any(isinstance(dep, OutputDependence) for dep in result.dependences)

def test_invalid_code():
    """
    Invalid syntax: missing colon after for loop.
    """
    source_code = """
for i in range(10)
    a[i] = a[i-1] + 1
"""
    result = analyze_loop_dependences(source_code)
    assert result.analyzable is False
    assert result.fail_reason == 'AST parsing failed'
    assert result.dependences == []

def test_empty_code():
    """
    Empty code is considered analyzable but no dependences.
    """
    source_code = ""
    result = analyze_loop_dependences(source_code)
    assert result.analyzable is True
    assert result.fail_reason == 'Empty code'
    assert result.dependences == []

def test_constant_subscript_dependences():
    """
    for i in range(10):
        a[3] = a[3] + 1
    Loop-carried true, anti, and output dependences due to repeated read/write to a[3].
    """
    source_code = """
for i in range(10):
    a[3] = a[3] + 1
"""
    result = analyze_loop_dependences(source_code)
    assert result.analyzable is True
    assert result.fail_reason is None
    kinds = {type(dep) for dep in result.dependences}
    assert TrueDependence in kinds
    assert AntiDependence in kinds
    assert OutputDependence in kinds

def test_unit_stride_offset_true_dependence():
    """
    for i in range(10):
        b[i + 2] = b[i + 1] + 1
    Loop-carried true dependence due to shifted linear subscripts.
    """
    source_code = """
for i in range(10):
    b[i + 2] = b[i + 1] + 1
"""
    result = analyze_loop_dependences(source_code)
    assert result.analyzable is True
    assert result.fail_reason is None
    assert len(result.dependences) == 1
    assert isinstance(result.dependences[0], TrueDependence)

def test_unit_stride_offset_no_dependence():
    """
    for i in range(10):
        b[i + 100] = b[i + 50] + 1
    No loop-carried dependence due to non-overlapping accessed indices.
    """
    source_code = """
for i in range(10):
    b[i + 100] = b[i + 50] + 1
"""
    result = analyze_loop_dependences(source_code)
    assert result.analyzable is True
    assert result.fail_reason is None
    assert len(result.dependences) == 0

def test_mixed_constant_and_linear():
    """
    for i in range(10):
        a[i] = a[5] + 1
    Loop-carried true and anti dependences because
    iteration i=5 writes a[5], others read it.
    """
    source_code = """
for i in range(10):
    a[i] = a[5] + 1
"""
    result = analyze_loop_dependences(source_code)
    assert result.analyzable is True
    assert result.fail_reason is None
    assert len(result.dependences) == 2
    assert any(isinstance(dep, TrueDependence) for dep in result.dependences)
    assert any(isinstance(dep, AntiDependence) for dep in result.dependences)

def test_mixed_constant_and_linear_2():
    """
    for i in range(10):
        a[i] = a[0] + 1
    Loop-carried true and anti dependences because
    iteration i=5 writes a[5], others read it.
    """
    source_code = """
for i in range(10):
    a[i] = a[5] + 1
"""
    result = analyze_loop_dependences(source_code)
    assert result.analyzable is True
    assert result.fail_reason is None
    assert len(result.dependences) == 2
    assert any(isinstance(dep, TrueDependence) for dep in result.dependences)
    assert any(isinstance(dep, AntiDependence) for dep in result.dependences)

def test_constant_read_variable_write_true_dependence():
    source_code = """
for i in range(10):
    a[i] = a[0] + 1
"""
    result = analyze_loop_dependences(source_code)
    assert result.analyzable is True
    assert result.fail_reason is None
    assert len(result.dependences) == 1
    assert isinstance(result.dependences[0], TrueDependence)

def test_constant_read_variable_write_anti_dependence():
    """
    for i in range(10):
        a[i] = a[9] + 1
    Loop-carried anti dependence due to last iteration writing a[9]
    after earlier iterations read it.
    """
    source_code = """
for i in range(10):
    a[i] = a[9] + 1
"""
    result = analyze_loop_dependences(source_code)
    assert result.analyzable is True
    assert result.fail_reason is None
    assert len(result.dependences) == 1
    assert isinstance(result.dependences[0], AntiDependence)