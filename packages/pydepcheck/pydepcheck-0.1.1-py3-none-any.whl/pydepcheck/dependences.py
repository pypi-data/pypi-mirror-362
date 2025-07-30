import ast
from dataclasses import dataclass
from typing import List, Union, Optional

@dataclass
class DependenceResult:
    analyzable: bool
    fail_reason: Optional[str] = None
    dependences: list = None

@dataclass
class Dependence:
    var: str
    source: str
    sink: str
    source_node: ast.AST
    sink_node: ast.AST
    unanalyzable_subscripts: List[str] = None

@dataclass
class TrueDependence(Dependence):
    pass

@dataclass
class AntiDependence(Dependence):
    pass

@dataclass
class OutputDependence(Dependence):
    pass
