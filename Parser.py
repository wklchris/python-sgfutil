from ply import lex
from ply import yacc

tokens = (
    "PROP", "VALUE",
    "SEMICOLON",
    "LBRANCH", 'RBRANCH'
)

t_SEMICOLON = r';'
t_LBRANCH   = r'\(;'
t_RBRANCH   = r'\)'


# Lexer part
def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    err_msg = f"Illegal character {t.value[0]!r} in line {t.lineno}."
    print(err_msg)


## Normal lex definitions
def t_PROP(t):
    r'[A-Z]{1,10}'
    return t

def t_VALUE(t):
    r'\[[\S\s]*?(?<!\\)\]'
    return t


# Yacc part

def p_error(t):
    err_msg = f"Yacc error at {t}"
    print(err_msg)

def p_out(t):
    '''out : LBRANCH itemlst RBRANCH
           | LBRANCH RBRANCH'''
    if len(t) == 4:
        t[0] = t[2]
    else:
        t[0] = []

def p_itemlst(t):
    '''itemlst : item
               | item itemlst
               | item SEMICOLON itemlst'''
    # When there is only one item in the itemlst
    if len(t) == 2:
        t[0] = [t[1]]
    # Return example: [['B', 'pb'], ['W', 'pd']]
    else:
        t[0] = [t[1], *t[len(t)-1]]

def p_item(t):
    '''item : PROP val
            | item val'''
    # When a PROP is matched, let R[0] = [PROP[0], val(0)].
    if t.slice[1].type == 'PROP':
        t[0] = [t[1], t[2]]
    # Otherwise, let R[i+1] = [*R[0], val(i)].
    #   Return example: ['AW', 'pa', 'pb']
    else:
        t[0] = [*t[1], t[2]] 

def p_val(t):
    '''val : VALUE'''
    t[0] = t[1].strip('[]')


# --- Main ---

def parse_sgf(sgf_file):
    lexer = lex.lex()
    parser = yacc.yacc()

    def _parse(sgf_file):
        with open(sgf_file, 'r', encoding='utf-8') as f:
            sgf_raw = f.read()
        sgf_parsed = parser.parse(sgf_raw)
        return sgf_parsed

    res = _parse(sgf_file)
    return res

