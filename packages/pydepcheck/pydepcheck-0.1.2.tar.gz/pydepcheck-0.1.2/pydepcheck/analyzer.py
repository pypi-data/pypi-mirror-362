from typing import List, Union, Optional
import ast
import re
from .dependences import DependenceResult, TrueDependence, AntiDependence, OutputDependence


def get_read_set(node: ast.AST) -> List[ast.AST]:
    """
    Returns a list of array loads (reads) from the given AST node.
    """
    reads = set()
    for subnode in ast.walk(node):
        if isinstance(subnode, ast.Subscript) and isinstance(subnode.ctx, ast.Load) and isinstance(subnode.value, ast.Name):
            reads.add((f'{subnode.value.id}', ast.unparse(subnode.slice)))
    return reads

def get_write_set(node: ast.AST) -> List[ast.AST]:
    """
    Returns a list of array stores (writes) from the given AST node.
    """
    writes = set()
    for subnode in ast.walk(node):
        if isinstance(subnode, ast.Subscript) and isinstance(subnode.ctx, ast.Store) and isinstance(subnode.value, ast.Name):
            writes.add((f'{subnode.value.id}', ast.unparse(subnode.slice)))
    return writes


def is_integer(s: str):
    try:
        int(s)
        return True
    except ValueError:
        return False
    
def is_unit_stride_of(s: str, i: str):
    '''
    Check if `s` is a linear function of `i` with coefficient 1.
    '''
    s = s.replace(' ', '')
    if i == s or re.fullmatch(i+r'[+-]\d+', s) or re.fullmatch(r'(\d+)[+]'+i, s):
        return True
    return False

def get_const_offset(s: str, i: str):
    s = s.replace(' ', '')
    if i == s:
        return 0
    
    m = re.fullmatch(i+r'([+-]\d+)', s)
    if m:
        return int(m.groups()[0])
    
    m = re.fullmatch(r'(\d+)[+]'+i, s)
    if m:
        return int(m.groups()[0])
    
    return None

def is_subscript_analyzable(sub: str, i: str):
    return is_integer(sub) or is_unit_stride_of(sub, i)

def get_loop_bounds(tree: ast.AST) -> tuple:
    assert isinstance(tree, ast.For)
    assert len(tree.iter.args) == 2
    lower_bound = ast.unparse(tree.iter.args[0])
    upper_bound = ast.unparse(tree.iter.args[1])
    return lower_bound, upper_bound

def has_dependence(source, sink, L, U, loop_var):
    try: 
        LU_range = int(U) - int(L)
    except:
        # If L and U are not both integers, we just return True
        return True
    
    if is_unit_stride_of(source, loop_var) and is_unit_stride_of(sink, loop_var):
        source_offset = get_const_offset(source, loop_var)
        sink_offset = get_const_offset(sink, loop_var)
        distance = source_offset - sink_offset
        if distance == 0:
            # This would be a loop independent dependence
            return False
        elif distance > 0:
            # Check if the distance is within the loop bounds
            return distance < LU_range
        else:
            # Negative distance indicates infeasible dependence
            return False
    elif is_integer(source) and is_integer(sink):
        return int(source) == int(sink)
    elif is_integer(source) and is_unit_stride_of(sink, loop_var):
        sink_offset = get_const_offset(sink, loop_var)
        sink_index = int(source) - sink_offset
        # `int(L) <= sink_index < int(U)` ensures that sink_index is within loop bounds
        # `sink_index > int(L)` ensures that there exists at least one source index less than the sink index
        return int(L) <= sink_index < int(U) and sink_index > int(L) 
    elif is_unit_stride_of(source, loop_var) and is_integer(sink):
        source_offset = get_const_offset(source, loop_var)
        source_index = int(sink) - source_offset
        # `int(L) <= source_index < int(U)` ensures that source_index is within loop bounds
        # `source_index < int(U) - 1` ensures that there exists at least one sink index greater than the source index
        return int(L) <= source_index < int(U) and source_index < int(U) - 1
    else:
        raise NotImplementedError

def get_true_dependences(source_node, sink_node, L, U, loop_var):
    dependences = []
    for arr1, subscipt1 in get_write_set(source_node):
        for arr2, subscipt2 in get_read_set(sink_node):
            source = f'{arr1}[{subscipt1}]'
            sink = f'{arr2}[{subscipt2}]'
            if arr1 == arr2:
                unanalyzable_subscripts = []              
                if not is_subscript_analyzable(subscipt1, loop_var):
                    unanalyzable_subscripts.append(subscipt1)
                if not is_subscript_analyzable(subscipt2, loop_var):
                    unanalyzable_subscripts.append(subscipt2)
                
                # If some subscripts are unanalyzable, we just return a TrueDependence
                if unanalyzable_subscripts:
                    dependences.append(
                        TrueDependence(arr1, source, sink, source_node, sink_node, unanalyzable_subscripts)
                    )
                else: 
                    # If all subscripts are analyzable, we will check for dependences
                    if has_dependence(subscipt1, subscipt2, L, U, loop_var):
                        dependences.append(
                            TrueDependence(arr1, source, sink, source_node, sink_node)
                        )
    return dependences

def get_anti_dependences(source_node, sink_node, L, U, loop_var):
    dependences = []
    for arr1, subscipt1 in get_read_set(source_node):
        for arr2, subscipt2 in get_write_set(sink_node):
            source = f'{arr1}[{subscipt1}]'
            sink = f'{arr2}[{subscipt2}]'
            if arr1 == arr2:
                unanalyzable_subscripts = []              
                if not is_subscript_analyzable(subscipt1, loop_var):
                    unanalyzable_subscripts.append(subscipt1)
                if not is_subscript_analyzable(subscipt2, loop_var):
                    unanalyzable_subscripts.append(subscipt2)
                
                # If some subscripts are unanalyzable, we just return a TrueDependence
                if unanalyzable_subscripts:
                    dependences.append(
                        AntiDependence(arr1, source, sink, source_node, sink_node, unanalyzable_subscripts)
                    )
                else: 
                    # If all subscripts are analyzable, we will check for dependences
                    if has_dependence(subscipt1, subscipt2, L, U, loop_var):
                        dependences.append(
                            AntiDependence(arr1, source, sink, source_node, sink_node)
                        )
    return dependences

def get_output_dependences(source_node, sink_node, L, U, loop_var):
    dependences = []
    for arr1, subscipt1 in get_write_set(source_node):
        for arr2, subscipt2 in get_write_set(sink_node):
            source = f'{arr1}[{subscipt1}]'
            sink = f'{arr2}[{subscipt2}]'
            if arr1 == arr2:
                unanalyzable_subscripts = []              
                if not is_subscript_analyzable(subscipt1, loop_var):
                    unanalyzable_subscripts.append(subscipt1)
                if not is_subscript_analyzable(subscipt2, loop_var):
                    unanalyzable_subscripts.append(subscipt2)
                
                # If some subscripts are unanalyzable, we just return a TrueDependence
                if unanalyzable_subscripts:
                    dependences.append(
                        OutputDependence(arr1, source, sink, source_node, sink_node, unanalyzable_subscripts)
                    )
                else: 
                    # If all subscripts are analyzable, we will check for dependences
                    if has_dependence(subscipt1, subscipt2, L, U, loop_var):
                        dependences.append(
                            OutputDependence(arr1, source, sink, source_node, sink_node)
                        )
    return dependences


def analyze_loop_dependences(source_code: str) -> DependenceResult:
    """
    Analyzes Python loop nest dependences from source code.
    For now, this is a stub returning a fixed response.
    """
    if not source_code.strip():
        return DependenceResult(analyzable=True, fail_reason='Empty code', dependences=[])

    try:
        tree = ast.parse(source_code)
    except SyntaxError as e:
        return DependenceResult(analyzable=False, fail_reason='AST parsing failed', dependences=[])

    tree = tree.body[0]
    from .passes import rewrite_range, expand_aug_assign
    tree = rewrite_range.transform(tree)
    tree = expand_aug_assign.transform(tree)

    dependences = []
    # Get all assignment statements in the loop
    assignments = [node for node in ast.walk(tree) if isinstance(node, ast.Assign)]
    L, U = get_loop_bounds(tree)
    loop_var = tree.target.id
    for assign1 in assignments:
        for assign2 in assignments:
            dependences += get_true_dependences(assign1, assign2, L, U, loop_var)
            dependences += get_anti_dependences(assign1, assign2, L, U, loop_var)
            dependences += get_output_dependences(assign1, assign2, L, U, loop_var)         

    return DependenceResult(analyzable=True, dependences=dependences)


if __name__ == "__main__":
    example_code = """
for i in range(10):
    a[i] = a[i-1] + 1
"""
    result = analyze_loop_dependences(example_code)
    print(result)