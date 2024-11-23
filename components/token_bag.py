from token import Token


class TokenBag:
    def __init__(self) -> None:
        self.tokens: list[Token] = self._fill_with_tokens()

    @staticmethod
    def _fill_with_tokens(self) -> list[Token]:
        tokens = []
        for t in Token:
            if t == Token.purple:
                tokens.extend([t] * 2)  # add 2 purple tokens
            elif t == Token.gold:
                tokens.extend([t] * 3)  # add 3 yellow tokens
            else:
                tokens.extend([t] * 4)  # add 4 tokens for other colors
        return tokens

    def add_token(self, token: Token) -> None:
        self.tokens.append(token)

    def take_token(self) -> Token:
        return self.tokens.pop()