#!/usr/bin/env python3

def read_grid():
    with open('steganography_grid.txt', 'r') as f:
        lines = f.readlines()
    
    grid = []
    for line in lines:
        parts = line.strip().split(': ')
        if len(parts) == 2:
            grid.append(parts[1])
    return grid

def print_small_regions(grid):
    """Print 8x8 regions to look for individual letters"""
    
    print("Looking at 8x8 regions for individual letters:")
    print("="*50)
    
    # Try different 8x8 regions
    for start_row in range(10, 50, 8):
        for start_col in range(10, 50, 8):
            print(f"Region [{start_row}-{start_row+7}, {start_col}-{start_col+7}]:")
            
            for i in range(8):
                if start_row + i < len(grid):
                    line = grid[start_row + i][start_col:start_col+8]
                    print(f"  {line}")
            print()

def try_bitmap_font_decode(grid):
    """Try to decode as if it's a bitmap font"""
    
    print("Bitmap font analysis - looking for 5x7 or 6x8 character patterns:")
    print("="*60)
    
    # Common sizes for bitmap fonts are 5x7, 6x8, 8x8
    char_width = 6
    char_height = 8
    
    # Try different starting positions
    for start_row in [20, 25, 30, 35, 40]:
        for start_col in range(0, 50, char_width):
            
            chars_in_line = []
            
            # Extract multiple characters in this row
            for char_offset in range(8):  # Try up to 8 characters
                char_col = start_col + char_offset * char_width
                if char_col + char_width >= len(grid[0]):
                    break
                
                # Extract character bitmap
                char_bitmap = []
                for row_offset in range(char_height):
                    if start_row + row_offset < len(grid):
                        char_line = grid[start_row + row_offset][char_col:char_col + char_width]
                        char_bitmap.append(char_line)
                
                # Try to recognize this character
                recognized = recognize_character(char_bitmap)
                if recognized:
                    chars_in_line.append(recognized)
                else:
                    chars_in_line.append('?')
            
            if any(c != '?' for c in chars_in_line):
                text = ''.join(chars_in_line).strip('?')
                if len(text) > 2:  # Only show if we have some recognizable text
                    print(f"Row {start_row}, Col {start_col}: '{text}'")
                    
                    # Show the actual bitmap for verification
                    print("  Bitmap:")
                    for row_offset in range(char_height):
                        if start_row + row_offset < len(grid):
                            line = grid[start_row + row_offset][start_col:start_col + len(chars_in_line) * char_width]
                            print(f"    {line}")
                    print()

def recognize_character(char_bitmap):
    """Try to recognize a character from its bitmap"""
    
    if not char_bitmap or len(char_bitmap) < 6:
        return None
    
    # Simple pattern matching for common letters
    # This is very basic - just looking for distinctive patterns
    
    # Join all rows to make pattern matching easier
    pattern = ''.join(char_bitmap)
    
    # Count # density and positions
    hash_count = pattern.count('#')
    total_chars = len(pattern)
    
    if hash_count < 2:
        return None  # Too sparse
    
    if hash_count > total_chars * 0.8:
        return None  # Too dense
    
    # Look for specific letter patterns (very basic)
    # This is just a starting point - real OCR would be much more sophisticated
    
    # Check first and last rows for patterns
    top_row = char_bitmap[0] if char_bitmap else ""
    bottom_row = char_bitmap[-1] if len(char_bitmap) > 0 else ""
    
    # Very basic pattern recognition
    if pattern.count('###') >= 2:  # Might be 'E', 'F', 'H', etc.
        if top_row.count('#') >= 3 and bottom_row.count('#') >= 3:
            return 'E'
        elif top_row.count('#') >= 3 and bottom_row.count('#') <= 1:
            return 'F'
    
    if pattern.count('##') >= 3 and '#.#' in pattern:
        return 'H'
    
    # Look for vertical patterns
    vertical_lines = 0
    for col in range(len(char_bitmap[0]) if char_bitmap else 0):
        col_pattern = ""
        for row in char_bitmap:
            if col < len(row):
                col_pattern += row[col]
        if col_pattern.count('#') >= 4:  # Strong vertical line
            vertical_lines += 1
    
    if vertical_lines >= 2:
        return 'H'
    elif vertical_lines == 1:
        return 'I'
    
    return None  # Couldn't recognize

def manual_inspection(grid):
    """Manually inspect promising areas"""
    
    print("Manual inspection of specific regions:")
    print("="*40)
    
    # Look at some specific areas that seemed promising
    regions = [
        (25, 32, 15, 35, "Center region"),
        (35, 42, 20, 40, "Lower center"),
        (28, 35, 45, 60, "Right side"),
    ]
    
    for start_row, end_row, start_col, end_col, description in regions:
        print(f"{description} [{start_row}-{end_row}, {start_col}-{end_col}]:")
        
        for i in range(start_row, min(end_row + 1, len(grid))):
            if i < len(grid):
                line = grid[i][start_col:min(end_col + 1, len(grid[i]))]
                print(f"  {i+1:2d}: {line}")
        print()

if __name__ == "__main__":
    grid = read_grid()
    
    print_small_regions(grid)
    print("\n" + "="*60 + "\n")
    
    try_bitmap_font_decode(grid)
    print("\n" + "="*60 + "\n")
    
    manual_inspection(grid)
