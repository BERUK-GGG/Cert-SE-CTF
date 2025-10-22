#!/usr/bin/env python3

def create_html_visualization():
    """Create an HTML file to visualize the grid"""
    
    with open('steganography_grid.txt', 'r') as f:
        lines = f.readlines()
    
    html_content = """<!DOCTYPE html>
<html>
<head>
    <title>Steganography Grid Visualization</title>
    <style>
        body { 
            font-family: 'Courier New', monospace; 
            background-color: black; 
            color: white;
            padding: 20px;
        }
        .grid { 
            font-size: 8px; 
            line-height: 8px; 
            letter-spacing: 0px;
            white-space: pre;
        }
        .highlighted { color: lime; }
        .normal { color: #333; }
    </style>
</head>
<body>
    <h2>Steganography Grid (64x64)</h2>
    <div class="grid">
"""
    
    for line in lines:
        if ':' in line:
            parts = line.strip().split(': ')
            if len(parts) == 2:
                row_num = parts[0]
                pattern = parts[1]
                
                html_line = f"{row_num}: "
                for char in pattern:
                    if char == '#':
                        html_line += '<span class="highlighted">█</span>'
                    else:
                        html_line += '<span class="normal">░</span>'
                
                html_content += html_line + '\n'
    
    html_content += """    </div>
</body>
</html>"""
    
    with open('grid_visualization.html', 'w') as f:
        f.write(html_content)
    
d to grid_visualization.html")

def analyze_for_text():
    """Try to find readable text in the grid"""
    
    with open('steganography_grid.txt', 'r') as f:
        lines = f.readlines()
    
    # Extract just the pattern part
    grid = []
    for line in lines:
        if ':' in line:
            parts = line.strip().split(': ')
            if len(parts) == 2:
                grid.append(parts[1])
    
    print(f"Grid loaded: {len(grid)} rows x {len(grid[0]) if grid else 0} columns")
    
    # Look for common text patterns
    print("\nLooking for potential text regions...")
    
    # Check for horizontal text patterns (groups of # that might be letters)
    for i, row in enumerate(grid):
        # Look for sequences of # characters that might form letters
        groups = []
        current_group = ""
        
        for j, char in enumerate(row):
            if char == '#':
                if not current_group:
                    current_group = f"{j}"
                current_group += char
            else:
                if len(current_group) > 2:  # Only keep groups with 3+ characters
                    groups.append(current_group)
                current_group = ""
        
        if len(current_group) > 2:
            groups.append(current_group)
        
        if len(groups) >= 3:  # If row has multiple groups, might contain letters
            print(f"Row {i+1:2d}: {len(groups)} groups - {row}")
    
    # Try vertical analysis too
    print("\nChecking vertical patterns...")
    
    if grid:
        cols = len(grid[0])
        for col in range(0, cols, 8):  # Check every 8th column
            vertical_pattern = ""
            for row in range(len(grid)):
                if col < len(grid[row]):
                    vertical_pattern += grid[row][col]
            
            # Count consecutive # patterns
            hash_groups = 0
            in_group = False
            for char in vertical_pattern:
                if char == '#' and not in_group:
                    hash_groups += 1
                    in_group = True
                elif char == '.' and in_group:
                    in_group = False
            
            if hash_groups > 3:
                print(f"Column {col}: {hash_groups} groups - {vertical_pattern}")

def look_for_flag_pattern():
    """Specifically look for 'ctf{' or similar flag patterns"""
    
    with open('steganography_grid.txt', 'r') as f:
        lines = f.readlines()
    
    grid = []
    for line in lines:
        if ':' in line:
            parts = line.strip().split(': ')
            if len(parts) == 2:
                grid.append(parts[1])
    
    print("\nSearching for flag-like patterns...")
    
    # Look for areas with higher density that might contain text
    for start_row in range(0, len(grid)-8, 4):
        for start_col in range(0, 56, 4):  # 64-8=56
            
            # Check 8x8 block
            block_chars = 0
            block_hashes = 0
            
            for r in range(start_row, min(start_row + 8, len(grid))):
                for c in range(start_col, min(start_col + 8, len(grid[r]))):
                    block_chars += 1
                    if grid[r][c] == '#':
                        block_hashes += 1
            
            if block_chars > 0:
                density = block_hashes / block_chars
                
                # If density is between 30-70%, might contain readable text
                if 0.3 <= density <= 0.7:
                    print(f"\nHigh-density region at rows {start_row+1}-{start_row+8}, cols {start_col+1}-{start_col+8} (density: {density:.2f}):")
                    for r in range(start_row, min(start_row + 8, len(grid))):
                        segment = grid[r][start_col:start_col+8]
                        print(f"  {r+1:2d}: {segment}")

if __name__ == "__main__":
    print("Creating visualizations and analyzing steganography grid...")
    
    create_html_visualization()
    analyze_for_text()
    look_for_flag_pattern()
