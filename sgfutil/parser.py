from .lexer import SgfLexer
from ply import yacc
from .tree import GameNode, GameProp

class SgfParserNative(object):
    '''
    A sgf parser that parses SGFs in Python's native data structures,
        i.e. combination of Lists & tuples.
    Each node in the game is recorded as a tuple: (key, val, nodetype),
        where nodetype is defined by SgfLexer.tokens.
    For example, "B[pd]" is interpreted as ('B', 'pd', 'MOVE').
    '''
    tokens = SgfLexer.tokens
    
    def p_colection(self, p):
        '''collection : tree
                      | tree collection'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = [p[1], *p[2]]

    def p_tree(self, p):
        '''tree : LPAREN seq RPAREN
                | LPAREN seq tree RPAREN
                | LPAREN seq RPAREN tree'''
        # A tree can either be nested in an outer tree,
        #     or follow a previous tree after RPAREN.
        if len(p) == 4:
            p[0] = [p[2]]
        elif p.slice[4].type == 'RPAREN':
            p[0] = [p[2], *p[3]]
        else:
            p[0] = [p[2], *p[4]]
    
    def p_seq(self, p):
        '''seq : node
               | node seq'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = [p[1], *p[2]]
    
    def p_node(self, p):
        '''node : SEMICOLON property
                | node property'''
        if p[1] == ';':
            p[0] = (p[2],)
        else:
            p[0] = (*p[1], p[2])
    
    def p_property(self, p):
        '''property : MOVE val
                    | SETUP val
                    | NODEANNO val
                    | MOVEANNO val
                    | MARKUP val
                    | ROOT val
                    | GAMEINFO val
                    | TIMING val
                    | PROP val
                    | property val'''
        if p.slice[1].type in 'MOVE SETUP NODEANNO MOVEANNO MARKUP ROOT GAMEINFO TIMING PROP':
            p[0] = (p[1], p[2], p.slice[1].type)
        # Append new val p[2] to the existing val list.
        elif isinstance(p[1][1], list):
            p[0] = (p[1][0], [*p[1][1], p[2]], p[1][2])
        else:
            p[0] = (p[1][0], [p[1][1], p[2]], p[1][2])
    
    def p_val(self, p):
        '''val : LBRACKET INT RBRACKET
               | LBRACKET REAL RBRACKET
               | LBRACKET POINT RBRACKET
               | LBRACKET TEXT RBRACKET'''
        p[0] = p[2]

    def p_error(self, p):
        capture_len = 30
        capture_str = p.lexer.lexdata[p.lexpos:p.lexpos+capture_len]
        err_msg = f'Yacc error at line {p.lexer.lineno}: "{capture_str} ..."'
        print(err_msg)
        exit()

    def __init__(self, sgf_lexer=None):
        self.lexer = sgf_lexer if sgf_lexer else SgfLexer()
        self.parsed_sgf = None
    
    def __repr__(self):
        if not self.parsed_sgf:
            return "Use sgf_parse(data) to parse."
        s = ''
        for treeidx, tree in enumerate(self.parsed_sgf):
            s += f'\n--- Branch #{treeidx} ---\n'
            for node in tree:
                s += str(node) + '\n'
        return s
    
    def sgf_parse(self, inputstr, debug=False):
        self.parser = yacc.yacc(module=self)
        if inputstr.endswith('.sgf'):
            with open(inputstr, 'r', encoding='utf-8') as f:
                self.parsed_sgf = self.parser.parse(f.read(), debug=debug)
        else:
            self.parsed_sgf = self.parser.parse(inputstr, debug=debug)


class SgfParser(SgfParserNative):
    '''
    Overwrite the SgfParserNative parser to record each node in class GameProp.
    '''
    def p_node(self, p):
        '''node : SEMICOLON property
                | node property'''
        if p[1] == ';':
            p[0] = GameNode(children=[p[2]])
        else:
            # p[0] = (*p[1], p[2])
            p[0] = GameNode(children=[*p[1].children, p[2]])

    def p_property(self, p):
        '''property : MOVE val
                    | SETUP val
                    | NODEANNO val
                    | MOVEANNO val
                    | MARKUP val
                    | ROOT val
                    | GAMEINFO val
                    | TIMING val
                    | PROP val
                    | property val'''
        if p.slice[1].type in 'MOVE SETUP NODEANNO MOVEANNO MARKUP ROOT GAMEINFO TIMING PROP':
            # p[0] = (p[1], p[2], p.slice[1].type)
            p[0] = GameProp(prop=p[1], val=p[2], nodetype=p.slice[1].type)
        # Append new val p[2] to the existing val list.
        elif isinstance(p[1][1], list):
            # p[0] = (p[1][0], [*p[1][1], p[2]], p[1][2])
            p[0] = GameProp(prop=p[1].prop, val=[*p[1].val, p[2]], nodetype=p[1].nodetype)
        else:
            # p[0] = (p[1][0], [p[1][1], p[2]], p[1][2]) 
            p[0] = GameProp(prop=p[1].prop, val=[p[1].val, p[2]], nodetype=p[1].nodetype)
    
    def __repr__(self):
        if not self.parsed_sgf:
            return "Use sgf_parse(data) to parse."
        s = ''
        for treeidx, tree in enumerate(self.parsed_sgf):
            s += f'\n--- Branch #{treeidx} ---\n'
            for node in tree:
                s += node.__repr__() + '\n'
        return s