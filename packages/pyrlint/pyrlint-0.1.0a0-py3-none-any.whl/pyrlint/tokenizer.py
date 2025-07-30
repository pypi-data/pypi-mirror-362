from dataclasses import dataclass, field
import re
import enum
from warnings import warn

__all__ = ['RTokenType', 'RToken', 'RTokenizerError', 'RInternalWarning', 'RTokenizer']

_REGEX_NUMBER = re.compile(r"[0-9]*(\.[0-9]*)?([eE][+-]?[0-9]*)?[Li]?")
_REGEX_HEX_NUMBER = re.compile(r"0x[0-9a-fA-F]*L?")
_REGEX_USER_OPERATOR = re.compile(r"%[^\n%]*%")
_REGEX_WHITESPACE = re.compile(r"[\s\u00A0\u3000]+")
_REGEX_COMMENT = re.compile(r"#[^\n]*$", re.MULTILINE)


class RTokenType(enum.IntEnum):
    LPAREN = 0                  # '('
    RPAREN = enum.auto()        # ')'
    LBRACKET = enum.auto()      # '['
    RBRACKET = enum.auto()      # ']'
    LDBRACKET = enum.auto()     # '[['
    RDBRACKET = enum.auto()     # ']]'
    LBRACE = enum.auto()        # '{'
    RBRACE = enum.auto()        # '}'
    COMMA = enum.auto()         # ','
    SEMI = enum.auto()          # ';'
    WHITESPACE = enum.auto()    # '\n', ' ', '\t', ...
    STRING = enum.auto()        # '"123"', 'r"123"', 'R"123"', ...
    NUMBER = enum.auto()        # '1e2', '.2', '3i', '4.44', ...
    ID = enum.auto()            # function names, variable names, attributes, '`123`'
    OPER = enum.auto()          # '+', '-', '%', '<-', ...
    UOPER = enum.auto()         # User operators: '%>%', '%>>>%', '%test%'
    ERR = enum.auto()           # Error, unresolved chars
    COMMENT = enum.auto()       # '#...'


@dataclass
class RToken:
    type: RTokenType = RTokenType.ERR
    content: str = ""
    offset: int = -1
    row: int = 0
    col: int = 0

    def __len__(self) -> int:
        return len(self.content)

    def __bool__(self) -> bool:
        return self.offset != -1

    @property
    def is_operator(self, op: str) -> bool:
        return self.type == RTokenType.OPER and self.content == op

    @property
    def is_binary_op(self) -> bool:
        if self.content == '!':
            return False
        return self.type in (RTokenType.OPER, RTokenType.UOPER)

    @property
    def is_local_left_assign(self) -> bool:
        return self.type == RTokenType.OPER and self.content in ("=", "<-", ":=")

    @property
    def is_local_right_assign(self) -> bool:
        return self.type == RTokenType.OPER and self.content == "->"

    @property
    def is_parent_left_assign(self) -> bool:
        return self.type == RTokenType.OPER and self.content == "<<-"

    @property
    def is_parent_right_assign(self) -> bool:
        return self.type == RTokenType.OPER and self.content == "->>"

    @property
    def is_left_assign(self) -> bool:
        return self.type == RTokenType.OPER and self.content in ("=", "<-", "<<-", ":=")

    @property
    def is_right_assign(self) -> bool:
        return self.type == RTokenType.OPER and self.content in ("->", "->>")

    @property
    def is_right_bracket(self) -> bool:
        return self.type in (RTokenType.RBRACE, RTokenType.RBRACKET, RTokenType.RDBRACKET, RTokenType.RPAREN)

    @property
    def is_left_bracket(self) -> bool:
        return self.type in (RTokenType.LBRACE, RTokenType.LBRACKET, RTokenType.LDBRACKET, RTokenType.LPAREN)

    @property
    def is_dollar(self) -> bool:
        return self.type == RTokenType.OPER and self.content == '$'

    @property
    def is_at(self) -> bool:
        return self.type == RTokenType.OPER and self.content == '@'

    @property
    def is_id(self) -> bool:
        return self.type == RTokenType.ID

    @property
    def is_namespace_extraction_operator(self) -> bool:
        return self.type == RTokenType.OPER and self.content in ('::', ':::')

    @property
    def is_function_keyword(self) -> bool:
        return self.type == RTokenType.ID and self.content in ('function', '\\')

    @property
    def is_string(self) -> bool:
        return self.type == RTokenType.STRING

    @property
    def is_comma(self) -> bool:
        return self.type == RTokenType.COMMA

    @property
    def is_whitespace(self) -> bool:
        return self.type == RTokenType.WHITESPACE

    @property
    def is_whitespace_or_comment(self) -> bool:
        return self.type in (RTokenType.WHITESPACE, RTokenType.COMMENT)

    @property
    def is_roxygen_comment(self) -> bool:
        if self.type != RTokenType.COMMENT:
            return False
        return re.match(r"^#*'", self.content)

    @property
    def is_valid_as_identifier(self) -> bool:
        return self.type in (RTokenType.ID, RTokenType.NUMBER, RTokenType.STRING)

    @property
    def has_newline(self) -> bool:
        return self.type == RTokenType.WHITESPACE and '\n' in self.content

    @property
    def is_valid_as_unary_operator(self) -> bool:
        return self.content in ("-", "+", "!", "?", "~")

    @property
    def can_start_expression(self) -> bool:
        return self.is_valid_as_unary_operator or self.is_valid_as_identifier or self.type == RTokenType.LPAREN

    @property
    def is_extraction_operator(self) -> bool:
        return self.is_namespace_extraction_operator or self.is_dollar or self.is_at

    @property
    def is_blank(self) -> bool:
        return self.is_whitespace and '\n' not in self.content

    @property
    def is_whitespace_with_newline(self) -> bool:
        return self.is_whitespace and '\n' in self.content

    @property
    def can_open_argument_list(self) -> bool:
        return self.type in (RTokenType.LPAREN, RTokenType.LBRACKET, RTokenType.LDBRACKET)

    @property
    def can_close_argument_list(self) -> bool:
        return self.type in (RTokenType.RPAREN, RTokenType.RBRACKET, RTokenType.RDBRACKET)

    @property
    def can_continue_statement(self) -> bool:
        return self.is_binary_op or self.can_open_argument_list

    def is_symbol_named(self, name: str) -> bool:
        if self.type == RTokenType.STRING or (
                self.type == RTokenType.ID and self.content.startswith('`')):
            if len(self.content) < 2:
                return False
            return self.content[1:-1] == name
        return self.content == name

    @property
    def can_follow_binary_operator(self) -> bool:
        if self.type in (RTokenType.ID, RTokenType.LBRACE, RTokenType.LPAREN, RTokenType.NUMBER, RTokenType.STRING):
            return True
        if self.is_valid_as_unary_operator:
            return True
        return False

    @property
    def is_pipe_operator(self) -> bool:
        return re.match(r'"^(%[^>]*>+[^>]*%)|([|]>)$"', self.content)

    @staticmethod
    def type_complement(lhs_type: RTokenType) -> RTokenType:
        if lhs_type == RTokenType.LPAREN:
            return RTokenType.RPAREN
        if lhs_type == RTokenType.LBRACE:
            return RTokenType.RBRACE
        if lhs_type == RTokenType.LBRACKET:
            return RTokenType.RBRACKET
        if lhs_type == RTokenType.LDBRACKET:
            return RTokenType.RDBRACKET

        if lhs_type == RTokenType.RPAREN:
            return RTokenType.LPAREN
        if lhs_type == RTokenType.RBRACE:
            return RTokenType.LBRACE
        if lhs_type == RTokenType.RBRACKET:
            return RTokenType.LBRACKET
        if lhs_type == RTokenType.RDBRACKET:
            return RTokenType.LDBRACKET
        return RTokenType.ERR

    @property
    def get_symbol_name(self) -> str:
        if self.type == RTokenType.STRING or (
                self.type == RTokenType.ID and self.content.startswith('`')):
            if len(self.content) < 2:
                return ''
            return self.content[1:-1]
        return self.content


class RTokenizerError(Exception):
    def __init__(self, reason: str, row=0, col=0):
        if row > 0 and col > 0:
            tag = f'[Ln {row}, Col {col}] '
        elif row > 0 and col == 0:
            tag = f'[Ln {row}] '
        else:
            tag = f''
        super().__init__(tag + reason)


class RInternalWarning(RuntimeWarning):
    def __init__(self, reason: str):
        super().__init__(f'R internal warning: {reason}')


class RTokenizer:
    def __init__(self,
                 data: str,
                 pos: int = 0,  # Full content string
                 end: int = None,
                 row: int = 0,
                 col: int = 0):
        self.data: str = data
        self.pos: int = pos
        self.end: int = len(data) if end is None else end
        self.row: int = row
        self.col: int = col
        self._brace_stack = []

    def _update_position(self, pos: int, length: int, row: int, col: int) -> tuple[int, int]:
        new_line_cnt = 0
        new_pos = -1
        for m in re.compile(r'\n').finditer(self.data, pos, pos + length):
            new_pos = m.start(0)
            new_line_cnt += 1
        if new_line_cnt == 0:
            col += length
        else:
            row += new_line_cnt
            col = length - (new_pos - pos) - 1
        return row, col

    def next_token(self):
        if self._is_eol:
            return RToken()
        c = self._peek()

        # check for raw string literals
        if c == 'r' or c == 'R':
            next = self._peek(1)
            if next == '"' or next == "'":
                try:
                    return self._match_raw_string_literal()
                except RTokenizerError:
                    pass

        match c:
            case '(':
                return self._consume_token(RTokenType.LPAREN, 1)
            case ')':
                return self._consume_token(RTokenType.RPAREN, 1)
            case '{':
                return self._consume_token(RTokenType.LBRACE, 1)
            case '}':
                return self._consume_token(RTokenType.RBRACE, 1)
            case ';':
                return self._consume_token(RTokenType.SEMI, 1)
            case ',':
                return self._consume_token(RTokenType.COMMA, 1)
            case '[':
                if self._peek(1) == '[':
                    self._brace_stack.append(RTokenType.LDBRACKET)
                    token = self._consume_token(RTokenType.LDBRACKET, 2)
                else:
                    self._brace_stack.append(RTokenType.LBRACKET)
                    token = self._consume_token(RTokenType.LBRACKET, 1)
                return token
            case ']':
                if len(self._brace_stack) == 0:  # TODO: warn?
                    if self._peek(1) == ']':
                        return self._consume_token(RTokenType.RDBRACKET, 2)
                    else:
                        return self._consume_token(RTokenType.RBRACKET, 1)
                else:
                    if self._peek(1) == ']':
                        top = self._brace_stack[len(self._brace_stack) - 1]
                        if top == RTokenType.LDBRACKET:
                            token = self._consume_token(RTokenType.RDBRACKET, 2)
                        else:
                            token = self._consume_token(RTokenType.RBRACKET, 1)
                    else:
                        token = self._consume_token(RTokenType.RBRACKET, 1)
                    self._brace_stack.pop()
                    return token
            case '"' | '\'' | '`':
                return self._match_delimited()
            case '#':
                return self._match_comment()
            case '%':
                return self._match_user_operator()
            case ' ' | '\t' | '\r' | '\n' | '\u00A0' | '\u3000':
                return self._match_whitespace()
            case '\\':
                return self._match_identifier()
            case '_':
                # R 4.2.0 introduced the pipe-bind operator
                # parse that as a special identifier.
                return self._consume_token(RTokenType.ID, 1)
        c_next = self._peek(1)
        if (c >= '0' and c <= '9') or (c == '.' and c_next >= '0' and c_next <= '9'):
            number_token = self._match_number()
            if len(number_token) > 0:
                return number_token
        if c.isalnum() or c == '.':
            # From Section 10.3.2, identifiers must not start with
            # a digit, nor may they start with a period followed by
            # a digit.
            #
            # Since we're not checking for either condition, we must
            # match on identifiers AFTER we have already tried to
            # match on number.
            return self._match_identifier()
        # check for embedded knitr chunks
        embedded_chunk = self._match_knitr_embedded_chunk()
        if embedded_chunk:
            return embedded_chunk
        oper = self._match_operator()
        if oper:
            return oper
        # Error
        return self._consume_token(RTokenType.ERR, 1)

    def _match_raw_string_literal(self) -> RToken:
        start = self.pos
        # consume leading 'r' or 'R'
        first_char = self._eat()
        if not (first_char == 'r' or first_char == 'R'):
            self.pos = start
            raise RTokenizerError("expected 'r' or 'R' at start of raw string literal", self.row, self.col)

        # consume quote character
        quoteChar = self._eat()
        if not (quoteChar == '"' or quoteChar == "'"):
            self.pos = start
            raise RTokenizerError("expected quote character at start of raw string literal", self.row, self.col)

        # consume an optional number of hyphens
        hyphenCount = 0
        ch = self._eat()
        while ch == '-':
            hyphenCount += 1
            ch = self._eat()

        # okay, we're now sitting on open parenthesis
        lhs = ch
        # form right boundary character based on consumed parenthesis.
        # if it wasn't a parenthesis, just look for the associated closing quote
        if lhs == '(':
            rhs = ')'
        elif lhs == '{':
            rhs = '}'
        elif lhs == '[':
            rhs = ']'
        else:
            self.pos = start
            raise RTokenizerError("expected opening bracket at start of raw string literal", self.row, self.col)

        # start searching for the end of the raw string
        valid = False
        while True:
            # i know, i know -- a label!? we use that here just because
            # we need to 'break' out of a nested loop below, and just
            # using a simple goto is cleaner than having e.g. an extra
            # boolean flag tracking whether we should 'continue'
            if self._is_eol:
                break

            # find the boundary character
            ch = self._eat()
            if ch != rhs:
                continue

            # consume hyphens
            is_continue = False
            for _ in range(hyphenCount):
                ch = self._peek()
                if ch != '-':
                    is_continue = True
                    break
                self.pos += 1
            if is_continue:
                continue

            # consume quote character
            ch = self._peek()
            if ch != quoteChar:
                continue
            self.pos += 1

            # we're at the end of the string; break out of the loop
            valid = True
            break

        row = self.row
        col = self.col
        self.row, self.col = self._update_position(start, self.pos - start, self.row, self.col)
        return RToken(RTokenType.STRING if valid else RTokenType.ERR, self.data[start:self.pos], start, row, col)

    def _match_whitespace(self) -> RToken:
        return self._consume_token(RTokenType.WHITESPACE, self._token_length(_REGEX_WHITESPACE))

    def _match_number(self) -> RToken:
        length = self._token_length(_REGEX_HEX_NUMBER)
        if length == 0:
            length = self._token_length(_REGEX_NUMBER)
        return self._consume_token(RTokenType.NUMBER, length)

    def _match_identifier(self) -> RToken:
        start = self.pos
        match = True
        while match:
            self._eat()
            ch = self._peek()
            match = ch.isalnum() or ch == '.' or ch == '_'
        row = self.row
        col = self.col
        self.row, self.col = self._update_position(start, self.pos - start, self.row, self.col)
        return RToken(RTokenType.ID, self.data[start:self.pos], start, row, col)

    def _match_comment(self) -> RToken:
        return self._consume_token(RTokenType.COMMENT, self._token_length(_REGEX_COMMENT))

    def _match_delimited(self) -> RToken:
        start = self.pos
        quote = self._eat()
        while not self._is_eol:
            ch = self._eat()
            # skip over escaped characters
            if ch == '\\':
                if not self._is_eol:
                    self._eat()
                    continue
            # check for matching quote
            if ch == quote:
                break
        # because delimited items can contain newlines,
        # update our row + col position after parsing the token
        row = self.row
        col = self.col
        self.row, self.col = self._update_position(start, self.pos - start, self.row, self.col)
        # NOTE: the Java version of the tokenizer returns a special RString_token
        # subclass which includes the well_formed flag as an attribute. Our
        # implementation of RToken is stack based so doesn't support subclasses
        # (because they will be sliced when copied). If we need the well
        # formed flag we can just add it onto RToken.
        return RToken(RTokenType.ID if quote == '`' else RTokenType.STRING,
                      self.data[start:self.pos],
                      start,
                      row,
                      col)

    def _match_user_operator(self) -> RToken:
        length = self._token_length(_REGEX_USER_OPERATOR)
        if length == 0:
            return self._consume_token(RTokenType.ERR, 1)
        else:
            return self._consume_token(RTokenType.UOPER, length)

    def _match_knitr_embedded_chunk(self) -> RToken:
        # bail if we don't start with '<<' here
        if self._peek(0) != '<' or self._peek(1) != '<':
            return RToken()
        # consume the chunk label, looking for '>>'
        offset = 1
        while True:
            # give up on newlines or EOF
            ch = self._peek(offset)
            if ch == '' or ch == '\n':
                return RToken()
            # look for closing '>>'
            if (self._peek(offset + 0) == '>' and
                    self._peek(offset + 1) == '>'):
                return self._consume_token(RTokenType.STRING, offset + 2)
            offset += 1
        # return RToken()

    def _match_operator(self) -> RToken:
        c_next = self._peek(1)
        match self._peek():
            case ':':  # :::, ::, :=
                if c_next == '=':
                    return self._consume_token(RTokenType.OPER, 2)
                elif c_next == ':':
                    c_next_next = self._peek(2)
                    return self._consume_token(RTokenType.OPER, (3 if c_next_next == ':' else 2))
                else:  # This condition is not included in rstudio tokenizer because of fall-through rule
                    return self._consume_token(RTokenType.OPER, 1)
            case '|':  # or, |>, |
                if c_next == '|' or c_next == '>':
                    return self._consume_token(RTokenType.OPER, 2)
                else:
                    return self._consume_token(RTokenType.OPER, 1)
            case '&':  # and, &
                return self._consume_token(RTokenType.OPER, (2 if c_next == '&' else 1))
            case '<':  # <=, <-, <<-, <
                if c_next == '=' or c_next == '-':  # <=, <-
                    return self._consume_token(RTokenType.OPER, 2)
                elif c_next == '<':
                    c_next_next = self._peek(2)
                    if c_next_next == '-':  # <<-
                        return self._consume_token(RTokenType.OPER, 3)
                else:  # plain old <
                    return self._consume_token(RTokenType.OPER, 1)
            case '-':  # also -> and ->>
                if c_next == '>':
                    c_next_next = self._peek(2)
                    return self._consume_token(RTokenType.OPER, (3 if c_next_next == '>' else 2))
                else:
                    return self._consume_token(RTokenType.OPER, 1)
            case '*':  # '*' and '**' (which R's parser converts to '^')
                return self._consume_token(RTokenType.OPER, (2 if c_next == '*' else 1))
            case '+' | '/' | '?' | '^' | '~' | '$' | '@':
                # single-character operators
                return self._consume_token(RTokenType.OPER, 1)
            case '>':  # also >=
                return self._consume_token(RTokenType.OPER, (2 if c_next == '=' else 1))
            case '=':  # also =>, ==
                if c_next == '=' or c_next == '>':
                    return self._consume_token(RTokenType.OPER, 2)
                else:
                    return self._consume_token(RTokenType.OPER, 1)
            case '!':  # also !=
                return self._consume_token(RTokenType.OPER, (2 if c_next == '=' else 1))
            case _:
                return RToken()

    @property
    def _is_eol(self) -> bool:
        return self.pos >= self.end

    def _peek(self, lookahead: int = 0) -> str:
        if self.end - self.pos <= lookahead:
            return ''
        return self.data[self.pos + lookahead]

    def _eat(self) -> str:
        ch = self.data[self.pos]
        self.pos += 1
        return ch

    def _token_length(self, regex: re.Pattern) -> int:
        m = regex.search(self.data, self.pos, self.end)
        if m:
            return m.end(0) - m.start(0)
        return 0

    def _eat_until(self, regex: re.Pattern) -> None:
        m = regex.search(self.data, self.pos, self.end)
        if m:
            self.pos = m.start(0)
        self.pos = self.end

    def _consume_token(self, typ: RTokenType, length: int) -> RToken:
        if length == 0:
            warn(f"Can't create zero-length token", category=RInternalWarning)
            return RToken()
        if self.pos + length > self.end:
            warn(f"Premature EOF", category=RInternalWarning)
            return RToken()
        row = self.row
        col = self.col
        self.row, self.col = self._update_position(self.pos, length, self.row, self.col)
        start = self.pos
        self.pos += length
        return RToken(typ, self.data[start: self.pos], start, row, col)
