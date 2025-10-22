#!/usr/bin/env python3

import re

def extract_highlighted_spans():
    """Extract the span numbers that are highlighted in lightgreen"""
    
    with open('index.html', 'r') as f:
        content = f.read()
    
    # Find the CSS rule that sets background-color to lightgreen
    # Looking for the pattern: span:nth-of-type(NUMBER)
    pattern = r'span:nth-of-type\((\d+)\)'
    
    # Extract all the span numbers
    matches = re.findall(pattern, content)
    
    # Convert to integers and sort
    span_numbers = [int(match) for match in matches]
    span_numbers.sort()
    
    print(f"Found {len(span_numbers)} highlighted spans")
    print(f"Range: {min(span_numbers)} to {max(span_numbers)}")
    
    return span_numbers

def create_grid(span_numbers):
    """Convert span numbers to a 64x64 grid"""
    
    # With 4096 spans, this is likely a 64x64 grid (64*64 = 4096)
    grid_size = 64
    
    # Create empty grid
    grid = [['.' for _ in range(grid_size)] for _ in range(grid_size)]
    
    # Mark highlighted positions
    for span_num in span_numbers:
        # Convert 1-based span number to 0-based index
        index = span_num - 1
        
        # Convert to row, col
        row = index // grid_size
        col = index % grid_size
        
        if 0 <= row < grid_size and 0 <= col < grid_size:
            grid[row][col] = '#'
    
    return grid

def save_grid(grid, filename='grid_output.txt'):
    """Save grid to file"""
    with open(filename, 'w') as f:
        for i, row in enumerate(grid):
            line = ''.join(row)
            f.write(f"{i+1:2d}: {line}\n")
    print(f"Grid saved to {filename}")

def display_grid_info(grid):
    """Display information about the grid"""
    total_cells = len(grid) * len(grid[0])
    highlighted_cells = sum(row.count('#') for row in grid)
    
    print(f"Grid size: {len(grid)}x{len(grid[0])}")
    print(f"Total cells: {total_cells}")
    print(f"Highlighted cells: {highlighted_cells}")
    print(f"Percentage highlighted: {highlighted_cells/total_cells*100:.1f}%")
    
    # Show first few rows
    print("\nFirst 10 rows of grid:")
    for i in range(min(10, len(grid))):
        line = ''.join(grid[i])
        print(f"{i+1:2d}: {line}")

if __name__ == "__main__":
    print("Extracting highlighted span selectors from index.html...")
    
    span_numbers = extract_highlighted_spans()
    
    print("\nConverting to 64x64 grid...")
    grid = create_grid(span_numbers)
    
    display_grid_info(grid)
    
    save_grid(grid, 'steganography_grid.txt')
    
    print("\nGrid analysis complete!")
