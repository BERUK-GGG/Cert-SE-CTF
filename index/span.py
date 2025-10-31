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

binary_string = convert_to_binary()

if __name__ == "__main__":
    binary = convert_to_binary()
    print(f"Binary length: {len(binary)}")
    print(f"Number of 1s: {binary.count('1')}")
    print(f"Number of 0s: {binary.count('0')}")
    print(f"First 100 bits: {binary}")
    text = ''.join(chr(int(binary_string[i:i+8], 2)) for i in range(0, len(binary_string), 8))
    print(text)
    #print(f"Binary string: {binary}")