from dataclasses import dataclass
from random import shuffle
from typing import Optional

from token import Token
from token_bag import TokenBag


@dataclass
class TokenBoardField:
    x: int
    y: int
    token: Optional[Token] = None

    def __post_init__(self):
        if not (1 <= self.x <= 5) or not (1 <= self.y <= 5):
            raise ValueError(f"Coordinates {self.x}, {self.y} are out of bounds (1-5)")


class TokenBoard:
    def __init__(self) -> None:
        self.fields = [
            [TokenBoardField(x + 1, y + 1, token=None) for y in range(5)]
            for x in range(5)
        ]

    def replenish(self, token_bag: TokenBag) -> TokenBag:
        shuffle(token_bag.tokens)

        for coord in BOARD_REPLENISH_ORDER:
            field = self._get_field(coord)
            if field.token is None:
                if token_bag.tokens:
                    field.token = token_bag.take_token()
                else:
                    print("No tokens left in the bag.")
                    break

        print(self.fields)  # TODO: for temporary QA, remove
        return token_bag

    def _get_field(self, coord: tuple[int, int]) -> TokenBoardField:
        x, y = coord
        if not (1 <= x <= 5) or not (1 <= y <= 5):
            raise ValueError(f"Coordinates {x}, {y} are out of bounds (1-5)")
        return self.fields[x - 1][y - 1]


BOARD_REPLENISH_ORDER = [
    (3, 3),
    (3, 4),
    (2, 4),
    (2, 3),
    (2, 2),
    (3, 2),
    (4, 2),
    (4, 3),
    (4, 4),
    (4, 5),
    (3, 5),
    (2, 5),
    (1, 5),
    (1, 4),
    (1, 3),
    (1, 2),
    (1, 1),
    (2, 1),
    (3, 1),
    (4, 1),
    (5, 1),
    (5, 2),
    (5, 3),
    (5, 4),
    (5, 5),
]