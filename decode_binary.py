#!/usr/bin/env python3
import re

def extract_highlighted_spans():
    """Extract span numbers from span.txt file"""
    highlighted_spans = set()
    
    with open('span.txt', 'r') as f:
        content = f.read()
    
    # Find all numbers inside span:nth-of-type()
    pattern = r'span:nth-of-type\((\d+)\)'
    matches = re.findall(pattern, content)
    
    for match in matches:
        highlighted_spans.add(int(match))
    
    return highlighted_spans

def convert_to_binary():
    """Convert 4096 spans to binary: highlighted=1, others=0"""
    highlighted = extract_highlighted_spans()
    
    binary_string = ""
    for span_num in range(1, 4097):  # spans 1-4096
        if span_num in highlighted:
            binary_string += "1"
        else:
            binary_string += "0"
    
    return binary_string

def try_ascii_decode(binary_str):
    """Try to decode binary as ASCII characters"""
    print("=== ASCII DECODE ATTEMPTS ===")
    
    # Try 8-bit chunks (standard ASCII)
    print("8-bit ASCII:")
    for i in range(0, len(binary_str) - 7, 8):
        chunk = binary_str[i:i+8]
        try:
            ascii_val = int(chunk, 2)
            if 32 <= ascii_val <= 126:  # Printable ASCII
                char = chr(ascii_val)
                print(f"  {chunk} -> {ascii_val} -> '{char}'")
            elif ascii_val == 0:
                print(f"  {chunk} -> {ascii_val} -> NULL")
        except:
            continue
    
    # Try 7-bit chunks
    print("\n7-bit ASCII:")
    for i in range(0, len(binary_str) - 6, 7):
        chunk = binary_str[i:i+7]
        try:
            ascii_val = int(chunk, 2)
            if 32 <= ascii_val <= 126:
                char = chr(ascii_val)
                print(f"  {chunk} -> {ascii_val} -> '{char}'")
        except:
            continue

def look_for_patterns(binary_str):
    """Look for specific patterns that might indicate flag format"""
    print("\n=== PATTERN ANALYSIS ===")
    
    # Look for common flag patterns in binary
    # "ctf{" in ASCII: 01100011 01110100 01100110 01111011
    ctf_pattern = "01100011011101000110011001111011"
    if ctf_pattern in binary_str:
        pos = binary_str.find(ctf_pattern)
        print(f"Found 'ctf{{' pattern at position {pos}")
    
    # Look for repeating patterns
    print("Looking for repeating 8-bit patterns...")
    for length in [8, 16, 32]:
        for i in range(0, min(200, len(binary_str) - length)):
            pattern = binary_str[i:i+length]
            count = binary_str.count(pattern)
            if count > 3 and '1' in pattern:  # Must contain at least one 1
                print(f"  Pattern '{pattern}' repeats {count} times")

def decode_first_bytes(binary_str):
    """Decode the first several bytes to see if there's readable text"""
    print("\n=== FIRST BYTES DECODE ===")
    
    for i in range(0, min(320, len(binary_str)), 8):
        if i + 8 <= len(binary_str):
            chunk = binary_str[i:i+8]
            try:
                ascii_val = int(chunk, 2)
                char = chr(ascii_val) if 32 <= ascii_val <= 126 else f"[{ascii_val}]"
                print(f"Byte {i//8 + 1:2d}: {chunk} -> {ascii_val:3d} -> {char}")
            except:
                print(f"Byte {i//8 + 1:2d}: {chunk} -> Invalid")

if __name__ == "__main__":
    binary = convert_to_binary()
    print(f"Binary length: {len(binary)}")
    print(f"Number of 1s: {binary.count('1')}")
    print(f"First 64 bits: {binary[:64]}")
    
    decode_first_bytes(binary)
    try_ascii_decode(binary[:400])  # Just first 50 bytes
    look_for_patterns(binary)
