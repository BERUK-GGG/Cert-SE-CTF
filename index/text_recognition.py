

def load_grid():
    """Load the grid from file"""
    grid = []
    with open('steganography_grid.txt', 'r') as f:
        for line in f:
            if ':' in line:
                parts = line.strip().split(': ')
                if len(parts) == 2:
                    grid.append(parts[1])
    return grid

def try_text_recognition(grid):
    """Try various approaches to recognize text patterns"""
    
    print("Attempting text recognition on 64x64 grid...")
    print("="*50)
    
    # Approach 1: Look for readable text horizontally in different regions
    print("1. Scanning for horizontal text patterns:")
    
    # Focus on regions that had high density
    promising_regions = [
        (24, 32, 16, 32),  # Around rows 25-32, cols 17-32 had very high density
        (32, 40, 40, 56), 
        (40, 48, 12, 28),
        (48, 56, 24, 40)
    ]
    
    for start_row, end_row, start_col, end_col in promising_regions:
        print(f"\nRegion [{start_row+1}-{end_row}, {start_col+1}-{end_col}]:")
        for row in range(start_row, min(end_row, len(grid))):
            segment = grid[row][start_col:end_col]
            # Try to interpret patterns as letters
            letters = pattern_to_letters(segment)
            print(f"  Row {row+1:2d}: {segment} -> {letters}")
    
    # Approach 2: Try reading vertically
    print(f"\n2. Vertical text analysis:")
    
    for col_start in range(10, 50, 8):
        print(f"\nColumns {col_start}-{col_start+7}:")
        for col_offset in range(8):
            col = col_start + col_offset
            if col < 64:
                vertical = ""
                for row in range(20, 45):  # Focus on middle section
                    if row < len(grid) and col < len(grid[row]):
                        vertical += grid[row][col]
                
                if vertical.count('#') > 5:
                    letters = pattern_to_letters(vertical)
                    print(f"  Col {col:2d}: {vertical} -> {letters}")

def pattern_to_letters(pattern_str):
    """Try to convert a pattern string to letters"""
    
    # Simple heuristic approach
    letters = []
    
    # Split on dots and analyze # groups
    parts = pattern_str.split('.')
    
    for part in parts:
        if len(part) >= 2:  # Only consider groups of 2+ # characters
            # Very basic letter recognition based on pattern length
            if len(part) == 2:
                letters.append('I')
            elif len(part) == 3:
                letters.append('T')
            elif len(part) == 4:
                letters.append('F')
            elif len(part) >= 5:
                letters.append('M')
    
    return ''.join(letters) if letters else '?'

def check_specific_regions(grid):
    """Check the most promising high-density regions more carefully"""
    
    print("\n3. Detailed analysis of highest density regions:")
    
    # The region around rows 25-32, cols 17-24 had 55% density
    high_density_region = (24, 32, 16, 24)  # 0-indexed
    start_row, end_row, start_col, end_col = high_density_region
    
    print(f"\nHighest density region [{start_row+1}-{end_row}, {start_col+1}-{end_col}]:")
    
    region_pattern = []
    for row in range(start_row, min(end_row, len(grid))):
        segment = grid[row][start_col:end_col]
        region_pattern.append(segment)
        print(f"  Row {row+1:2d}: {segment}")
    
    # Try to interpret this as 8x8 character blocks
    print("\nTrying to interpret as character blocks:")
    
    # Look at this as potential letters/numbers
    print("As potential ASCII art:")
    for i, row_pattern in enumerate(region_pattern):
        visual = row_pattern.replace('#', '█').replace('.', '░')
        print(f"  {start_row+i+1:2d}: {visual}")

def look_for_flag_format(grid):
    """Specifically look for common flag formats like ctf{...}"""
    
    print("\n4. Searching for flag format patterns:")
    
    # Look for potential bracket patterns [ or { 
    # These might appear as vertical lines with some horizontal elements
    
    bracket_patterns = []
    
    # Check for vertical lines that might be brackets
    for col in range(64):
        vertical_line = ""
        consecutive_hashes = 0
        max_consecutive = 0
        
        for row in range(64):
            if row < len(grid) and col < len(grid[row]):
                if grid[row][col] == '#':
                    consecutive_hashes += 1
                    max_consecutive = max(max_consecutive, consecutive_hashes)
                else:
                    consecutive_hashes = 0
                vertical_line += grid[row][col]
        
        # If we have a long vertical line, might be a bracket
        if max_consecutive >= 8:
            print(f"Potential bracket at column {col+1}: {max_consecutive} consecutive #'s")
            
            # Show context around this column
            for row in range(20, 45):  # Focus on middle area
                if row < len(grid):
                    context = grid[row][max(0, col-3):min(64, col+4)]
                    print(f"  Row {row+1}: {context}")
            print()

def manual_interpretation(grid):
    """Manual examination of the most promising areas"""
    
    print("\n5. Manual interpretation attempt:")
    
    # The analysis showed several regions with 40-55% density
    # Let's examine the one at rows 25-32, cols 17-24 more carefully
    
    print("Examining the highest density region (rows 25-32, cols 17-24):")
    
    # Extract this 8x8 region
    region = []
    for row in range(24, 32):  # 0-indexed
        if row < len(grid):
            segment = grid[row][16:24]  # 0-indexed
            region.append(segment)
            
            # Convert to more visible characters
            visual = segment.replace('#', '██').replace('.', '  ')
            print(f"Row {row+1:2d}: {segment} -> {visual}")
    
    print("\nTrying different interpretations...")
    
    # Maybe the text is rotated or needs different scaling
    # Let's try looking at it as 4x4 blocks within the 8x8 region
    
    print("\nAs 4x4 sub-blocks:")
    for block_row in range(0, 8, 4):
        for block_col in range(0, 8, 4):
            print(f"\nBlock at [{block_row},{block_col}]:")
            for r in range(4):
                if block_row + r < len(region):
                    line = region[block_row + r][block_col:block_col+4]
                    visual = line.replace('#', '█').replace('.', '░')
                    print(f"  {visual}")

if __name__ == "__main__":
    grid = load_grid()
    print(f"Loaded grid: {len(grid)} rows x {len(grid[0]) if grid else 0} cols")
    
    try_text_recognition(grid)
    check_specific_regions(grid) 
    look_for_flag_format(grid)
    manual_interpretation(grid)
