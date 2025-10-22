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

def decode_mod95_plus32():
    """Try mod 95 + 32 on all spans to find the flag"""
    print("=== MOD 95 + 32 DECODE (Looking for flag) ===")
    
    spans = extract_highlighted_spans()
    
    result = ""
    for i, span_num in enumerate(spans):
        ascii_val = (span_num % 95) + 32
        char = chr(ascii_val)
        result += char
        
        # Print first 100 characters with position info
        if i < 100:
            print(f"  Pos {i:2d}: {span_num:4d} % 95 + 32 = {ascii_val:3d} -> '{char}'")
    
    print(f"\nFull decoded string ({len(result)} chars):")
    print(result)
    
    # Look for flag patterns
    print(f"\n=== SEARCHING FOR FLAG PATTERNS ===")
    
    # Look for common flag formats
    flag_patterns = [
        r'ctf\{[^}]+\}',
        r'flag\{[^}]+\}',
        r'CERT\{[^}]+\}',
        r'\{[^}]+\}',
    ]
    
    for pattern in flag_patterns:
        matches = re.findall(pattern, result, re.IGNORECASE)
        if matches:
            print(f"Found {len(matches)} matches for pattern '{pattern}':")
            for match in matches:
                print(f"  {match}")
    
    # Look for any substring containing braces
    brace_start = result.find('{')
    brace_end = result.find('}')
    
    if brace_start != -1 and brace_end != -1 and brace_start < brace_end:
        potential_flag = result[brace_start:brace_end+1]
        print(f"\nPotential flag found: {potential_flag}")
        
        # Also check context around it
        start = max(0, brace_start - 10)
        end = min(len(result), brace_end + 10)
        context = result[start:end]
        print(f"Context: {context}")
    
    # Check for patterns that might be encoded differently
    print(f"\n=== LOOKING FOR ENCODED PATTERNS ===")
    
    # Check every 10 characters for patterns
    for start in range(0, min(200, len(result)), 10):
        chunk = result[start:start+10]
        print(f"Chars {start:2d}-{start+9:2d}: {chunk}")

if __name__ == "__main__":
    decode_mod95_plus32()
