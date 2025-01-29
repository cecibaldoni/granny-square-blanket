# %% Import necessary libraries
import matplotlib.pyplot as plt
import random
from itertools import combinations

# %% Define parameters
colors = {
    "yellow": "#ffe45e",
    "green": "#c1fba4",
    "blue": "#8093f1",
    "rose": "#ffd6e0",
}
color_combinations = list(combinations(colors, 2))
square = {
    "colors": ("yellow", "green"),  # Two colors
    "orientation": "top-left to bottom-right"  # Orientation
}
yarn_balls_per_color = 4
squares_per_two_balls = 6
# Total number of squares
total_squares = 6 * 12  # 6 combinations, 12 squares each

# Calculate the maximum number of squares per combination
max_squares_per_combination = {
    (color1, color2): min(yarn_balls_per_color, yarn_balls_per_color) * squares_per_two_balls // 2
    for color1, color2 in color_combinations
}

print("Max squares feasible per combination:")
for comb, max_squares in max_squares_per_combination.items():
    print(f"{comb}: {max_squares} squares")


print("Color combinations:", color_combinations)
print("Example square:", square)


# %%
def visualize_pattern_with_full_orientations(pattern, title="Pattern"):
    rows, cols = len(pattern), len(pattern[0])
    fig, ax = plt.subplots(figsize=(cols, rows))

    for r in range(rows):
        for c in range(cols):
            square = pattern[r][c]
            color1, color2 = colors[square["colors"][0]], colors[square["colors"][1]]
            orientation = square["orientation"]
            order = square["order"]

            # Define coordinates
            x, y = c, rows - r - 1  # Flip y for better visualization

            # Draw based on orientation and color order
            if orientation == "top-left to bottom-right":  # \
                if order == "yellow-top":
                    # Yellow is top-left, green is bottom-right
                    ax.fill([x, x+1, x], [y, y+1, y+1], color=color1, alpha=0.7)
                    ax.fill([x+1, x+1, x], [y+1, y, y], color=color2, alpha=0.7)
                else:  # green-top
                    # Green is top-left, yellow is bottom-right
                    ax.fill([x, x+1, x], [y, y+1, y+1], color=color2, alpha=0.7)
                    ax.fill([x+1, x+1, x], [y+1, y, y], color=color1, alpha=0.7)
            else:  # top-right to bottom-left /
                if order == "yellow-top":
                    # Yellow is top-right, green is bottom-left
                    ax.fill([x, x+1, x+1], [y, y, y+1], color=color1, alpha=0.7)
                    ax.fill([x+1, x, x], [y+1, y+1, y], color=color2, alpha=0.7)
                else:  # green-top
                    # Green is top-right, yellow is bottom-left
                    ax.fill([x, x+1, x+1], [y, y, y+1], color=color2, alpha=0.7)
                    ax.fill([x+1, x, x], [y+1, y+1, y], color=color1, alpha=0.7)

            # Add debugging text
            ax.text(x + 0.5, y + 0.5, f"{orientation}\n{order}", ha="center", va="center", fontsize=6, color="black")

    ax.set_xlim(0, cols)
    ax.set_ylim(0, rows)
    ax.set_aspect('equal')
    ax.axis('off')
    plt.title(title)
    plt.show()
# Testing four squares with all possible diagonal orientations
test_pattern = [
    [
        {"colors": ("yellow", "green"), "orientation": "top-left to bottom-right", "order": "yellow-top"},
        {"colors": ("yellow", "green"), "orientation": "top-left to bottom-right", "order": "green-top"},
    ],
    [
        {"colors": ("yellow", "green"), "orientation": "top-right to bottom-left", "order": "yellow-top"},
        {"colors": ("yellow", "green"), "orientation": "top-right to bottom-left", "order": "green-top"},
    ]
]

# Visualize the test pattern
visualize_pattern_with_full_orientations(test_pattern, "Test: Four Orientations")


# %%
def visualize_two_orientations():
    fig, ax = plt.subplots(figsize=(4, 2))

    # Define coordinates for the first square (orientation: \)
    x1, y1 = 0, 1  # Bottom-left corner
    ax.fill([x1, x1+1, x1], [y1, y1, y1+1], color="yellow", alpha=0.7)  # Top-left triangle
    ax.fill([x1+1, x1+1, x1], [y1+1, y1, y1], color="green", alpha=0.7)  # Bottom-right triangle

    # Define coordinates for the second square (orientation: /)
    x2, y2 = 2, 1  # Bottom-left corner of second square
    ax.fill([x2, x2+1, x2+1], [y2, y2, y2+1], color="yellow", alpha=0.7)  # Top-right triangle
    ax.fill([x2+1, x2, x2], [y2+1, y2+1, y2], color="green", alpha=0.7)  # Bottom-left triangle

    # Add labels to identify orientations
    ax.text(0.5, 1.5, "\\", ha="center", va="center", fontsize=16, color="black")
    ax.text(2.5, 1.5, "/", ha="center", va="center", fontsize=16, color="black")

    ax.set_xlim(0, 4)
    ax.set_ylim(0, 2)
    ax.set_aspect('equal')
    ax.axis('off')
    plt.title("Test: Two Diagonal Orientations")
    plt.show()

# Run the test visualization
visualize_two_orientations()

# %%

def visualize_four_configurations():
    fig, ax = plt.subplots(figsize=(6, 3))

    # First square: \ (Yellow top-left, Green bottom-right)
    x1, y1 = 0, 1
    ax.fill([x1, x1+1, x1], [y1, y1, y1+1], color="yellow", alpha=0.7)  # Top-left triangle
    ax.fill([x1+1, x1+1, x1], [y1+1, y1, y1], color="green", alpha=0.7)  # Bottom-right triangle (fixed)

    # Second square: \ (Green top-left, Yellow bottom-right)
    x2, y2 = 2, 1
    ax.fill([x2, x2+1, x2], [y2, y2, y2+1], color="green", alpha=0.7)  # Top-left triangle
    ax.fill([x2+1, x2+1, x2], [y2+1, y2, y2], color="yellow", alpha=0.7)  # Bottom-right triangle

    # Third square: / (Yellow top-right, Green bottom-left)
    x3, y3 = 4, 1
    ax.fill([x3, x3+1, x3+1], [y3, y3, y3+1], color="yellow", alpha=0.7)  # Top-right triangle
    ax.fill([x3, x3, x3+1], [y3+1, y3, y3+1], color="green", alpha=0.7)  # Bottom-left triangle

    # Fourth square: / (Green top-right, Yellow bottom-left)
    x4, y4 = 6, 1
    ax.fill([x4, x4+1, x4+1], [y4, y4, y4+1], color="green", alpha=0.7)  # Top-right triangle
    ax.fill([x4, x4, x4+1], [y4+1, y4, y4+1], color="yellow", alpha=0.7)  # Bottom-left triangle

    # Add labels to identify configurations
    ax.text(0.5, 1.5, "\\ Yellow Top", ha="center", va="center", fontsize=8, color="black")
    ax.text(2.5, 1.5, "\\ Green Top", ha="center", va="center", fontsize=8, color="black")
    ax.text(4.5, 1.5, "/ Yellow Top", ha="center", va="center", fontsize=8, color="black")
    ax.text(6.5, 1.5, "/ Green Top", ha="center", va="center", fontsize=8, color="black")

    ax.set_xlim(0, 8)
    ax.set_ylim(0, 2)
    ax.set_aspect('equal')
    ax.axis('off')
    plt.title("Test: Four Configurations")
    plt.show()

# Run the test
visualize_four_configurations()

# %%
def debug_triangle_edges():
    fig, ax = plt.subplots(figsize=(4, 2))

    # Square 1: \ diagonal
    x1, y1 = 0, 0  # Bottom-left corner
    # Top-left triangle (Black)
    ax.plot([x1, x1+1, x1, x1], [y1, y1, y1+1, y1], color="black", linewidth=2, label="\\ Top-left")
    # Bottom-right triangle (Red - Corrected)
    ax.plot([x1+1, x1, x1+1, x1+1], [y1+1, y1+1, y1, y1+1], color="red", linewidth=2, label="\\ Bottom-right")
    ax.text(x1+0.5, y1+0.5, "\\ diagonal", ha="center", va="center", fontsize=10)

    # Square 2: / diagonal
    x2, y2 = 2, 0  # Bottom-left corner
    # Bottom-left triangle (Blue)
    ax.plot([x2, x2, x2+1, x2], [y2+1, y2, y2+1, y2+1], color="blue", linewidth=2, label="/ Bottom-left")
    # Top-right triangle (Green)
    ax.plot([x2, x2+1, x2+1, x2], [y2, y2, y2+1, y2], color="green", linewidth=2, label="/ Top-right")
    ax.text(x2+0.5, y2+0.5, "/ diagonal", ha="center", va="center", fontsize=10)

    # Set limits and aspect
    ax.set_xlim(0, 4)
    ax.set_ylim(0, 2)
    ax.set_aspect('equal')
    ax.axis('off')
    plt.title("Corrected Triangle Edges for \\ and /")
    plt.legend()
    plt.show()

# Run the corrected debug test
debug_triangle_edges()

# %%
def test_diagonal_orientations_with_colors():
    fig, ax = plt.subplots(figsize=(4, 2))

    # Square 1: \ diagonal (Yellow top-left, Green bottom-right)
    x1, y1 = 0, 0
    ax.fill([x1, x1+1, x1], [y1, y1, y1+1], color="yellow", alpha=0.7)  # Top-left triangle
    ax.fill([x1+1, x1, x1+1], [y1+1, y1+1, y1], color="green", alpha=0.7)  # Bottom-right triangle
    ax.text(x1+0.5, y1+0.5, "\\ diagonal", ha="center", va="center", fontsize=10, color="black")

    # Square 2: / diagonal (Green top-right, Yellow bottom-left)
    x2, y2 = 2, 0
    ax.fill([x2, x2, x2+1], [y2+1, y2, y2+1], color="yellow", alpha=0.7)  # Bottom-left triangle
    ax.fill([x2, x2+1, x2+1], [y2, y2, y2+1], color="green", alpha=0.7)  # Top-right triangle
    ax.text(x2+0.5, y2+0.5, "/ diagonal", ha="center", va="center", fontsize=10, color="black")

    # Set limits and aspect
    ax.set_xlim(0, 4)
    ax.set_ylim(0, 2)
    ax.set_aspect('equal')
    ax.axis('off')
    plt.title("Test: Colored Triangles for \\ and / Diagonal Orientations")
    plt.show()

# Run the test
test_diagonal_orientations_with_colors()

# %%
def test_four_configurations():
    fig, ax = plt.subplots(figsize=(6, 2))

    # Configuration 1: \ diagonal (Yellow-Top)
    x1, y1 = 0, 0
    ax.fill([x1, x1+1, x1], [y1, y1, y1+1], color="yellow", alpha=0.7)  # Top-left triangle
    ax.fill([x1+1, x1, x1+1], [y1+1, y1+1, y1], color="green", alpha=0.7)  # Bottom-right triangle
    ax.text(x1+0.5, y1+0.5, "\\ Yellow-Top", ha="center", va="center", fontsize=8)

    # Configuration 2: \ diagonal (Green-Top)
    x2, y2 = 2, 0
    ax.fill([x2, x2+1, x2], [y2, y2, y2+1], color="green", alpha=0.7)  # Top-left triangle
    ax.fill([x2+1, x2, x2+1], [y2+1, y2+1, y2], color="yellow", alpha=0.7)  # Bottom-right triangle
    ax.text(x2+0.5, y2+0.5, "\\ Green-Top", ha="center", va="center", fontsize=8)

    # Configuration 3: / diagonal (Yellow-Top)
    x3, y3 = 4, 0
    ax.fill([x3, x3, x3+1], [y3+1, y3, y3+1], color="yellow", alpha=0.7)  # Bottom-left triangle
    ax.fill([x3, x3+1, x3+1], [y3, y3, y3+1], color="green", alpha=0.7)  # Top-right triangle
    ax.text(x3+0.5, y3+0.5, "/ Yellow-Top", ha="center", va="center", fontsize=8)

    # Configuration 4: / diagonal (Green-Top)
    x4, y4 = 6, 0
    ax.fill([x4, x4, x4+1], [y4+1, y4, y4+1], color="green", alpha=0.7)  # Bottom-left triangle
    ax.fill([x4, x4+1, x4+1], [y4, y4, y4+1], color="yellow", alpha=0.7)  # Top-right triangle
    ax.text(x4+0.5, y4+0.5, "/ Green-Top", ha="center", va="center", fontsize=8)

    # Set limits and aspect
    ax.set_xlim(0, 8)
    ax.set_ylim(0, 2)
    ax.set_aspect('equal')
    ax.axis('off')
    plt.title("Test: Four Configurations (Two Colors, Two Diagonals)")
    plt.show()

# Run the test
test_four_configurations()
