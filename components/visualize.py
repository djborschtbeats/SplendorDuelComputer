import matplotlib.colors as mcolors
import matplotlib.patches as patches
import matplotlib.pyplot as plt

from token_board import TokenBoard


def visualize_token_board(token_board: TokenBoard) -> None:
    # Plot a color grid representing the board fields (2d list) and their tokens.
    # Convert each token's hex color to the corresponding RGB tuple
    # expected by matplotlib. Fill in fields without a token as gray.
    color_grid: list[list[tuple[float, float, float]]] = [
        [
            _hex_to_rgb(getattr(getattr(field, "token", None), "value", "#808080"))
            for field in row
        ]
        for row in token_board.fields
    ]

    fig, ax = plt.subplots(figsize=(5, 5))
    ax.imshow(color_grid, aspect="equal")

    # Add field borders
    for x in range(5):
        for y in range(5):
            ax.add_patch(
                patches.Rectangle(
                    (y - 0.5, x - 0.5),
                    1,
                    1,
                    linewidth=1,
                    edgecolor="black",
                    facecolor="none",
                )
            )

    ax.set_xticks(range(5))
    ax.set_yticks(range(5))
    ax.set_xticklabels(range(1, 6))
    ax.set_yticklabels(range(1, 6))
    ax.set_title("Token Board")
    plt.show()


def _hex_to_rgb(hex_color: str) -> tuple[float, float, float]:
    return mcolors.hex2color(hex_color)
