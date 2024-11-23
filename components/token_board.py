from dataclasses import dataclass
from random import shuffle
from typing import Optional

from components.t0ken import Token
from components.token_bag import TokenBag


@dataclass
class TokenBoardField:
    row: int
    col: int
    token: Optional[Token] = None

    def __post_init__(self):
        if not (1 <= self.row <= 5) or not (1 <= self.col <= 5):
            raise ValueError(
                f"Coordinates {self.row}, {self.col} are out of bounds (1-5)"
            )


class TokenBoard:
    def __init__(self) -> None:
        self.fields = [
            [TokenBoardField(row + 1, col + 1, token=None) for col in range(5)]
            for row in range(5)
        ]

    def _get_field(self, coord: tuple[int, int]) -> TokenBoardField:
        row, col = coord
        if not (1 <= row <= 5) or not (1 <= col <= 5):
            raise ValueError(f"Coordinates {row}, {col} are out of bounds (1-5)")
        return self.fields[row - 1][col - 1]

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

        # return empty bag for game continuity
        # TODO: attach TokenBag instance to TokenBoard instead?
        return token_bag

    def take_tokens(self, coords: list[tuple[int, int]]) -> list[Token]:
        # TODO: hook this up to the matplotlib chart
        if len(coords) > 3:
            raise ValueError("Cannot take tokens from more than three fields.")

        if not coords:
            raise ValueError("Must take at least one token.")

        fields: list[TokenBoardField] = [self._get_field(coord) for coord in coords]

        # Check if all passed fields have tokens
        if any(field.token is None for field in fields):
            raise ValueError("Cannot take tokens from empty fields.")

        # If more than one token is taken, check adjacency and alignment of fields
        if len(fields) > 1:
            # Each pair of consecutive fields in the sorted list must be adjacent
            for i in range(len(fields) - 1):
                if (
                    abs(fields[i].row - fields[i + 1].row) > 1
                    or abs(fields[i].col - fields[i + 1].col) > 1
                ):
                    raise ValueError("Fields must be adjacent.")

            # If 3 fields were selected, make sure they are in one line
            # (direction vector between pairs is consistent)
            if len(fields) == 3:
                delta_row_1 = fields[1].row - fields[0].row
                delta_col_1 = fields[1].col - fields[0].col
                delta_row_2 = fields[2].row - fields[1].row
                delta_col_2 = fields[2].col - fields[1].col

                if (delta_row_1, delta_col_1) != (delta_row_2, delta_col_2):
                    raise ValueError(
                        "Fields must be aligned in one line "
                        "(horizontal, vertical, or diagonal)."
                    )

        tokens: list[Optional[Token]] = []
        for field in fields:
            tokens.append(field.token)
            field.token = None  # Remove the token after extracting it

        return tokens

    def display(self) -> None:
        print(
            f"\n--- Token Board ---\n{self.fields}"
        )


BOARD_REPLENISH_ORDER = [
    (3, 3),
    (4, 3),
    (4, 2),
    (3, 2),
    (2, 2),
    (2, 3),
    (2, 4),
    (3, 4),
    (4, 4),
    (5, 4),
    (5, 3),
    (5, 2),
    (5, 1),
    (4, 1),
    (3, 1),
    (2, 1),
    (1, 1),
    (1, 2),
    (1, 3),
    (1, 4),
    (1, 5),
    (2, 5),
    (3, 5),
    (4, 5),
    (5, 5),
]