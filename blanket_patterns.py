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
# Function to filter dimensions
def valid_dimensions(total_squares):
    dimensions = []
    for rows in range(1, total_squares + 1):
        cols = total_squares // rows
        if rows * cols == total_squares:
            # Apply constraints: blanket should not be too narrow or too wide
            if 0.5 <= rows / cols <= 2:  # Ratio constraint: reasonable blanket shape
                dimensions.append((rows, cols))
    return dimensions

# Get valid dimensions
dimensions = valid_dimensions(total_squares)

print("Possible grid dimensions (rows x columns) with constraints:")
for dim in dimensions:
    print(f"{dim[0]} x {dim[1]}")



# %%
def apply_vertical_symmetry(pattern):
    rows = len(pattern)
    cols = len(pattern[0])
    symmetrical_pattern = []

    for row in pattern:
        # Mirror the left half to the right half
        left_half = row[:cols // 2]  # Take the first half
        mirrored_row = left_half + left_half[::-1]  # Mirror it
        symmetrical_pattern.append(mirrored_row[:cols])  # Truncate to original size

    return symmetrical_pattern

vertically_symmetric_6x12 = apply_vertical_symmetry(pattern_6x12)
visualize_pattern(vertically_symmetric_6x12, "Vertically Symmetric: 6x12")

# %%
def apply_horizontal_symmetry(pattern):
    rows = len(pattern)
    top_half = pattern[:rows // 2]  # Take the top half
    mirrored_pattern = top_half + top_half[::-1]  # Mirror it
    return mirrored_pattern[:rows]  # Truncate to original size

horizontally_symmetric_6x12 = apply_horizontal_symmetry(pattern_6x12)
visualize_pattern(horizontally_symmetric_6x12, "Horizontally Symmetric: 6x12")

# %%
def generate_pattern_with_rules(rows, cols):
    # Track usage of color combinations
    used_combinations = {comb: 0 for comb in color_combinations}
    pattern = []

    for r in range(rows):
        row = []
        for c in range(cols):
            valid_combinations = [
                comb for comb in color_combinations
                if used_combinations[comb] < max_squares_per_combination[comb]
            ]

            # Apply adjacency rule
            if r > 0:  # Check square above
                above_colors = pattern[r-1][c]["colors"]
                valid_combinations = [
                    comb for comb in valid_combinations
                    if above_colors[1] in comb
                ]
            if c > 0:  # Check square to the left
                left_colors = row[c-1]["colors"]
                valid_combinations = [
                    comb for comb in valid_combinations
                    if left_colors[1] in comb
                ]

            # Fallback if no valid combinations remain
            if not valid_combinations:
                valid_combinations = [
                    comb for comb in color_combinations
                    if used_combinations[comb] < max_squares_per_combination[comb]
                ]

            # Pick a valid combination
            chosen_comb = random.choice(valid_combinations)
            used_combinations[chosen_comb] += 1

            # Alternate orientation
            orientation = "top-left to bottom-right" if (r + c) % 2 == 0 else "top-right to bottom-left"

            row.append({"colors": chosen_comb, "orientation": orientation})
        pattern.append(row)

    return pattern

# Generate pattern with rules
pattern_with_rules_6x12 = generate_pattern_with_rules(6, 12)
pattern_with_rules_8x9 = generate_pattern_with_rules(8, 9)

# Visualize the new patterns
visualize_pattern(pattern_with_rules_6x12, "Rule-Based Pattern: 6x12")
visualize_pattern(pattern_with_rules_8x9, "Rule-Based Pattern: 8x9")

# %%
def generate_flexible_pattern(rows, cols):
    # Track usage of color combinations
    used_combinations = {comb: 0 for comb in color_combinations}
    pattern = []

    for r in range(rows):
        row = []
        for c in range(cols):
            # Filter valid combinations based on usage
            valid_combinations = [
                comb for comb in color_combinations
                if used_combinations[comb] < max_squares_per_combination[comb]
            ]

            # Apply adjacency rule
            if r > 0:  # Check square above
                above_colors = pattern[r-1][c]["colors"]
                valid_combinations = [
                    comb for comb in valid_combinations
                    if above_colors[1] in comb
                ]
            if c > 0:  # Check square to the left
                left_colors = row[c-1]["colors"]
                valid_combinations = [
                    comb for comb in valid_combinations
                    if left_colors[1] in comb
                ]

            # Add fallback for empty valid_combinations
            if not valid_combinations:
                valid_combinations = color_combinations.copy()

            # Add balancing: Favor underused combinations
            if valid_combinations:
                valid_combinations.sort(key=lambda comb: used_combinations[comb])

            # Pick the least-used valid combination
            chosen_comb = valid_combinations[0]
            used_combinations[chosen_comb] += 1

            # Alternate orientation
            orientation = "top-left to bottom-right" if (r + c) % 2 == 0 else "top-right to bottom-left"

            row.append({"colors": chosen_comb, "orientation": orientation})
        pattern.append(row)

    return pattern, used_combinations


# Fixed constraint
pattern_fixed_6x12 = generate_random_pattern(6, 12)
visualize_pattern(pattern_fixed_6x12, "Fixed: 6x12 Grid")

# Flexible constraint
pattern_flexible_6x12, usage_flexible_6x12 = generate_flexible_pattern(6, 12)
visualize_pattern(pattern_flexible_6x12, "Flexible: 6x12 Grid")

# Print usage statistics
print("Flexible Usage Counts:")
for comb, count in usage_flexible_6x12.items():
    print(f"{comb}: {count}")

# %%
def check_yarn_feasibility(usage_counts):
    feasible = True
    for comb, used in usage_counts.items():
        if used > max_squares_per_combination[comb]:
            print(f"Not feasible: {comb} requires {used} squares, but only {max_squares_per_combination[comb]} can be made.")
            feasible = False
    if feasible:
        print("All combinations are feasible with the available yarn!")
    return feasible

# After generating the flexible pattern
check_yarn_feasibility(usage_flexible_6x12)

# %%

def new_flexible_pattern(rows, cols):
    # Track usage of color combinations
    used_combinations = {comb: 0 for comb in color_combinations}
    pattern = []

    for r in range(rows):
        row = []
        for c in range(cols):
            # Apply adjacency rule
            valid_combinations = color_combinations.copy()
            if r > 0:  # Check square above
                above_colors = pattern[r-1][c]["colors"]
                valid_combinations = [
                    comb for comb in valid_combinations
                    if above_colors[1] in comb
                ]
            if c > 0:  # Check square to the left
                left_colors = row[c-1]["colors"]
                valid_combinations = [
                    comb for comb in valid_combinations
                    if left_colors[1] in comb
                ]

            # Add balancing: Favor underused combinations
            if valid_combinations:
                valid_combinations.sort(key=lambda comb: used_combinations[comb])

            # Pick the least-used valid combination
            chosen_comb = random.choice(valid_combinations)
            used_combinations[chosen_comb] += 1

            # Alternate orientation
            orientation = "top-left to bottom-right" if (r + c) % 2 == 0 else "top-right to bottom-left"

            row.append({"colors": chosen_comb, "orientation": orientation})
        pattern.append(row)

    return pattern, used_combinations

def yarn_feasibility(usage_counts):
    feasible = True
    leftover_yarn = {comb: 0 for comb in max_squares_per_combination.keys()}
    for comb, used in usage_counts.items():
        max_possible = max_squares_per_combination[comb]
        if used > max_possible:
            print(f"Not feasible: {comb} requires {used} squares, but only {max_possible} squares can be made.")
            feasible = False
        else:
            leftover_yarn[comb] = max_possible - used
    if feasible:
        print("All combinations are feasible with the available yarn!")
    else:
        print("Adjustments needed due to yarn constraints.")
    print("Leftover yarn availability per combination:")
    for comb, leftover in leftover_yarn.items():
        print(f"{comb}: {leftover} squares left")
    return feasible

# Generate a flexible pattern
pattern_flexible_6x12, usage_flexible_6x12 = new_flexible_pattern(6, 12)

# Visualize the pattern
visualize_pattern(pattern_flexible_6x12, "Flexible Pattern: 6x12 Grid")

# Check yarn feasibility
yarn_feasibility(usage_flexible_6x12)

# %%
def generate_geometric_pattern(rows, cols):
    pattern = []
    used_combinations = {comb: 0 for comb in color_combinations}
    all_combinations = list(color_combinations)  # Ensure we loop through all combinations
    num_combinations = len(all_combinations)

    for r in range(rows):
        row = []
        for c in range(cols):
            # Rotate through all combinations based on row and column
            chosen_comb = all_combinations[(r + c) % num_combinations]

            # Count usage
            used_combinations[chosen_comb] += 1

            # Alternate orientation
            orientation = "top-left to bottom-right" if (r + c) % 2 == 0 else "top-right to bottom-left"

            row.append({"colors": chosen_comb, "orientation": orientation})
        pattern.append(row)

    return pattern, used_combinations


# %%
# Generate geometric pattern
geometric_pattern_6x12, usage_geometric_6x12 = generate_geometric_pattern(6, 12)

# Visualize
visualize_pattern(geometric_pattern_6x12, "Geometric Chevron Pattern: 6x12 Grid")

# Check yarn feasibility
check_yarn_feasibility(usage_geometric_6x12)

# %%
def generate_true_diamond_pattern(rows, cols):
    pattern = []
    used_combinations = {comb: 0 for comb in color_combinations}
    all_combinations = list(color_combinations)
    num_combinations = len(all_combinations)

    # Define the center of the grid
    center_row, center_col = rows // 2, cols // 2

    for r in range(rows):
        row = []
        for c in range(cols):
            # Calculate distance from the center for the diamond layer
            distance = abs(center_row - r) + abs(center_col - c)

            # Choose a color combination for the current layer
            chosen_comb = all_combinations[distance % num_combinations]
            used_combinations[chosen_comb] += 1

            # Determine the square's orientation based on position
            if r <= center_row:  # Top half
                orientation = "top-left to bottom-right" if c <= center_col else "top-right to bottom-left"
            else:  # Bottom half
                orientation = "top-right to bottom-left" if c <= center_col else "top-left to bottom-right"

            row.append({"colors": chosen_comb, "orientation": orientation})
        pattern.append(row)

    return pattern, used_combinations


# %%
# Generate a true diamond pattern
true_diamond_pattern_6x12, usage_true_diamond_6x12 = generate_true_diamond_pattern(6, 12)

# Visualize
visualize_pattern(true_diamond_pattern_6x12, "Diamond Pattern: 6x12 Grid")

# Check yarn feasibility
check_yarn_feasibility(usage_true_diamond_6x12)

# %% 

def generate_corrected_diamond_pattern(rows, cols):
    # Ensure rows and cols are multiples of 2
    if rows % 2 != 0 or cols % 2 != 0:
        raise ValueError("Rows and columns must be even to create 2x2 blocks.")

    # Initialize the grid and color combinations
    pattern = [[None for _ in range(cols)] for _ in range(rows)]
    all_combinations = list(color_combinations)
    num_combinations = len(all_combinations)

    print("Generating corrected diamond pattern...")
    print(f"Grid dimensions: {rows}x{cols}")
    print(f"Available color combinations: {all_combinations}")

    # Fill the grid block by block
    for block_row in range(0, rows, 2):  # Step by 2 for blocks
        for block_col in range(0, cols, 2):  # Step by 2 for blocks
            # Choose a color combination for this block
            chosen_comb = all_combinations[(block_row + block_col) // 2 % num_combinations]

            print(f"\nProcessing 2x2 block at ({block_row}, {block_col}) with color combination {chosen_comb}:")

            # Assign the 2x2 block's colors and orientations to form a diamond
            # Top-left square (\ orientation, dominant color on top-left)
            pattern[block_row][block_col] = {"colors": chosen_comb, "orientation": "top-left to bottom-right"}
            print(f"  Top-left square: {pattern[block_row][block_col]}")

            # Top-right square (/ orientation, complementary color on top-right)
            pattern[block_row][block_col + 1] = {"colors": chosen_comb, "orientation": "top-right to bottom-left"}
            print(f"  Top-right square: {pattern[block_row][block_col + 1]}")

            # Bottom-left square (/ orientation, complementary color on bottom-left)
            pattern[block_row + 1][block_col] = {"colors": chosen_comb, "orientation": "top-right to bottom-left"}
            print(f"  Bottom-left square: {pattern[block_row + 1][block_col]}")

            # Bottom-right square (\ orientation, dominant color on bottom-right)
            pattern[block_row + 1][block_col + 1] = {"colors": chosen_comb, "orientation": "top-left to bottom-right"}
            print(f"  Bottom-right square: {pattern[block_row + 1][block_col + 1]}")

    print("\nPattern generation complete!")
    return pattern


# %%
def visualize_pattern_with_debug(pattern, title="Pattern"):
    rows, cols = len(pattern), len(pattern[0])
    fig, ax = plt.subplots(figsize=(cols, rows))

    for r in range(rows):
        for c in range(cols):
            square = pattern[r][c]
            color1, color2 = colors[square["colors"][0]], colors[square["colors"][1]]
            orientation = square["orientation"]

            # Define coordinates
            x, y = c, rows - r - 1  # Flip y for better visualization

            # Corrected diagonal logic
            if orientation == "top-left to bottom-right":  # Expecting \
                ax.fill([x, x+1, x+1], [y, y, y+1], color=color1, alpha=0.7)  # Corrected logic
                ax.fill([x+1, x, x], [y+1, y+1, y], color=color2, alpha=0.7)  # Corrected logic
            else:  # "top-right to bottom-left" Expecting /
                ax.fill([x, x+1, x], [y, y+1, y+1], color=color1, alpha=0.7)  # Corrected logic
                ax.fill([x+1, x+1, x], [y+1, y, y], color=color2, alpha=0.7)  # Corrected logic

            # Add debugging text for orientation
            ax.text(
                x + 0.5,
                y + 0.5,
                f"{orientation}",
                ha="center",
                va="center",
                fontsize=6,
                color="black",
            )

    ax.set_xlim(0, cols)
    ax.set_ylim(0, rows)
    ax.set_aspect('equal')
    ax.axis('off')
    plt.title(title)
    plt.show()


# %%
# Generate the corrected pattern with debugging
corrected_pattern = generate_corrected_diamond_pattern(6, 12)

# Visualize the corrected grid with debugging overlays
visualize_pattern_with_debug(corrected_pattern, "Corrected Diamond Pattern with Fixed Visualization")

