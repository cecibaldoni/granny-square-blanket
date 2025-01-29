# %% Import libraries


import matplotlib.pyplot as plt
import random
from itertools import combinations
from itertools import permutations

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

# %% Function for Visualisation
def visualize_pattern(pattern, title="Pattern"):
    """
    Visualize a pattern as a grid with diagonal squares.
    
    Parameters:
        pattern (list): 2D list of dictionaries representing squares.
        title (str): Title of the plot.
    """
    rows, cols = len(pattern), len(pattern[0])
    fig, ax = plt.subplots(figsize=(cols, rows))

    for r in range(rows):
        for c in range(cols):
            square = pattern[r][c]
            color1, color2 = colors[square["colors"][0]], colors[square["colors"][1]]
            orientation = square["orientation"]

            # Define coordinates
            x, y = c, rows - r - 1  # Flip y for better visualization

            # Draw diagonal based on orientation
            if orientation == "top-left to bottom-right":  # \
                ax.fill([x, x+1, x], [y, y+1, y+1], color=color1, alpha=0.7)
                ax.fill([x+1, x+1, x], [y+1, y, y], color=color2, alpha=0.7)
            else:  # top-right to bottom-left /
                ax.fill([x, x+1, x+1], [y, y, y+1], color=color1, alpha=0.7)
                ax.fill([x+1, x, x], [y+1, y+1, y], color=color2, alpha=0.7)

    ax.set_xlim(0, cols)
    ax.set_ylim(0, rows)
    ax.set_aspect('equal')
    ax.axis('off')
    plt.title(title)
    plt.show()

# %% Initial Code 
"""
Initial attempt to generate blanket patterns.
"""

# Function to generate random patterns (original version)
def generate_random_pattern(rows, cols):
    # Track usage of color combinations
    used_combinations = {comb: 0 for comb in color_combinations}
    pattern = []

    for r in range(rows):
        row = []
        for c in range(cols):
            # Select a random color combination
            valid_combinations = [
                comb for comb in color_combinations
                if used_combinations[comb] < max_squares_per_combination[comb]
            ]
            chosen_comb = random.choice(valid_combinations)
            used_combinations[chosen_comb] += 1

            # Assign a random orientation (initial version, incomplete)
            orientation = random.choice(["top-left to bottom-right", "top-right to bottom-left"])
            row.append({"colors": chosen_comb, "orientation": orientation})
        pattern.append(row)
    return pattern

# Generate and visualize a pattern
pattern_6x12 = generate_random_pattern(6, 12)
visualize_pattern(pattern_6x12, "Initial Pattern")


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
# def generate_pattern_with_rules(rows, cols):
#     # Track usage of color combinations
#     used_combinations = {comb: 0 for comb in color_combinations}
#     pattern = []

#     for r in range(rows):
#         row = []
#         for c in range(cols):
#             valid_combinations = [
#                 comb for comb in color_combinations
#                 if used_combinations[comb] < max_squares_per_combination[comb]
#             ]

#             # Apply adjacency rule
#             if r > 0:  # Check square above
#                 above_colors = pattern[r-1][c]["colors"]
#                 valid_combinations = [
#                     comb for comb in valid_combinations
#                     if above_colors[1] in comb
#                 ]
#             if c > 0:  # Check square to the left
#                 left_colors = row[c-1]["colors"]
#                 valid_combinations = [
#                     comb for comb in valid_combinations
#                     if left_colors[1] in comb
#                 ]

#             # Fallback if no valid combinations remain
#             if not valid_combinations:
#                 valid_combinations = [
#                     comb for comb in color_combinations
#                     if used_combinations[comb] < max_squares_per_combination[comb]
#                 ]

#             # Pick a valid combination
#             chosen_comb = random.choice(valid_combinations)
#             used_combinations[chosen_comb] += 1

#             # Alternate orientation
#             orientation = "top-left to bottom-right" if (r + c) % 2 == 0 else "top-right to bottom-left"

#             row.append({"colors": chosen_comb, "orientation": orientation})
#         pattern.append(row)

#     return pattern

# # Generate pattern with rules
# pattern_with_rules_6x12 = generate_pattern_with_rules(6, 12)
# pattern_with_rules_8x9 = generate_pattern_with_rules(8, 9)

# # Visualize the new patterns
# visualize_pattern(pattern_with_rules_6x12, "Rule-Based Pattern: 6x12")
# visualize_pattern(pattern_with_rules_8x9, "Rule-Based Pattern: 8x9")

# # %%
# def generate_flexible_pattern(rows, cols):
#     # Track usage of color combinations
#     used_combinations = {comb: 0 for comb in color_combinations}
#     pattern = []

#     for r in range(rows):
#         row = []
#         for c in range(cols):
#             # Filter valid combinations based on usage
#             valid_combinations = [
#                 comb for comb in color_combinations
#                 if used_combinations[comb] < max_squares_per_combination[comb]
#             ]

#             # Apply adjacency rule
#             if r > 0:  # Check square above
#                 above_colors = pattern[r-1][c]["colors"]
#                 valid_combinations = [
#                     comb for comb in valid_combinations
#                     if above_colors[1] in comb
#                 ]
#             if c > 0:  # Check square to the left
#                 left_colors = row[c-1]["colors"]
#                 valid_combinations = [
#                     comb for comb in valid_combinations
#                     if left_colors[1] in comb
#                 ]

#             # Add fallback for empty valid_combinations
#             if not valid_combinations:
#                 valid_combinations = color_combinations.copy()

#             # Add balancing: Favor underused combinations
#             if valid_combinations:
#                 valid_combinations.sort(key=lambda comb: used_combinations[comb])

#             # Pick the least-used valid combination
#             chosen_comb = valid_combinations[0]
#             used_combinations[chosen_comb] += 1

#             # Alternate orientation
#             orientation = "top-left to bottom-right" if (r + c) % 2 == 0 else "top-right to bottom-left"

#             row.append({"colors": chosen_comb, "orientation": orientation})
#         pattern.append(row)

#     return pattern, used_combinations


# # Fixed constraint
# pattern_fixed_6x12 = generate_random_pattern(6, 12)
# visualize_pattern(pattern_fixed_6x12, "Fixed: 6x12 Grid")

# # Flexible constraint
# pattern_flexible_6x12, usage_flexible_6x12 = generate_flexible_pattern(6, 12)
# visualize_pattern(pattern_flexible_6x12, "Flexible: 6x12 Grid")

# # Print usage statistics
# print("Flexible Usage Counts:")
# for comb, count in usage_flexible_6x12.items():
#     print(f"{comb}: {count}")

# %%
def check_yarn_feasibility(usage_counts):
    """
    Check if a pattern meets yarn feasibility constraints.
    -  Strictly feasible: All combinations ≤ 12 squares.
    -  Soft feasible: Some combinations exceed 12 squares but are ≤ 13 squares.
    -  Not feasible: At least one combination exceeds 13 squares.
    """
    strict = True  # If all are ≤ 12, the pattern is strictly feasible.
    soft = False  # If any is 13, the pattern is softly feasible.
    too_high = False  # If any is > 13, the pattern is not feasible.
    
    infeasible_combinations = []  # Store combinations that exceed limits
    soft_combinations = []  # Store combinations that are within 13 but exceed 12

    for comb, used in usage_counts.items():
        if used > 13:  # Completely infeasible
            too_high = True
            infeasible_combinations.append((comb, used))
        elif used > 12:  # ⚠️ Softly feasible
            soft = True
            soft_combinations.append((comb, used))
        # Feasible cases don't need extra tracking

    # Print results in a clear, grouped format
    if too_high:
        print("\nNo feasible patterns found!")
        for comb, used in infeasible_combinations:
            print(f" Not feasible: {comb} requires {used} squares, exceeding 13.")

    elif soft:
        print("\n This pattern is **softly feasible** (some combinations up to 13 squares)!")
        for comb, used in soft_combinations:
            print(f"⚠️ Soft feasible: {comb} requires {used} squares, exceeding 12 but within 13.")

    else:
        print("\nThis pattern is **strictly feasible** (all combinations ≤ 12 squares)!")

    return "strict" if strict else "soft" if soft else "not_feasible"
# %%
def flexible_pattern(rows, cols):
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


# Generate a flexible pattern
pattern_flexible_6x12, usage_flexible_6x12 = flexible_pattern(6, 12)
visualize_pattern(pattern_flexible_6x12, "Flexible Pattern: 6x12 Grid")


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
visualize_pattern(geometric_pattern_6x12, "Geometric Chevron Pattern: 6x12 Grid")
check_yarn_feasibility(usage_geometric_6x12)

# %%
# -------------------------------------------------------------------
# Orientation Troubleshooting:
# The diagonal orientations for squares (\ and /) were debugged in
# `orientation.py`. The issue has been resolved there, ensuring all
# four configurations work correctly.
# Below, I use the corrected orientations directly in the pattern generation.
# -------------------------------------------------------------------


# %%
# all_orientations = {
#     (color1, color2): [
#         {"orientation": "\\", "top": color1, "bottom": color2},
#         {"orientation": "\\", "top": color2, "bottom": color1},
#         {"orientation": "/", "top": color1, "bottom": color2},
#         {"orientation": "/", "top": color2, "bottom": color1}
#     ]
#     for color1, color2 in color_combinations
# }

# %%
def generate_random_pattern_fixed(rows, cols):
    pattern = []
    used_combinations = {comb: 0 for comb in color_combinations}

    for r in range(rows):
        row = []
        for c in range(cols):
            # Select a valid color combination
            valid_combinations = [
                comb for comb in color_combinations
                if used_combinations[comb] < max_squares_per_combination[comb]
            ]
            chosen_comb = random.choice(valid_combinations)
            used_combinations[chosen_comb] += 1

            # Explicitly define one of the four configurations
            orientation_choice = random.choice([
                "\\ Yellow-Top", "\\ Green-Top",
                "/ Yellow-Top", "/ Green-Top"
            ])
            if "Yellow" in orientation_choice:
                top_color, bottom_color = chosen_comb[0], chosen_comb[1]
            else:
                top_color, bottom_color = chosen_comb[1], chosen_comb[0]

            # Append square configuration
            row.append({
                "colors": chosen_comb,
                "orientation": orientation_choice,
                "top": top_color,
                "bottom": bottom_color
            })
        pattern.append(row)
    return pattern

# %%
def visualize_pattern_debug(pattern, title="Pattern"):
    rows, cols = len(pattern), len(pattern[0])
    fig, ax = plt.subplots(figsize=(cols, rows))
    print(f"Visualizing pattern with dimensions: {rows}x{cols}")

    for r in range(rows):
        for c in range(cols):
            square = pattern[r][c]
            color1 = colors[square["colors"][0]]
            color2 = colors[square["colors"][1]]
            orientation = square["orientation"]

            x, y = c, rows - r - 1  # Flip y for better visualization
            # print(f"Plotting square at ({r}, {c}): {square}")

            if orientation == "\\":
                ax.fill([x, x+1, x], [y, y+1, y+1], color=color1, alpha=0.7)
                ax.fill([x+1, x+1, x], [y+1, y, y], color=color2, alpha=0.7)
            else:  # Orientation is "/"
                ax.fill([x, x+1, x+1], [y+1, y, y+1], color=color1, alpha=0.7)
                ax.fill([x+1, x, x], [y, y+1, y], color=color2, alpha=0.7)

    ax.set_xlim(0, cols)
    ax.set_ylim(0, rows)
    ax.set_aspect("equal")
    ax.axis("off")
    plt.title(title)
    plt.show()

# %%
pattern_random_corrected = generate_random_pattern_fixed(6, 12)
visualize_pattern_debug(pattern_random_corrected, "Corrected Random Pattern")

# %%
def generate_chevron_pattern(rows, cols):
    print("Generating chevron pattern...")
    pattern = []
    used_combinations = {comb: 0 for comb in color_combinations}
    all_combinations = list(color_combinations)
    num_combinations = len(all_combinations)

    for r in range(rows):
        row = []
        for c in range(cols):
            # Rotate through all color combinations
            chosen_comb = all_combinations[(r + c) % num_combinations]

            # Determine orientation explicitly
            if r % 2 == 0:  # Even row
                orientation = "\\" if c % 2 == 0 else "/"
            else:  # Odd row
                orientation = "/" if c % 2 == 0 else "\\"

            # Explicitly assign top and bottom colors
            if orientation == "\\":
                if (r + c) % 2 == 0:
                    top_color, bottom_color = chosen_comb[0], chosen_comb[1]
                else:
                    top_color, bottom_color = chosen_comb[1], chosen_comb[0]
            else:  # Orientation is "/"
                if (r + c) % 2 == 0:
                    top_color, bottom_color = chosen_comb[0], chosen_comb[1]
                else:
                    top_color, bottom_color = chosen_comb[1], chosen_comb[0]

            # Add square to the row
            square = {"colors": (top_color, bottom_color), "orientation": orientation}
            print(f"Square at ({r}, {c}): {square}")
            row.append(square)
        pattern.append(row)

    print("Pattern generation complete!")
    return pattern


# %%
def count_yarn_usage(pattern):
    usage_counts = {comb: 0 for comb in color_combinations}
    for row in pattern:
        for square in row:
            comb = tuple(square["colors"])
            if comb in usage_counts:
                usage_counts[comb] += 1
            else: 
                usage_counts[comb[::-1]] += 1
    return usage_counts

# %%
# Generate and visualize a chevron pattern
pattern_chevron = generate_chevron_pattern(6, 12)
visualize_pattern_debug(pattern_chevron, "Chevron Pattern (Debug)")
# Check if enough yarn is available for chevron pattern
yarn_usage_chevron = count_yarn_usage(pattern_chevron)
check_yarn_feasibility(yarn_usage_chevron)


# %%
def generate_2x2_block_pattern(rows, cols, central_color="yellow"): # change central color!
    """
    Generate a corrected 2x2 grid pattern with consistent alignment of colors.
    """
    print(f"Generating corrected 2x2 block pattern with central color: {central_color}")
    if rows % 2 != 0 or cols % 2 != 0:
        raise ValueError("Rows and columns must be even for 2x2 block patterns.")

    pattern = []
    color_options = list(colors.keys())
    central_color_combinations = [
        comb for comb in color_combinations if central_color in comb
    ]

    for r in range(0, rows, 2):  # Step by 2 for 2x2 blocks
        row1, row2 = [], []
        for c in range(0, cols, 2):
            # Choose a color combination that includes the central color
            chosen_comb = central_color_combinations[(r + c) % len(central_color_combinations)]
            other_color = chosen_comb[1] if chosen_comb[0] == central_color else chosen_comb[0]

            # Determine block structure based on r and c
            if (r + c) % 4 == 0:
                block = [
                    {"colors": (central_color, other_color), "orientation": "\\"},  # Top-left
                    {"colors": (other_color, central_color), "orientation": "/"},  # Top-right
                    {"colors": (other_color, central_color), "orientation": "\\"},  # Bottom-left
                    {"colors": (central_color, other_color), "orientation": "/"},  # Bottom-right
                ]
            else:
                block = [
                    {"colors": (other_color, central_color), "orientation": "\\"},  # Top-left
                    {"colors": (central_color, other_color), "orientation": "/"},  # Top-right
                    {"colors": (central_color, other_color), "orientation": "\\"},  # Bottom-left
                    {"colors": (other_color, central_color), "orientation": "/"},  # Bottom-right
                ]

            # Append the block to the respective rows
            row1.extend(block[:2])  # Top row of the 2x2 block
            row2.extend(block[2:])  # Bottom row of the 2x2 block

        pattern.append(row1)
        pattern.append(row2)

    print("2x2 block pattern generation complete!")
    return pattern

# %%
# Generate and visualize the pattern
pattern_2x2 = generate_2x2_block_pattern(6, 12, central_color="yellow")
visualize_pattern_debug(pattern_2x2, "Corrected 2x2 Block Pattern with Yellow Center")
# Check yarn feasibility for 2x2 pattern
yarn_usage_2x2 = count_yarn_usage(pattern_2x2)
check_yarn_feasibility(yarn_usage_2x2)


# %% 
def generate_balanced_chevron_pattern(rows, cols):
    """
    Generate a chevron pattern where all six combinations are used evenly.
    """
    print("Generating balanced chevron pattern...")
    pattern = []
    used_combinations = {comb: 0 for comb in color_combinations}
    all_combinations = list(color_combinations)

    # Shuffle the combinations to randomize their order
    random.shuffle(all_combinations)
    num_combinations = len(all_combinations)

    for r in range(rows):
        row = []
        for c in range(cols):
            # Select a combination based on position, ensuring all are used
            chosen_comb = all_combinations[(r * cols + c) % num_combinations]

            # Determine orientation
            if r % 2 == 0:  # Even row
                orientation = "\\" if c % 2 == 0 else "/"
            else:  # Odd row
                orientation = "/" if c % 2 == 0 else "\\"

            # Assign top and bottom colors
            if orientation == "\\":
                top_color, bottom_color = chosen_comb[0], chosen_comb[1]
            else:  # Orientation is "/"
                top_color, bottom_color = chosen_comb[1], chosen_comb[0]

            # Add square to the row
            square = {"colors": (top_color, bottom_color), "orientation": orientation}
            used_combinations[chosen_comb] += 1
            row.append(square)

        pattern.append(row)

    print("Pattern generation complete!")
    return pattern, used_combinations

# %% 
# Generate and visualize the balanced chevron pattern
pattern_balanced_chevron, usage_balanced_chevron = generate_balanced_chevron_pattern(6, 12)
visualize_pattern_debug(pattern_balanced_chevron)
# Check yarn feasibility
check_yarn_feasibility(usage_balanced_chevron)


# %%
# Define color combinations (normalized)
normalized_color_combinations = list({tuple(sorted(pair)) for pair in combinations(colors, 2)})
print("Normalized color combinations:", normalized_color_combinations)

# Adjust yarn usage for normalized combinations
max_squares_per_combination = {
    tuple(sorted((color1, color2))): min(yarn_balls_per_color, yarn_balls_per_color) * squares_per_two_balls // 2
    for color1, color2 in normalized_color_combinations
}
def is_valid_sequence_touch(sequence, ordered=False):
    """
    Check if a sequence satisfies the "touch rule."
    - If `ordered=True`: The shared color must be in the correct position.
    - If `ordered=False`: Just ensures two adjacent combinations share a color.
    """
    for i in range(len(sequence) - 1):
        first, second = sequence[i], sequence[i + 1]
        if len(set(first) & set(second)) == 0:  # No shared color
            return False
        if ordered and first[1] != second[0]:  # If ordered, check correct positioning
            return False
    return True

valid_sequences = [
    seq for seq in permutations(normalized_color_combinations)
    if is_valid_sequence_touch(seq)
]
feasible_sequences = [
    seq for seq in valid_sequences
    if check_yarn_feasibility({comb: seq.count(comb) for comb in seq})
]

print(f"Valid sequences after applying touch rule: {len(valid_sequences)}")
print(f"Feasible sequences after applying yarn constraints: {len(feasible_sequences)}")


# %%
def generate_pattern_by_blocks(rows, cols, block_size=2):
    """
    Generate a pattern where color combinations are assigned to blocks.
    Ensures proper 2D list structure.
    """
    pattern = []
    usage_counts = {comb: 0 for comb in color_combinations}

    for r in range(0, rows, block_size):
        block_rows = [[] for _ in range(block_size)]  # Initialize block rows
        for c in range(0, cols, block_size):
            # Randomly assign a block of color combinations
            block_combinations = random.sample(color_combinations, block_size ** 2)
            block = []
            for i in range(block_size):
                block_row = []
                for j in range(block_size):
                    comb = block_combinations[i * block_size + j]
                    usage_counts[comb] += 1
                    if (r + i) % 2 == 0:
                        orientation = "\\" if (c + j) % 2 == 0 else "/"
                    else:
                        orientation = "/" if (c + j) % 2 == 0 else "\\"
                    block_row.append({"colors": comb, "orientation": orientation})
                block.append(block_row)
            
            # Append block rows correctly
            for i in range(block_size):
                block_rows[i].extend(block[i])

        pattern.extend(block_rows)  # Append block rows to the final pattern

    return pattern, usage_counts

# %%
# Set blanket dimensions
rows, cols = 6, 12

# Store feasible patterns
strict_feasible_patterns = []
soft_feasible_patterns = []

# Generate multiple patterns
for _ in range(10):  # Generate 10 patterns
    pattern, usage_counts = generate_pattern_by_blocks(rows, cols)
    feasibility = check_yarn_feasibility(usage_counts)

    if feasibility == "strict":
        strict_feasible_patterns.append((pattern, usage_counts))
    elif feasibility == "soft":
        soft_feasible_patterns.append((pattern, usage_counts))

# Visualize patterns that are **strictly feasible** (preferred)
if strict_feasible_patterns:
    print("\n🎯 Visualizing STRICTLY feasible patterns (12 squares max):")
    for idx, (pattern, usage_counts) in enumerate(strict_feasible_patterns):
        visualize_pattern(pattern, title=f"Strict Feasible Pattern {idx+1}")
else:
    print("\n⚠️ No strictly feasible patterns found. Trying SOFT feasibility...")

    if soft_feasible_patterns:
        print("\n🔄 Visualizing SOFT feasible patterns (some with 13 squares max):")
        for idx, (pattern, usage_counts) in enumerate(soft_feasible_patterns):
            visualize_pattern(pattern, title=f"Soft Feasible Pattern {idx+1}")
    else:
        print("\n🚨 No feasible patterns found, even with 13-square flexibility.")

###########################################################################
###########################################################################

# %%
sample_size = 6
sampled_sequences = random.sample(valid_sequences, min(sample_size, len(valid_sequences)))

print(f"Randomly sampled {len(sampled_sequences)} sequences:")
for idx, seq in enumerate(sampled_sequences, start=1):
    print(f"Sequence {idx}: {seq}")

# Function to generate a pattern for a sequence
def generate_pattern_from_sequence(sequence, rows, cols):
    pattern = []
    for r in range(rows):
        row = []
        for c in range(cols):
            comb = sequence[(r + c) % len(sequence)]  # Rotate through the sequence

            # Determine orientation explicitly
            if r % 2 == 0:  # Even row
                orientation = "\\" if c % 2 == 0 else "/"
            else:  # Odd row
                orientation = "/" if c % 2 == 0 else "\\"

            # Explicitly assign top and bottom colors
            if orientation == "\\":
                top_color, bottom_color = comb[0], comb[1]
            else:  # Orientation is "/"
                top_color, bottom_color = comb[1], comb[0]

            # Append the square to the row
            row.append({"colors": (top_color, bottom_color), "orientation": orientation})
        pattern.append(row)
    return pattern

def visualize_pattern(patterns, title="Pattern"):
    """
    Visualize one or multiple patterns.
    
    Parameters:
        patterns (list or dict): A list of patterns (for multiple patterns) or a single pattern (as a dict).
        title (str): Title for the plot(s).
    """
    # Check if it's a list of patterns or a single pattern
    if isinstance(patterns, list):  # Multiple patterns
        # Iterate through the list and visualize each pattern separately
        for idx, pattern in enumerate(patterns, start=1):
            visualize_single_pattern(pattern, title=f"Pattern {idx}")
    else:  # Single pattern
        visualize_single_pattern(patterns, title=title)


def visualize_single_pattern(pattern, title="Pattern"):
    """
    Visualize a single pattern.
    
    Parameters:
        pattern (list): 2D list of dictionaries representing squares.
        title (str): Title for the plot.
    """
    rows, cols = len(pattern), len(pattern[0])
    fig, ax = plt.subplots(figsize=(cols, rows))

    for r in range(rows):
        for c in range(cols):
            square = pattern[r][c]
            color1 = colors[square["colors"][0]]
            color2 = colors[square["colors"][1]]
            orientation = square["orientation"]

            x, y = c, rows - r - 1  # Flip y for better visualization

            # Draw triangles without overlapping
            if orientation == "\\":
                ax.fill([x, x+1, x], [y, y+1, y+1], color=color1, alpha=0.7)
                ax.fill([x+1, x+1, x], [y+1, y, y], color=color2, alpha=0.7)
            else:  # Orientation is "/"
                ax.fill([x, x+1, x+1], [y+1, y, y+1], color=color1, alpha=0.7)
                ax.fill([x+1, x, x], [y, y+1, y], color=color2, alpha=0.7)

    ax.set_xlim(0, cols)
    ax.set_ylim(0, rows)
    ax.set_aspect("equal")
    ax.axis("off")
    plt.title(title)
    plt.show()

# Generate patterns for sampled sequences
rows, cols = 6, 12  # Blanket dimensions
sampled_patterns = [generate_pattern_from_sequence(seq, rows, cols) for seq in sampled_sequences]

# Visualize all sampled patterns
visualize_pattern(sampled_patterns, title="Sampled Patterns")

# %% 
color_combinations = list(combinations(colors, 2))
balanced_sequence = [
    ('yellow', 'green'), ('blue', 'rose'), ('yellow', 'blue'), 
     ('green', 'rose'), ('yellow', 'rose'), ('green', 'blue'),
]

def generate_assigned_chevron_pattern(rows, cols, assigned_sequence):
    """
    Generate a chevron pattern with an assigned sequence of combinations.
    """
    print("Generating chevron pattern with an assigned sequence...")
    pattern = []
    used_combinations = {comb: 0 for comb in color_combinations}

    for r in range(rows):
        row = []
        for c in range(cols):
            # Use the assigned sequence to pick the combination
            chosen_comb = assigned_sequence[c % len(assigned_sequence)]

            # Determine orientation explicitly
            if r % 2 == 0:  # Even row
                orientation = "\\" if c % 2 == 0 else "/"
            else:  # Odd row
                orientation = "/" if c % 2 == 0 else "\\"

            # Assign top and bottom colors
            if orientation == "\\":
                top_color, bottom_color = chosen_comb[0], chosen_comb[1]
            else:  # Orientation is "/"
                top_color, bottom_color = chosen_comb[1], chosen_comb[0]

            # Add square to the row
            square = {"colors": (top_color, bottom_color), "orientation": orientation}
            used_combinations[chosen_comb] += 1
            row.append(square)

        pattern.append(row)

    print("Pattern generation complete!")
    return pattern, used_combinations

# Generate and visualize the assigned chevron pattern
pattern_assigned_chevron, usage_assigned_chevron = generate_assigned_chevron_pattern(6, 12, balanced_sequence)
visualize_pattern_debug(pattern_assigned_chevron, "Assigned Chevron Pattern")

# Check yarn feasibility
check_yarn_feasibility(usage_assigned_chevron)


# %%
