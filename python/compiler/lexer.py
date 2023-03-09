import ply.lex as lex

tokens = (
	'PROGRAM', 'BEGIN', 'END', 'PROCEDURE', 'IS', 'VAR',
	'IF','THEN', 'ELSE', 'ENDIF', 'WHILE', 'DO', 'ENDWHILE', 'REPEAT', 'UNTIL',
	'READ', 'WRITE', 'ASSIGN', 'PLUS', 'MINUS', 'DIVIDE', 'MULTIPLY', 'MODULO', 'EQ', 'NEQ', 'LT', 'GT', 'LEQ', 'GEQ',	
	'SEMICOLON', 'LBR', 'RBR', 'COMMA', 'ID', 'NUM'								
)

t_ignore_COM = r'\[[^\]]*\]'
t_ignore  = ' \t'
t_PROGRAM = r'PROGRAM'
t_BEGIN	= r'BEGIN'
t_END = r'END'
t_PROCEDURE = r'PROCEDURE'
t_IS = r'IS'
t_VAR = r'VAR'
t_IF = r'IF'
t_THEN = r'THEN'
t_ELSE = r'ELSE'
t_ENDIF = r'ENDIF'
t_DO = r'DO'
t_WHILE = r'WHILE'
t_ENDWHILE = r'ENDWHILE'
t_REPEAT = r'REPEAT'
t_UNTIL = r'UNTIL'
t_READ	= r'READ'
t_WRITE	= r'WRITE'
t_ASSIGN = r':='
t_PLUS	= r'\+'
t_MINUS	= r'\-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'\/'
t_MODULO = r'\%'
t_EQ = r'='
t_NEQ = r'!='
t_LEQ = r'<='
t_LT = r'<'
t_GEQ = r'>='
t_GT = r'>'
t_LBR = r'\('
t_RBR = r'\)'
t_SEMICOLON	= r';'
t_COMMA = r','
t_ID = r'[_a-z]+'

def t_NUM(t):
	r'\d+'
	t.value = int(t.value)
	return t

def t_newline(t):
	r'\r?\n+'
	t.lexer.lineno += len(t.value)

def t_error(t):
	print("Error: Wrong char '%s' at line " % t.value[0] + str(t.lexer.lineno))
	t.lexer.skip(1)

lexer = lex.lex()

