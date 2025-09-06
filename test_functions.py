import main

# Test SVG content
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

# Test parsing
board_data = main.parse_svg_board(svg_content)
print(f"Board size: {board_data['board_size']}")
print(f"Jumps: {board_data['jumps']}")

# Test roll generation
rolls = main.generate_rolls(board_data['board_size'], 2, board_data['jumps'])
print(f"Generated rolls: {rolls}")
print(f"Roll count: {len(rolls)}")
