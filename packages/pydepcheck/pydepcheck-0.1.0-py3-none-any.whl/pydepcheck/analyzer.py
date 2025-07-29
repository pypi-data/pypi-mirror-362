from typing import List, Union
import ast

class DependenceResult:
    def __init__(self, dependences: List[str], unanalyzable_reasons: List[str]):
        self.dependences = dependences
        self.unanalyzable_reasons = unanalyzable_reasons

    def is_analyzable(self) -> bool:
        return len(self.unanalyzable_reasons) == 0

    def __str__(self):
        if self.is_analyzable():
            return f"Dependences found: {self.dependences}"
        else:
            return f"Unanalyzable: {self.unanalyzable_reasons}"


def analyze_loop_dependences(source_code: str) -> DependenceResult:
    """
    Analyzes Python loop nest dependences from source code.
    For now, this is a stub returning a fixed response.
    """
    try:
        tree = ast.parse(source_code)
    except SyntaxError as e:
        return DependenceResult([], [f"Syntax error: {e}"])

    # TODO: Implement actual loop dependence analysis here.
    # For now, mock result:
    dependences = ["i -> i+1"]  # Mock example
    unanalyzable_reasons = []

    return DependenceResult(dependences, unanalyzable_reasons)


if __name__ == "__main__":
    example_code = """
for i in range(10):
    a[i] = a[i-1] + 1
"""
    result = analyze_loop_dependences(example_code)
    print(result)