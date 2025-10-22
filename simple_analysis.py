#!/usr/bin/env python3

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

def analyze_grid_simple(grid):
    """Simple, direct analysis of the grid"""
    
    print("=== SIMPLE GRID ANALYSIS ===")
    print(f"Grid size: {len(grid)}x{len(grid[0]) if grid else 0}")
    
    # Count total highlighted positions
    total_highlights = sum(row.count('#') for row in grid)
    print(f"Total highlighted positions: {total_highlights} out of {64*64} ({total_highlights/(64*64)*100:.1f}%)")
    
    # Just show the grid visually with better contrast
    print("\n=== VISUAL GRID (# = block, . = empty) ===")
    for i, row in enumerate(grid):
        print(f"{i+1:2d}: {row}")
    
    print("\n=== LOOKING FOR OBVIOUS PATTERNS ===")
    
    # Look for completely filled rows or columns
    for i, row in enumerate(grid):
        if row.count('#') > 50:  # More than 75% filled
            print(f"High-density row {i+1}: {row.count('#')}/64 filled")
    
    # Look for completely filled columns
    for col in range(64):
        col_data = ''.join(grid[row][col] for row in range(64))
        if col_data.count('#') > 50:
            print(f"High-density column {col+1}: {col_data.count('#')}/64 filled")
    
    # Look for rectangular regions
    print("\n=== CHECKING FOR RECTANGULAR PATTERNS ===")
    
    # Simple approach: look for areas where multiple consecutive rows have patterns
    consecutive_patterns = []
    
    for start_row in range(60):  # Don't go to the very end
        for start_col in range(60):
            # Check for 4x4 blocks of all #
            if (start_row + 4 <= 64 and start_col + 4 <= 64):
                block_filled = True
                for r in range(4):
                    for c in range(4):
                        if grid[start_row + r][start_col + c] != '#':
                            block_filled = False
                            break
                    if not block_filled:
                        break
                
                if block_filled:
                    print(f"Solid 4x4 block at row {start_row+1}, col {start_col+1}")

def look_for_text_blocks(grid):
    """Look for potential text characters in the grid"""
    
    print("\n=== SEARCHING FOR CHARACTER-LIKE PATTERNS ===")
    
    # Common approach: look for 8x8 or 5x7 character blocks
    # Let's try 8x8 first
    
    for start_row in range(0, 64-8, 8):  # Step by 8
        for start_col in range(0, 64-8, 8):
            
            # Extract 8x8 block
            block = []
            for r in range(8):
                block.append(grid[start_row + r][start_col:start_col + 8])
            
            # Calculate density of this block
            total_chars = 8 * 8
            filled_chars = sum(row.count('#') for row in block)
            density = filled_chars / total_chars
            
            # Only show blocks with reasonable density for text (10-80%)
            if 0.1 <= density <= 0.8:
                print(f"\nBlock at ({start_row+1},{start_col+1}) - density: {density:.2f}")
                for i, row in enumerate(block):
                    visual = row.replace('#', '█').replace('.', '░')
                    print(f"  {visual}")

def search_for_flag_strings(grid):
    """Look for common flag patterns like 'ctf' or 'flag'"""
    
    print("\n=== SEARCHING FOR FLAG-LIKE STRINGS ===")
    
    # Convert grid to a single string and look for patterns
    full_string = ''.join(''.join(row) for row in grid)
    
    # Look for repeating patterns that might encode letters
    print("Grid as single string (first 200 chars):")
    print(full_string[:200])
    
    # Try to find the boundaries of the actual content
    # Look for the first and last # characters
    first_hash = full_string.find('#')
    last_hash = full_string.rfind('#')
    
    print(f"\nFirst # at position: {first_hash}")
    print(f"Last # at position: {last_hash}")
    
    if first_hash != -1 and last_hash != -1:
        # Convert back to row/col
        first_row = first_hash // 64
        first_col = first_hash % 64
        last_row = last_hash // 64
        last_col = last_hash % 64
        
        print(f"First # at row {first_row+1}, col {first_col+1}")
        print(f"Last # at row {last_row+1}, col {last_col+1}")
        
        # Show the bounding box of content
        print(f"\nContent spans from row {first_row+1} to {last_row+1}")
        print(f"Showing this region:")
        
        for row in range(max(0, first_row-1), min(64, last_row+2)):
            print(f"{row+1:2d}: {grid[row]}")

if __name__ == "__main__":
    grid = load_grid()
    if not grid:
        print("Failed to load grid")
        exit(1)
    
    analyze_grid_simple(grid)
    look_for_text_blocks(grid)
    search_for_flag_strings(grid)
