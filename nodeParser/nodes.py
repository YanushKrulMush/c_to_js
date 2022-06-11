class Node(object):
    pass

class NodeVisitor(object):
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        for c in node:
            self.visit(c)

class Assignment(Node):
    def __init__(self, op, lvalue, rvalue):
        self.op = op
        self.lvalue = lvalue
        self.rvalue = rvalue

class Function(Node):
    def __init__(self, decl, param_decls, body):
        self.decl = decl
        self.param_decls = param_decls
        self.body = body

class Declarator(Node):
    def __init__(self, name, params):
        self.name = name
        self.params = params

class Compound(Node):
    def __init__(self, body, returnStatement):
        self.body = body
        self.returnStatement = returnStatement

class Initializer(Node):
    def __init__(self, type, name, value):
        self.type = type
        self.name = name
        self.value = value