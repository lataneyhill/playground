#!/usr/bin/env python3

# Terminals ~ Token
# Non-Terminals ~ Variables (compounding of tokens)

### GRAMMAR ###
# expr ::= constant
#      |   let [rec] let-binding { and let-binding } in expr
# constant ::= false
#          |   true
#          |   ()
# let-binding ::= value-name { parameter } [: typexpr] [:> typexpr] = expr
# value-name ::= lowercase-ident
# letter ::= A...Z | a...z
# lowercase-ident ::= (a...z | _) { letter | 0...9 | _ | ' }

import abc, enum
from typing import Optional


class TokenType(enum.Enum):
    # Keywords
    AND = enum.auto()
    FALSE = enum.auto()
    IN = enum.auto()
    LET = enum.auto()
    REC = enum.auto()
    TRUE = enum.auto()

    # Literals
    LOWERCASE_IDENT = enum.auto()

    # Symbols
    EQUAL = enum.auto()
    UNIT = enum.auto()

    EOF = enum.auto()


class Token:
    def __init__(self, typ, lexeme, literal=None):
        self.typ = typ
        self.lexeme = lexeme
        self.literal = literal

    def __str__(self):
        return "Token({}, {}, {})".format(self.typ, self.lexeme, self.literal)

    def __repr__(self):
        return str(self)


class Lexer:
    def __init__(self, text: str):
        self._text = text
        self._pos: int = 0
        self._char: Optional[str] = text[self._pos]
        self._keywords = {
            "and": TokenType.AND,
            "false": TokenType.FALSE,
            "in": TokenType.IN,
            "let": TokenType.LET,
            "rec": TokenType.REC,
            "true": TokenType.TRUE,
            "unit": TokenType.UNIT,
        }
        self._symbols = {"=": TokenType.EQUAL}

    def _advance(self):
        self._pos += 1
        if self._pos >= len(self._text):
            self._char = None
        else:
            self._char = self._text[self._pos]
        return self._char

    def _match(self, ch):
        if self._pos < len(self._text) and self._char == ch:
            self._advance()
            return True
        return False

    def _symbol(self):
        if self._char == "(":
            self._advance()
            if self._match(")"):
                return Token(TokenType.UNIT, "()")

        if self._char in self._symbols:
            assert self._char is not None
            lexeme = self._char
            typ = self._symbols[self._char]
            self._advance()
            return Token(typ, lexeme)

        return None

    def _lowercase_ident(self):
        """
        >>> for v in ["_", "_myIdent", "Bad", "good12'", "in", "falsetrue"]:
        ...     lexer = Lexer(v)
        ...     lexer._lowercase_ident()
        Token(TokenType.LOWERCASE_IDENT, _, None)
        Token(TokenType.LOWERCASE_IDENT, _myIdent, None)
        Token(TokenType.LOWERCASE_IDENT, good12', None)
        Token(TokenType.IN, in, None)
        Token(TokenType.LOWERCASE_IDENT, falsetrue, None)
        """
        start = self._pos
        ch = self._char
        if ch is not None and (ch.islower() or ch == "_"):
            ch = self._advance()
        else:
            return None

        while ch is not None and (ch.isalnum() or ch in "_'"):
            ch = self._advance()

        lexeme = self._text[start : self._pos]
        if lexeme in self._keywords:
            typ = self._keywords[lexeme]
        else:
            typ = TokenType.LOWERCASE_IDENT
        return Token(typ, lexeme)

    def _skip_space(self):
        while self._char is not None and self._char.isspace():
            self._advance()

    def get_next_token(self):
        """
        >>> lexer = Lexer("let rec f = ()")
        >>> lexer.get_next_token()
        Token(TokenType.LET, let, None)
        >>> lexer.get_next_token()
        Token(TokenType.REC, rec, None)
        >>> lexer.get_next_token()
        Token(TokenType.LOWERCASE_IDENT, f, None)
        >>> lexer.get_next_token()
        Token(TokenType.EQUAL, =, None)
        >>> lexer.get_next_token()
        Token(TokenType.UNIT, (), None)
        """
        while self._char is not None:
            if self._char.isspace():
                self._skip_space()
                if self._char is None:
                    break

            for method in (self._symbol, self._lowercase_ident):
                result = method()
                if result is not None:
                    return result

            raise Exception("Lexer: invalid")

        return Token(TokenType.EOF, None)


class AST(abc.ABC):
    def __repr__(self):
        return str(self)

    @abc.abstractmethod
    def __str__(self):
        pass

    @abc.abstractmethod
    def visit(self, visitor):
        pass


class Constant(AST):
    def __init__(self, typ):
        self.typ = typ

    def __str__(self):
        return "Constant({})".format(self.typ)

    def visit(self, visitor):
        visitor.acceptConstant(self)


class ValueName(AST):
    def __init__(self, token):
        self.token = token

    def __str__(self):
        return "ValueName({})".format(self.token)

    def visit(self, visitor):
        visitor.acceptValueName(self)

class LetBinding(AST):
    def __init__(self, value_name, expr):
        self.value_name = value_name
        self.expr = expr
    def __str__(self):
        return "LetBinding({}, {})".format(self.value_name, self.expr)
    def visit(self, visitor):
        visitor.acceptLetBinding(self)

class ExprConstant(AST):
    def __init__(self, constant):
        self.constant = constant

    def __str__(self):
        return "ExprConstant({})".format(self.constant)

    def visit(self, visitor):
        visitor.acceptExprConstant(self)


class ExprLet(AST):
    def __init__(self, rec, let_bindings, expr):
        self.rec = rec
        self.let_bindings = let_bindings
        self.expr = expr

    def __str__(self):
        return "ExprLet({}, {}, {})".format(self.rec, self.let_bindings, self.expr)

    def visit(self, visitor):
        visitor.acceptExprLet(self)

class Parser:
    def __init__(self, lexer):
        self._lexer = lexer
        self._token: Token = lexer.get_next_token()

    def _eat(self, typ):
        if self._token.typ == typ:
            self._token = self._lexer.get_next_token()
        else:
            raise Exception("Parser: invalid")

    def _constant(self):
        if self._token.typ in (TokenType.FALSE, TokenType.TRUE, TokenType.UNIT):
            typ = self._token.typ
            self._eat(typ)
            return Constant(typ)
        return None

    def _let_binding(self):
        value_name = self._value_name()
        self._eat(TokenType.EQUAL)
        expr = self._expr()
        return LetBinding(value_name, expr)

    def _value_name(self):
        token = self._token
        self._eat(TokenType.LOWERCASE_IDENT)
        return ValueName(token)

    def _expr(self):
        constant = self._constant()
        if constant is not None:
            return ExprConstant(constant)

        self._eat(TokenType.LET)
        rec = False
        if self._token.typ == TokenType.REC:
            self._eat(TokenType.REC)
            rec = True
        let_binding = self._let_binding()
        self._eat(TokenType.IN)
        expr = self._expr()
        return ExprLet(rec, let_binding, expr)

    def parse(self):
        return self._expr()


class PrettyPrinter:
    def __init__(self):
        self.output = ""
    def acceptConstant(self, v: Constant):
        self.output += str(v.typ)
    def acceptExprConstant(self, v: ExprConstant):
        v.constant.visit(self)
    def acceptExprLet(self, v: ExprLet):
        self.output += "let "
        if v.rec:
            self.output += "rec "
        v.let_bindings.visit(self)
        self.output += " in "
        v.expr.visit(self)
    def acceptLetBinding(self, v: LetBinding):
        v.value_name.visit(self)
        self.output += " = "
        v.expr.visit(self)
    def acceptValueName(self, v: ValueName):
        self.output += v.token.lexeme


def main():
    import doctest, sys

    if "-test" in sys.argv:
        doctest.testmod()
    else:
        input = "let rec f = false in ()"
        lexer = Lexer(input)
        expr = Parser(lexer).parse()
        pp = PrettyPrinter()
        expr.visit(pp)
        print("INPUT:  " + input)
        print("OUTPUT: " + pp.output)


if __name__ == "__main__":
    main()
