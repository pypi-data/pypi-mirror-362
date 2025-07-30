import ast
import copy

class AugAssignExpander(ast.NodeTransformer):
    def visit_AugAssign(self, node):
        target_copy = copy.deepcopy(node.target)
        target_copy.ctx = ast.Load()
        newnode = ast.Assign(
            targets=[node.target], 
            value=ast.BinOp(
                left=target_copy, 
                op=node.op, 
                right=node.value
            ),
            lineno=node.lineno,
        )
        ast.fix_missing_locations(newnode)
        return newnode
    
def transform(node):
    return AugAssignExpander().visit(node)