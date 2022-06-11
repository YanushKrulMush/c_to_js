from ply import yacc
import lexer
import nodes

tokens = lexer.tokens

def p_function_definition(p):
    """ function_definition : type_specifier declarator compound_statement
    """
    p[0] = nodes.Function(p[1], p[2], p[3])

def p_compound_statement(p):
    """ compound_statement : LBRACE RBRACE
	| LBRACE statement_list RETURN expression SEMI RBRACE
    """
    p[0] = nodes.Compound(p[2], p[4])

def p_statement_list(p):
    """ statement_list : statement
	| statement_list statement
    """
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[1].append(p[2])
        p[0] = p[1]

def p_statement(p):
    """ statement : initializer
	| assignment_expression
    """
    p[0] = p[1]

def p_initializer(p):
    """ initializer : type_specifier IDENTIFIER EQUALS expression SEMI
    """
    p[0] = nodes.Initializer(p[1], p[2], p[4])

def p_assignment_expression(p):
    """ assignment_expression : expression SEMI
    | IDENTIFIER assignment_operator assignment_expression
    """
    if len(p) == 3:
        p[0] = p[1]
    else:
        p[0] = nodes.Assignment(p[2], p[1], p[3])

def p_expression(p):
    """ expression : IDENTIFIER
    | STRING
    | INTEGER
    | FLOAT
    """    
    p[0] = p[1]

def p_declarator(p):
    """ declarator : IDENTIFIER LPAREN RPAREN
    """
    p[0] = nodes.Declarator(p[1], [])

def p_type_specifier(p):
    """ type_specifier : VOID
	| CHAR
	| SHORT
	| INT
	| LONG
	| FLOAT
	| DOUBLE
    """
    p[0] = p[1]

def p_assignment_operator(p):
    """ assignment_operator : EQUALS
	| TIMESEQUAL
	| DIVEQUAL
	| MODEQUAL
	| PLUSEQUAL
	| MINUSEQUAL
	| LSHIFTEQUAL 
	| RSHIFTEQUAL 
	| ANDEQUAL
	| XOREQUAL
	| OREQUAL
    """
    p[0] = p[1]


parser = yacc.yacc()

def parse(data, debug=0):
    parser.error = 0
    p = parser.parse(data, debug=debug)
    if parser.error:
        return None
    return p

if __name__ == '__main__':
    file = open("C:\\Users\\JA\\Documents\\AGH\\Kompilatory\\js_translator\\test.c", "r")
    parse(file.read())
	