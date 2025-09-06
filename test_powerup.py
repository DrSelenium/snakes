import main

# Test power-up mechanics with a simple scenario
rolls = [6, 1, 6, 1]  # Should power up, then revert, power up again, then revert
board_size = 100
jumps = []

positions, squares_landed, winner, roll_count = main.simulate_game(board_size, 2, jumps, rolls)

print("Power-up mechanics test:")
print(f"Rolls: {rolls}")
print(f"Final positions: {positions}")
print(f"Squares landed: {len(squares_landed)}")

# The mechanics should work as follows:
# Player 1: roll 6 (regular) -> power up, move 6
# Player 2: roll 1 (regular) -> move 1
# Player 1: roll 6 (power) -> move 64, still power
# Player 2: roll 1 (regular) -> move 1
# Player 1: roll 1 (power) -> move 2, revert to regular

print("✓ Power-up mechanics test completed")
