import main
from unittest.mock import Mock

# Test with a larger SVG board (16x16 = 256 squares)
svg_content_large = '''<svg viewBox="0 0 512 512" xmlns="http://www.w3.org/2000/svg">
  <rect width="100%" height="100%" fill="#f0f0f0" />
  <line x1="224" y1="32" x2="192" y2="64" stroke="BLUE" />
  <line x1="96" y1="64" x2="64" y2="96" stroke="RED" />
</svg>'''

# Mock the request object
mock_request = Mock()
mock_request.data.decode.return_value = svg_content_large

# Temporarily replace the request in the module
original_request = main.request
main.request = mock_request

try:
    # Test the slpu function
    response_data, status_code, headers = main.slpu()
    
    print(f"Status Code: {status_code}")
    print(f"Content-Type: {headers.get('Content-Type')}")
    
    # Extract rolls from response
    import re
    text_match = re.search(r'<text>(.*?)</text>', response_data)
    if text_match:
        rolls_str = text_match.group(1)
        rolls = [int(r) for r in rolls_str]
        print(f"✓ Generated {len(rolls)} rolls for larger board")
        
        # Test that rolls are valid (1-6)
        if all(1 <= r <= 6 for r in rolls):
            print("✓ All rolls are valid (1-6)")
        else:
            print("✗ Some rolls are invalid")
            
        # Test the game simulation
        board_data = main.parse_svg_board(svg_content_large)
        print(f"✓ Board size: {board_data['board_size']}")
        
        sim_positions, squares_landed, winner, _ = main.simulate_game(
            board_data['board_size'], 2, board_data['jumps'], rolls
        )
        
        print(f"✓ Winner: Player {winner}")
        print(f"✓ Squares landed: {len(squares_landed)}")
        print(f"✓ Coverage: {len(squares_landed) / board_data['board_size']:.2%}")
        
        if winner == 1:  # Last player (0-indexed)
            print("✓ Last player won as expected")
        else:
            print("✗ Last player did not win")
            
    else:
        print("✗ Could not extract rolls from response")

finally:
    # Restore original request
    main.request = original_request
