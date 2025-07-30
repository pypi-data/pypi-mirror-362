'''
This pass rewrites range() to a regular form. For example:
* range(10) -> range(0, 10)
* range(N) -> range(0, N)
* range(10, 20) -> range(10, 20)
* range(10, 20, 2) -> unsupported for now
'''
import ast

class RewriteRange(ast.NodeTransformer):
    def visit_For(self, node):
        self.generic_visit(node)
        if isinstance(node.iter, ast.Call) and node.iter.func.id == 'range':
            if len(node.iter.args) == 1:
                node.iter = ast.Call(func=node.iter.func, args=[ast.Constant(value=0), node.iter.args[0]], keywords=[])
            elif len(node.iter.args) == 2:
                pass
            elif len(node.iter.args) == 3:
                raise NotImplementedError
        
        return node
    
def transform(node):
    return RewriteRange().visit(node)