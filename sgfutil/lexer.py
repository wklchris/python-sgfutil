from ply import lex

class SgfLexer(object):
    tokens = (
        # Delimeters
        "SEMICOLON",
        "LPAREN", 'RPAREN',
        'LBRACKET', 'RBRACKET',
        # PROP types
        "PROP",
        # Value types
        "INT", "REAL",
        "POINT",
        "TEXT"
    )

    t_SEMICOLON = r';'
    t_LPAREN    = r'\('
    t_RPAREN    = r'\)'
    t_LBRACKET  = r'\['
    t_RBRACKET  = r'\]'
    t_PROP      = r'[A-Z]{1,10}'

    def t_INT(self, t):
        r'[\+\-]?[0-9]+'
        t.value = int(t.value)
        return t

    def t_REAL(self, t):
        r'[\+\-]?[0-9]+\.[0-9]*'
        t.value = float(t.value)
        return t

    t_POINT     = r'[a-z]{2}'
    # TEXT can have an escaped rbracket '\]' inside. 
    t_TEXT      = r'(?<=\[)[\s\S]+?[^\\](?=\])'


    def t_error(self, t):
        print(f"Illegal character {t.value[0]!r} at line {t.lexer.lineno}")
        # t.lexer.skip(1)
        exit()
    
    def t_newline(self,t):
         r'\n+'
         t.lexer.lineno += t.value.count("\n")
    
    # Build function for a lexer class
    def __init__(self):
        self.lexer = lex.lex(module=self)

    # Test function (optional)
    def test(self, data):
        self.lexer.input(data)
        while True:
            tok = self.lexer.token()
            if not tok: 
                break
            print(tok)
