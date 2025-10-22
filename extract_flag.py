#!/usr/bin/env python3
import re

def extract_highlighted_spans():
    """Extract span numbers from span.txt file"""
    highlighted_spans = []
    
    with open('span.txt', 'r') as f:
        content = f.read()
    
    pattern = r'span:nth-of-type\((\d+)\)'
    matches = re.findall(pattern, content)
    
    for match in matches:
        highlighted_spans.append(int(match))
    
    return sorted(highlighted_spans)

def find_flag_carefully():
    """More carefully extract the flag"""
    spans = extract_highlighted_spans()
    
    # Decode using mod 95 + 32
    result = ""
    for span_num in spans:
        ascii_val = (span_num % 95) + 32
        char = chr(ascii_val)
        result += char
    
    print(f"Full decoded string ({len(result)} chars):")
    print(repr(result))  # Using repr to see escape characters clearly
    
    # Find all brace pairs
    brace_positions = []
    open_braces = []
    
    for i, char in enumerate(result):
        if char == '{':
            open_braces.append(i)
        elif char == '}' and open_braces:
            start = open_braces.pop()
            brace_positions.append((start, i))
    
    print(f"\nFound {len(brace_positions)} brace pairs:")
    for i, (start, end) in enumerate(brace_positions):
        content = result[start:end+1]
        print(f"  Pair {i+1}: positions {start}-{end}")
        print(f"    Content: {repr(content)}")
        print(f"    Length: {len(content)} chars")
        
        # Show context
        context_start = max(0, start - 5)
        context_end = min(len(result), end + 5)
        context = result[context_start:context_end]
        print(f"    Context: {repr(context)}")
        print()
    
    # Look for flag-like patterns
    print("=== ANALYZING FOR FLAG PATTERNS ===")
    
    for i, (start, end) in enumerate(brace_positions):
        content = result[start:end+1]
        
        # Check if it looks like a flag
        if len(content) > 10:  # Reasonable flag length
            print(f"Potential flag candidate {i+1}: {content}")
            
            # Check for common flag prefixes before the brace
            prefix_start = max(0, start - 10)
            prefix = result[prefix_start:start]
            print(f"  Prefix: {repr(prefix)}")
            
            # Look for letters that might be 'ctf' or 'flag'
            if 'ctf' in prefix.lower() or 'flag' in prefix.lower() or 'cert' in prefix.lower():
                print(f"  *** POTENTIAL FLAG: {prefix}{content}")

if __name__ == "__main__":
    find_flag_carefully()
