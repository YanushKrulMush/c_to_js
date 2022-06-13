import os
from ply import yacc
import lexer

tokens = lexer.tokens

def p_translation_unit(p):
    """ translation_unit : external_declaration
	| translation_unit external_declaration
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + os.linesep + p[2]

def p_external_declaration(p):
    """ external_declaration : function_definition
	| declaration
    """
    p[0] = p[1]

def p_function_definition(p):
    """ function_definition : declaration_specifiers declarator declaration_list compound_statement
	| declaration_specifiers declarator compound_statement
	| declarator declaration_list compound_statement
	| declarator compound_statement
    """
    p[0] = "function " + p[2] + p[3]
    if "main" in p[2]:
        p[0] += f"{os.linesep}main()"


def p_primary_expression(p):
    """ primary_expression  : IDENTIFIER
    | STRING
    | INTEGER
    | CHARACTER
    | FLOAT
    | LPAREN expression RPAREN
    """
    # NIECH SIE STANIE LOGOWANIE
    if p[1] == "printf":
        p[1] = "console.log"
    p[0] = p[1] 

def p_postfix_expression(p):
    """ postfix_expression : primary_expression
	| postfix_expression LBRACKET expression RBRACKET
	| postfix_expression LPAREN RPAREN
	| postfix_expression LPAREN argument_expression_list RPAREN
	| postfix_expression PERIOD IDENTIFIER
	| postfix_expression ARROW IDENTIFIER
	| postfix_expression INCREMENT
	| postfix_expression DECREMENT
    """
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = p[1] + p[2]
    else:
        p[0] = p[1] + p[2] + ', '.join(p[3]) + p[4]

def p_argument_expression_list(p):
    """ argument_expression_list : assignment_expression
	| argument_expression_list COMMA assignment_expression
    """
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[1].append(p[3])
        p[0] = p[1]

def p_unary_expression(p):
    """ unary_expression : postfix_expression
	| INCREMENT unary_expression
	| DECREMENT unary_expression
	| unary_operator cast_expression
	| SIZEOF unary_expression
	| SIZEOF LPAREN type_name RPAREN
    """
    p[0] = p[1]

def p_unary_operator(p):
    """ unary_operator : MODULO
	| TIMES
	| PLUS
	| MINUS
	| NOT
	| LNOT
    """
    p[0] = p[1]

def p_cast_expression(p):
    """ cast_expression : unary_expression
	| LPAREN type_name RPAREN cast_expression
    """
    p[0] = p[1]


def p_multiplicative_expression(p):
    """ multiplicative_expression : cast_expression
	| multiplicative_expression TIMES cast_expression
	| multiplicative_expression DIVIDE cast_expression
	| multiplicative_expression MODULO cast_expression
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + " " + p[2] + " " + p[3]

def p_additive_expression(p):
    """ additive_expression : multiplicative_expression
	| additive_expression PLUS multiplicative_expression
	| additive_expression MINUS multiplicative_expression
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + " " + p[2] + " " + p[3]

def p_shift_expression(p):
    """ shift_expression : additive_expression
	| shift_expression LSHIFT additive_expression
	| shift_expression RSHIFT additive_expression
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + " " + p[2] + " " + p[3]

def p_relational_expression(p):
    """ relational_expression : shift_expression
	| relational_expression LT shift_expression
	| relational_expression GT shift_expression
	| relational_expression LE shift_expression
	| relational_expression GE shift_expression
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + " " + p[2] + " " + p[3]

def p_equality_expression(p):
    """ equality_expression : relational_expression
	| equality_expression EQ relational_expression
	| equality_expression NE relational_expression
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + " " + p[2] + " " + p[3]

def p_and_expression(p):
    """ and_expression : equality_expression
	| and_expression AND equality_expression
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + " " + p[2] + " " + p[3]

def p_exclusive_or_expression(p):
    """ exclusive_or_expression : and_expression
	| exclusive_or_expression XOR and_expression
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + " " + p[2] + " " + p[3]

def p_inclusive_or_expression(p):
    """ inclusive_or_expression : exclusive_or_expression
	| inclusive_or_expression OR exclusive_or_expression
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + " " + p[2] + " " + p[3]

def p_logical_and_expression(p):
    """ logical_and_expression : inclusive_or_expression
	| logical_and_expression LAND inclusive_or_expression
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + " " + p[2] + " " + p[3]

def p_logical_or_expression(p):
    """ logical_or_expression : logical_and_expression
	| logical_or_expression LOR logical_and_expression
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + " " + p[2] + " " + p[3]

def p_conditional_expression(p):
    """ conditional_expression : logical_or_expression
	| logical_or_expression TERNARY expression COLON conditional_expression
    """
    p[0] = p[1]

def p_assignment_expression(p):
    """ assignment_expression : conditional_expression
	| unary_expression assignment_operator assignment_expression
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + " " + p[2] + " " + p[3]

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

def p_expression(p):
    """ expression : assignment_expression
	| expression COMMA assignment_expression
    """
    p[0] = p[1]

def p_constant_expression(p):
    """ constant_expression : conditional_expression
    """
    p[0] = p[1]

def p_declaration(p):
    """ declaration : declaration_specifiers SEMI
	| declaration_specifiers init_declarator_list SEMI
    """
    p[0] = "let " + ", ".join(p[2])

def p_declaration_specifiers(p):
    """ declaration_specifiers : type_specifier
	| type_specifier declaration_specifiers
	| type_qualifier
	| type_qualifier declaration_specifiers
    """
    p[0] = ""

def p_init_declarator_list(p):
    """ init_declarator_list : init_declarator
	| init_declarator_list COMMA init_declarator
    """
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[1].append(p[3])
        p[0] = p[1]

def p_init_declarator(p):
    """ init_declarator : declarator
	| declarator EQUALS initializer
    """
    p[0] = p[1] + "=" + p[3]

def p_type_specifier(p):
    """ type_specifier : VOID
	| CHAR
	| SHORT
	| INT
	| LONG
	| FLOAT
	| DOUBLE
	| SIGNED
	| UNSIGNED
	| struct_or_union_specifier
	| enum_specifier
    """
    if p[1] == "int":
        p[0] = "number"
    else:
        p[0] = p[1]
    
def p_struct_or_union_specifier(p):
    """ struct_or_union_specifier : struct_or_union IDENTIFIER LBRACE struct_declaration_list RBRACE
	| struct_or_union LBRACE struct_declaration_list RBRACE
	| struct_or_union IDENTIFIER
    """
    p[0] = p[1]

def p_struct_or_union(p):
    """ struct_or_union : STRUCT
	| UNION
    """
    p[0] = p[1]

def p_struct_declaration(p):
    """ struct_declaration : specifier_qualifier_list struct_declarator_list SEMI
    """
    p[0] = p[1]

def p_struct_declaration_list(p):
    """ struct_declaration_list : struct_declaration
	| struct_declaration_list struct_declaration
    """
    p[0] = p[1]

def p_struct_declarator_list(p):
    """ struct_declarator_list : struct_declarator
	| struct_declarator_list COMMA struct_declarator
    """
    p[0] = p[1]

def p_struct_declarator(p):
    """ struct_declarator : declarator
	| COLON constant_expression
	| declarator COLON constant_expression
    """
    p[0] = p[1]

def p_specifier_qualifier_list(p):
    """ specifier_qualifier_list : type_specifier specifier_qualifier_list
	| type_specifier
	| type_qualifier specifier_qualifier_list
	| type_qualifier
    """
    p[0] = p[1]

def p_enum_specifier(p):
    """ enum_specifier : ENUM LBRACE enumerator_list RBRACE
	| ENUM IDENTIFIER LBRACE enumerator_list RBRACE
	| ENUM IDENTIFIER
    """
    p[0] = p[1]

def p_enumerator_list(p):
    """ enumerator_list : enumerator
	| enumerator_list COMMA enumerator
    """
    p[0] = p[1]

def p_enumerator(p):
    """ enumerator : IDENTIFIER
	| IDENTIFIER EQUALS constant_expression
    """
    p[0] = p[1]

def p_type_qualifier(p):
    """ type_qualifier : CONST
	| VOLATILE
    """
    p[0] = p[1]

def p_declarator(p):
    """ declarator : pointer direct_declarator
	| direct_declarator
    """
    p[0] = p[1]

def p_direct_declarator(p):
    """ direct_declarator : IDENTIFIER
	| LPAREN declarator RPAREN
	| direct_declarator LBRACKET constant_expression RBRACKET
	| direct_declarator LBRACKET RBRACKET
	| direct_declarator LPAREN parameter_type_list RPAREN
	| direct_declarator LPAREN identifier_list RPAREN
	| direct_declarator LPAREN RPAREN
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        if len(p) == 4:
            p[0] =  p[1] + p[2] + p[3]
        else:
            p[0] = p[1] + p[2] + ','.join(p[3]) + p[4]

def p_pointer(p):
    """ pointer : TIMES
	| TIMES type_qualifier_list
	| TIMES pointer
	| TIMES type_qualifier_list pointer
    """
    p[0] = p[1]

def p_type_qualifier_list(p):
    """ type_qualifier_list : type_qualifier
	| type_qualifier_list type_qualifier
    """
    p[0] = p[1]

def p_parameter_type_list(p):
    """ parameter_type_list : parameter_list
	| parameter_list COMMA ELLIPSIS
    """
    p[0] = p[1]

def p_parameter_list(p):
    """ parameter_list : parameter_declaration
	| parameter_list COMMA parameter_declaration
    """
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[1].append(p[3])
        p[0] = p[1]

def p_parameter_declaration(p):
    """ parameter_declaration : declaration_specifiers declarator
	| declaration_specifiers abstract_declarator
	| declaration_specifiers
    """
    p[0] = p[1] + " " + p[2]

def p_identifier_list(p):
    """ identifier_list : IDENTIFIER
	| identifier_list COMMA IDENTIFIER
    """
    p[0] = p[1]

def p_type_name(p):
    """ type_name : specifier_qualifier_list
	| specifier_qualifier_list abstract_declarator
    """
    p[0] = p[1]

def p_abstract_declarator(p):
    """ abstract_declarator : pointer
	| direct_abstract_declarator
	| pointer direct_abstract_declarator
    """
    p[0] = p[1]

def p_direct_abstract_declarator(p):
    """ direct_abstract_declarator : LPAREN abstract_declarator RPAREN
	| LBRACKET RBRACKET
	| LBRACKET constant_expression RBRACKET
	| direct_abstract_declarator LBRACKET RBRACKET
	| direct_abstract_declarator LBRACKET constant_expression RBRACKET
	| LPAREN RPAREN
	| LPAREN parameter_type_list RPAREN
	| direct_abstract_declarator LPAREN RPAREN
	| direct_abstract_declarator LPAREN parameter_type_list RPAREN
    """
    p[0] = p[1]

def p_initializer(p):
    """ initializer : assignment_expression
	| LBRACE initializer_list RBRACE
	| LBRACE initializer_list COMMA RBRACE
    """
    p[0] = p[1]

def p_initializer_list(p):
    """ initializer_list : initializer
	| initializer_list COMMA initializer
    """
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[1].append(p[2])
        p[0] = p[1]

def p_statement(p):
    """ statement : labeled_statement
	| compound_statement
	| expression_statement
	| selection_statement
	| iteration_statement
	| jump_statement
    """
    p[0] = p[1]

def p_labeled_statement(p):
    """ labeled_statement : IDENTIFIER COLON statement
	| CASE constant_expression COLON statement
	| DEFAULT COLON statement
    """
    p[0] = p[1]

def p_compound_statement(p):
    """ compound_statement : LBRACE RBRACE
	| LBRACE statement_list RBRACE
	| LBRACE declaration_list RBRACE
	| LBRACE declaration_list statement_list RBRACE
    """
    if len(p) == 3:
        p[0] = p[1] + p[2]
    elif len(p) == 4:
        p[0] = f"{p[1]}{os.linesep}{os.linesep.join(p[2])}{os.linesep}{p[3]}"
    else:
        p[0] = f"{p[1]}{os.linesep}{os.linesep.join(p[2])}{os.linesep}{os.linesep.join(p[3])}{os.linesep}{p[4]}"

def p_declaration_list(p):
    """ declaration_list : declaration
	| declaration_list declaration
    """
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[1].append(p[2])
        p[0] = p[1]

def p_statement_list(p):
    """ statement_list : statement
	| statement_list statement
    """
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[1].append(p[2])
        p[0] = p[1]

def p_expression_statement(p):
    """ expression_statement : SEMI
	| expression SEMI
    """
    p[0] = p[1]

def p_selection_statement(p):
    """ selection_statement : IF LPAREN expression RPAREN statement
	| IF LPAREN expression RPAREN statement ELSE statement
	| SWITCH LPAREN expression RPAREN statement
    """
    if p[1] == "if":
        if len(p) == 6:
            p[0] = f"{p[1]} {p[2]}{p[3]}{p[4]}{p[5]}"
        else:
            p[0] = f"{p[1]}{os.linesep}{os.linesep.join(p[2])}{os.linesep}{os.linesep.join(p[3])}{os.linesep}{p[4]}"

def p_iteration_statement(p):
    """ iteration_statement : WHILE LPAREN expression RPAREN statement
	| DO statement WHILE LPAREN expression RPAREN SEMI
	| FOR LPAREN expression_statement expression_statement RPAREN statement
	| FOR LPAREN expression_statement expression_statement expression RPAREN statement
    """
    if p[1].lower() == "for":
        if len(p) == 8:
            x = f"{p[1]} {p[2]}{p[3]}; {p[4]}; {p[5]}{p[6]}{p[7]}" 
            p[0] = x
        else:
            x = f"{p[1]} {p[2]}{p[3]}; {p[4]}; {p[5]}{p[6]}" 
            p[0] = x
    elif p[1].lower() == "while":
        p[0] = f"{p[1]}{p[2]}{p[3]}{p[4]}{p[5]}"
    else:
         p[0] = f"{p[1]}{p[2]}{p[3]}{p[4]}{p[5]}{p[6]}"

def p_jump_statement(p):
    """ jump_statement : GOTO IDENTIFIER SEMI
	| CONTINUE SEMI
	| BREAK SEMI
	| RETURN SEMI
	| RETURN expression SEMI
    """
    if len(p) == 3:
        p[0] = p[1]
    else:
        p[0] = p[1] + " " + p[2]

def p_error(p):
    # get formatted representation of stack
    stack_state_str = ' '.join([symbol.type for symbol in parser.symstack][1:])

    print('Syntax error in input! Parser State:{} {} . {}'
          .format(parser.state,
                  stack_state_str,
                  p))

parser = yacc.yacc()

def parse(data, debug=0):
    parser.error = 0
    p = parser.parse(data, debug=debug)
    if parser.error:
        return None
    return p

if __name__ == '__main__':
    file = open("test.c", "r")
    parse(file.read(), 0)
	