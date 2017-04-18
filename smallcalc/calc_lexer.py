from smallcalc import text_buffer
from smallcalc import tok as token

EOF = 'EOF'
EOL = 'EOL'
INTEGER = 'INTEGER'
LITERAL = 'LITERAL'


class CalcLexer:

    def __init__(self, text=''):
        self._text_storage = text_buffer.TextBuffer(text)

    def load(self, text):
        self._text_storage.load(text)

    @property
    def _current_char(self):
        return self._text_storage.current_char

    @property
    def _current_line(self):
        return self._text_storage.current_line

    def _set_current_token_and_skip(self, token):
        self._text_storage.skip(len(token))

        self._current_token = token
        return token

    def _process_eol(self):
        try:
            self._current_char
            return None
        except text_buffer.EOLError:
            self._text_storage.newline()

            return self._set_current_token_and_skip(
                token.Token(EOL)
            )

    def _process_eof(self):
        try:
            self._current_line
            return None
        except text_buffer.EOFError:
            return self._set_current_token_and_skip(
                token.Token(EOF)
            )

    def _process_literal(self):
        return self._set_current_token_and_skip(
            token.Token(LITERAL, self._current_char)
        )

    def _process_integer(self):
        if not self._current_char.isdigit():
            return None

        return self._set_current_token_and_skip(
            token.Token(INTEGER, self._current_char)
        )

    def get_token(self):
        eof = self._process_eof()
        if eof:
            return eof

        eol = self._process_eol()
        if eol:
            return eol

        integer = self._process_integer()
        if integer:
            return integer

        literal = self._process_literal()
        if literal:
            return literal

    def get_tokens(self):
        t = self.get_token()
        tokens = []

        while t != token.Token('EOF'):
            tokens.append(t)
            t = self.get_token()

        tokens.append(token.Token('EOF'))

        return tokens