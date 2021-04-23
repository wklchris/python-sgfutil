class GameProp(object):
    """
    GameProp is a single property key-value pair in the SGF. 
    For example, "B[qd]" is a GameProp with prop=B, val=qd, nodetype=MOVE.
        For a full list of defined notdetype, see SgfLexer.tokens.
    A GameNode can have multiple GameProp.
        The id of a GameProp indicates the its # in the parent GameNode.
    """
    def __init__(self, prop=None, val=None, nodetype=None, id=0):
        self.prop = prop
        self.val = val
        self.nodetype = nodetype
        self.id = id  # id inside the node
    
    def __repr__(self):
        s = f"{self.prop}: {self.val} ({self.nodetype})"
        return s

    def update_node(self, **kwargs):
        self.__dict__.update(kwargs)


class GameNode(object):
    """
    GameNode is the middle-level component of a SGF. It contains one or more GameProp.
    
    Args:
    * parent: Type of GameNode. If it is the root, set parent=None.
    * children: Type of a list of GameNode. If it is a leaf, set children=[].
    * branch: Integer. The # of branch that the GameNode belongs to.
    """
    def __init__(self, parent=None, children=[], branch=0):
        self.parent = parent
        self.id = self.parent.id + 1 if parent else 0  # id inside the branch
        self.children = children
        self.branch = branch
    
    def __repr__(self):
        s_prefix = f"@{self.branch:0>3d}-{self.id:0>3d} ~ "
        sep = '; \n'
        sep = sep.ljust(len(s_prefix) + len(sep))
        s_props = sep.join([gp.__repr__() for gp in self.children])
        return s_prefix + s_props
