from flask import Flask, request, jsonify
import random

app = Flask(__name__)

def parse_jumps(jumps, board_size):
    """Parse jumps into a dictionary mapping start to end positions."""
    jump_map = {}
    for jump in jumps:
        start, end = map(int, jump.split(':'))
        if end == 0:  # Smoke or Mirror
            jump_map[start] = end
        else:
            jump_map[start] = end
    return jump_map

def apply_jump(position, jump_map, die_roll, board_size):
    """Apply a jump (Snake, Ladder, Smoke, Mirror) from the current position."""
    if position in jump_map:
        target = jump_map[position]
        if target == 0:  # Smoke (move backward by next roll)
            next_roll = die_roll  # Use same roll for simplicity in simulation
            new_position = position - next_roll
            return max(1, new_position)  # Ensure not going before square 1
        elif target > 0 and jump_map[position] == position:  # Mirror (move forward by next roll)
            next_roll = die_roll  # Use same roll for simplicity
            new_position = position + next_roll
            return min(board_size, new_position)  # Ensure not going past board
        else:  # Snake or Ladder
            return jump_map[position]
    return position

def simulate_game(board_size, players, jumps, rolls):
    """Simulate the game with given rolls and return final positions and squares landed."""
    jump_map = parse_jumps(jumps, board_size)
    positions = [1] * players  # All players start at square 1
    squares_landed = set()  # Track unique squares landed for scoring
    roll_index = 0
    player = 0

    while roll_index < len(rolls):
        # Current player's turn
        current_position = positions[player]
        die_roll = rolls[roll_index]
        roll_index += 1

        # Move by die roll
        new_position = current_position + die_roll
        if new_position > board_size:
            overshoot = new_position - board_size
            new_position = board_size - overshoot
        new_position = max(1, min(board_size, new_position))

        # Add position to squares landed
        squares_landed.add(new_position)

        # Apply any jump (Snake, Ladder, Smoke, Mirror)
        next_position = apply_jump(new_position, jump_map, die_roll, board_size)
        if next_position != new_position:
            squares_landed.add(next_position)

        # Update player's position
        positions[player] = next_position

        # Check if current player has won
        if positions[player] == board_size:
            return positions, squares_landed, player, roll_index

        # Move to next player
        player = (player + 1) % players

    return positions, squares_landed, None, roll_index

def generate_rolls(board_size, players, jumps):
    """Generate die rolls to make the last player win with optimal score."""
    max_attempts = 1000  # Limit attempts to avoid infinite loops
    best_rolls = []
    best_score = 0
    target_winner = players - 1  # Last player

    for _ in range(max_attempts):
        rolls = []
        positions = [1] * players
        current_player = 0
        attempt_rolls = 0
        max_rolls = 100  # Prevent excessively long sequences

        while attempt_rolls < max_rolls:
            die_roll = random.randint(1, 6)
            rolls.append(die_roll)

            # Simulate one move
            current_position = positions[current_player]
            new_position = current_position + die_roll
            if new_position > board_size:
                overshoot = new_position - board_size
                new_position = board_size - overshoot
            new_position = max(1, min(board_size, new_position))

            # Apply jumps
            jump_map = parse_jumps(jumps, board_size)
            next_position = apply_jump(new_position, jump_map, die_roll, board_size)
            positions[current_player] = next_position

            # Check if any player has won
            if next_position == board_size:
                # Simulate full game to get score
                sim_positions, squares_landed, winner, _ = simulate_game(board_size, players, jumps, rolls)
                if winner == target_winner:
                    score = board_size / len(squares_landed) if squares_landed else 0
                    if score > best_score:
                        best_score = score
                        best_rolls = rolls.copy()
                break

            current_player = (current_player + 1) % players
            attempt_rolls += 1

    return best_rolls

@app.route('/slpu', methods=['POST'])
def slpu():
    """Handle POST request to /slpu endpoint."""
    data = request.get_json()
    board_size = data['boardSize']
    players = data['players']
    jumps = data['jumps']

    # Generate die rolls
    rolls = generate_rolls(board_size, players, jumps)

    # Format as SVG
    rolls_str = ''.join(map(str, rolls))
    svg = f'<svg xmlns="http://www.w3.org/2000/svg"><text>{rolls_str}</text></svg>'
    return svg, 200, {'Content-Type': 'image/svg+xml'}

@app.route('/')
def home():
    return "Snakes and Ladders Server is running. Use POST to /slsm to generate rolls."

if __name__ == '__main__':
    app.run(debug=True)