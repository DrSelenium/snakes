import main
from unittest.mock import Mock

# Test SVG content (same as before)
svg_content = '''<svg viewBox="0 0 512 512" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="end" viewBox="0 0 8 8" refX="4" refY="4" markerWidth="4" markerHeight="4" orient="auto-start-reverse">
      <path d="M 0 0 L 8 4 L 0 8" />
    </marker>
    <pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse">
      <path d="M 0 0 L 32 0 32 32 0 32 0 0" fill="none" stroke="#ccc" stroke-width="1" />
    </pattern>
  </defs>
  <rect width="100%" height="100%" fill="url(#grid)" />
  <line x1="224" y1="480" x2="192" y2="448" stroke="BLUE" marker-end="url(#end)" />
  <line x1="96" y1="448" x2="64" y2="416" stroke="RED" marker-end="url(#end)" />
  <line x1="96" y1="384" x2="128" y2="352" stroke="AQUA" marker-end="url(#end)" />
  <line x1="160" y1="480" x2="192" y2="448" stroke="RED" marker-end="url(#end)" />
  <line x1="32" y1="384" x2="64" y2="352" stroke="GREEN" marker-end="url(#end)" />
  <line x1="96" y1="352" x2="128" y2="320" stroke="ORANGE" marker-end="url(#end)" />
</svg>'''

# Mock the request object
mock_request = Mock()
mock_request.data.decode.return_value = svg_content

# Temporarily replace the request in the module
original_request = main.request
main.request = mock_request

try:
    # Test the slpu function
    response_data, status_code, headers = main.slpu()
    
    print(f"Status Code: {status_code}")
    print(f"Content-Type: {headers.get('Content-Type')}")
    print(f"Response: {response_data}")
    
    # Validate the response format
    if response_data.startswith('<svg') and 'text' in response_data:
        print("✓ Response format is correct (SVG with text element)")
    else:
        print("✗ Response format is incorrect")
        
    # Extract rolls from response
    import re
    text_match = re.search(r'<text>(.*?)</text>', response_data)
    if text_match:
        rolls_str = text_match.group(1)
        rolls = [int(r) for r in rolls_str]
        print(f"✓ Extracted rolls: {rolls}")
        print(f"✓ Number of rolls: {len(rolls)}")
        
        # Test that rolls are valid (1-6)
        if all(1 <= r <= 6 for r in rolls):
            print("✓ All rolls are valid (1-6)")
        else:
            print("✗ Some rolls are invalid")
            
        # Test the game simulation
        board_data = main.parse_svg_board(svg_content)
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
