import main
from unittest.mock import Mock

print("=== Snakes & Ladders Power Up! - Final Validation ===\n")

# Test SVG matching the challenge format
svg_content = '''<svg viewBox="0 0 512 512" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="end" viewBox="0 0 8 8" refX="4" refY="4" markerWidth="4" markerHeight="4" orient="auto-start-reverse">
      <path d="M 0 0 L 8 4 L 0 8" />
    </marker>
  </defs>
  <rect width="100%" height="100%" fill="#f9f9f9" />
  <line x1="224" y1="480" x2="192" y2="448" stroke="BLUE" marker-end="url(#end)" />
  <line x1="96" y1="448" x2="64" y2="416" stroke="RED" marker-end="url(#end)" />
</svg>'''

# Mock the request
mock_request = Mock()
mock_request.data.decode.return_value = svg_content
original_request = main.request
main.request = mock_request

try:
    # Test the endpoint
    response_data, status_code, headers = main.slpu()
    
    # Parse the board
    board_data = main.parse_svg_board(svg_content)
    print(f"✓ Board parsed: {board_data['board_size']} squares, {len(board_data['jumps'])} jumps")
    
    # Extract rolls
    import re
    text_match = re.search(r'<text>(.*?)</text>', response_data)
    rolls = [int(r) for r in text_match.group(1)]
    
    # Simulate the game
    sim_positions, squares_landed, winner, _ = main.simulate_game(
        board_data['board_size'], 2, board_data['jumps'], rolls
    )
    
    # Calculate coverage
    coverage = len(squares_landed) / board_data['board_size']
    
    print(f"✓ Generated {len(rolls)} die rolls")
    print(f"✓ Winner: Player {winner} (last player = Player 1)")
    print(f"✓ Coverage: {coverage:.1%} ({len(squares_landed)}/{board_data['board_size']} squares)")
    
    # Validate requirements
    checks = [
        ("Response is SVG format", response_data.startswith('<svg') and 'text' in response_data),
        ("Content-Type is image/svg+xml", headers.get('Content-Type') == 'image/svg+xml'),
        ("All rolls are 1-6", all(1 <= r <= 6 for r in rolls)),
        ("Last player wins", winner == 1),
        ("Coverage > 25%", coverage > 0.25),
        ("Board size is valid", 16 <= board_data['board_size'] <= 32*32),
    ]
    
    print("\nValidation Results:")
    all_passed = True
    for check_name, passed in checks:
        status = "✓" if passed else "✗"
        print(f"{status} {check_name}")
        if not passed:
            all_passed = False
    
    print(f"\n{'🎉 All checks passed! Ready for challenge submission.' if all_passed else '❌ Some checks failed. Please review.'}")
    
    # Calculate potential score
    if coverage <= 0.25:
        sub_score = 25
    else:
        sub_score = int(25 * (1 - coverage))
    
    print(f"\nPotential sub-score for this round: {sub_score}/100")

finally:
    main.request = original_request
