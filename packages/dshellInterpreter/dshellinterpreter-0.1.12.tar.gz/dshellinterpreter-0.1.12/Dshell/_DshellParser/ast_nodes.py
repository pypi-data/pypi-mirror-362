from typing import Optional, Any

from .._DshellTokenizer.dshell_token_type import Token

__all__ = [
    'ASTNode',
    'StartNode',
    'ElseNode',
    'ElifNode',
    'IfNode',
    'LoopNode',
    'ArgsCommandNode',
    'CommandNode',
    'VarNode',
    'EndNode',
    'FieldEmbedNode',
    'EmbedNode',
    'SleepNode',
    'IdentOperationNode',
    'ListNode',
    'PermissionNode'
]


class ASTNode:
    """
    Base class for all AST nodes.
    """
    pass


class StartNode(ASTNode):
    """
    Node representing the start of the AST.
    """
    def __init__(self, body: list):
        self.body = body

    def __repr__(self):
        return f"<Command> - {self.body}"


class ElseNode(ASTNode):
    """
    Node representing the 'else' part of an if statement.
    """
    def __init__(self, body: list[Token]):
        """
        :param body: list of tokens representing the body of the else statement
        """
        self.body = body

    def __repr__(self):
        return f"<Else> - {self.body}"


class ElifNode(ASTNode):
    """
    Node representing an 'elif' part of an if statement.
    """
    def __init__(self, condition: list[Token], body: list[Token], parent: "IfNode"):
        """
        :param condition: list of tokens representing the condition for the elif
        :param body: list of tokens representing the body of the elif
        :param parent: the if node that this elif belongs to
        """
        self.condition = condition
        self.body = body
        self.parent = parent

    def __repr__(self):
        return f"<Elif> - {self.condition} - {self.body}"


class IfNode(ASTNode):
    """
    Node representing an 'if' statement, which can contain 'elif' and 'else' parts.
    """
    def __init__(self, condition: list[Token], body: list[Token], elif_nodes: Optional[list[ElifNode]] = None,
                 else_body: Optional[ElseNode] = None):
        """
        :param condition: list of tokens representing the condition for the if statement
        :param body: list of tokens representing the body of the if statement
        :param elif_nodes: optional list of ElifNode instances representing 'elif' parts
        :param else_body: optional ElseNode instance representing the 'else' part
        """
        self.condition = condition
        self.body = body
        self.elif_nodes = elif_nodes
        self.else_body = else_body

    def __repr__(self):
        return f"<If> - {self.condition} - {self.body} *- {self.elif_nodes} **- {self.else_body}"


class LoopNode(ASTNode):
    """
    Node representing a loop structure in the AST.
    """
    def __init__(self, variable: "VarNode", body: list):
        """
        :param variable: VarNode representing the loop variable. This variable will be used to iterate over the body. Can contain a ListNode, string or integer.
        :param body: list of tokens representing the body of the loop
        """
        self.variable = variable
        self.body = body

    def __repr__(self):
        return f"<Loop> - {self.variable.name} -> {self.variable.body} *- {self.body}"


class ArgsCommandNode(ASTNode):
    """
    Node representing the arguments of a command in the AST.
    """
    def __init__(self, body: list[Token]):
        """
        :param body: list of tokens representing the arguments of the command
        """
        self.body: list[Token] = body

    def __repr__(self):
        return f"<Args Command> - {self.body}"


class CommandNode(ASTNode):
    """
    Node representing a command in the AST.
    """
    def __init__(self, name: str, body: ArgsCommandNode):
        """
        :param name: The command name (e.g., "sm", "cc")
        :param body: ArgsCommandNode containing the arguments of the command
        """
        self.name = name
        self.body = body

    def __repr__(self):
        return f"<{self.name}> - {self.body}"


class VarNode(ASTNode):
    """
    Node representing a variable declaration in the AST.
    """
    def __init__(self, name: Token, body: list[Token]):
        """
        :param name: Token representing the variable name
        :param body: list of tokens representing the body of the variable
        """
        self.name = name
        self.body = body

    def __repr__(self):
        return f"<VAR> - {self.name} *- {self.body}"


class EndNode(ASTNode):
    """
    Node representing the end of the AST.
    """
    def __init__(self):
        pass

    def __repr__(self):
        return f"<END>"


class FieldEmbedNode(ASTNode):
    """
    Node representing a field in an embed structure.
    """
    def __init__(self, body: list[Token]):
        """
        :param body: list of tokens representing the field content
        """
        self.body: list[Token] = body

    def __repr__(self):
        return f"<EMBED_FIELD> - {self.body}"


class EmbedNode(ASTNode):
    """
    Node representing an embed structure in the AST.
    """
    def __init__(self, body: list[Token], fields: list[FieldEmbedNode]):
        """
        :param body: list of tokens representing the embed content
        :param fields: list of FieldEmbedNode instances representing the fields of the embed
        """
        self.body = body
        self.fields = fields

    def __repr__(self):
        return f"<EMBED> - {self.body}"


class PermissionNode(ASTNode):
    """
    Node representing a permission structure in the AST.
    """
    def __init__(self, body: list[Token]):
        """
        :param body: list of tokens representing the permission content
        """
        self.body = body

    def __repr__(self):
        return f"<PERMISSION> - {self.body}"


class SleepNode(ASTNode):
    """
    Node representing a sleep command in the AST.
    """
    def __init__(self, body: list[Token]):
        """
        :param body: list of tokens representing the sleep duration
        """
        self.body = body

    def __repr__(self):
        return f"<SLEEP> - {self.body}"


class IdentOperationNode(ASTNode):
    """
    Node representing an operation on an identifier in the AST.
    Manages operations on idendifiers (function calls)
    Ensure that the function call returns the associated class to allow nesting. Not mandatory in itself if it returns something
    """

    def __init__(self, ident: Token, function: Token, args: Token):
        """
        :param ident: Token representing the identifier (e.g., a class or object)
        :param function: Token representing the function to be called on the identifier
        :param args: Token representing the arguments passed to the function
        """
        self.ident = ident
        self.function = function
        self.args = args

    def __repr__(self):
        return f"<IDENT OPERATION> - {self.ident}.{self.function}({self.args})"


class ListNode(ASTNode):
    """
    Node representing a list structure in the AST.
    Iterable class for browsing lists created from Dshell code.
    This class also lets you interact with the list via specific methods not built in by python.
    """

    def __init__(self, body: list[Any]):
        """
        :param body: list of elements to initialize the ListNode with
        """
        self.iterable: list[Any] = body
        self.len_iterable: int = len(body)
        self.iterateur_count: int = 0

    def add(self, value: Any):
        """
        Add a value to the list.
        """
        if self.len_iterable > 10000:
            raise PermissionError('The list is too long, it must not exceed 10,000 elements !')

        self.iterable.append(value)
        self.len_iterable += 1

    def remove(self, value: Any, number: int = 1):
        """
        Remove a value from the list.
        """
        if number < 1:
            raise Exception(f"The number of elements to remove must be at least 1, not {number} !")

    def __add__(self, other: "ListNode"):
        """
        Add another ListNode to this one.
        :param other: Another ListNode to add to this one.
        :return: Instance of ListNode with combined elements.
        """
        for i in other:
            self.add(i)
        return self

    def __iter__(self):
        return self

    def __next__(self):
        """
        Iterate over the elements of the list.
        :return: an element from the list.
        """

        if self.iterateur_count >= self.len_iterable:
            self.iterateur_count = 0
            raise StopIteration()

        v = self.iterable[self.iterateur_count]
        self.iterateur_count += 1
        return v

    def __len__(self):
        return self.len_iterable

    def __getitem__(self, item):
        return self.iterable[item]

    def __bool__(self):
        return bool(self.iterable)

    def __repr__(self):
        return f"<LIST> - {self.iterable}"
