#!/usr/bin/env python3
import re

def extract_highlighted_spans():
    """Extract span numbers from span.txt file"""
    highlighted_spans = []
    
    with open('span.txt', 'r') as f:
        content = f.read()
    
    # Find all numbers inside span:nth-of-type()
    pattern = r'span:nth-of-type\((\d+)\)'
    matches = re.findall(pattern, content)
    
    for match in matches:
        highlighted_spans.append(int(match))
    
    return sorted(highlighted_spans)

def try_direct_ascii():
    """Try treating the span numbers directly as ASCII values"""
    print("=== DIRECT ASCII FROM SPAN NUMBERS ===")
    
    spans = extract_highlighted_spans()
    
    # Try first 50 span numbers as ASCII
    for i, span_num in enumerate(spans[:50]):
        if 32 <= span_num <= 126:  # Printable ASCII range
            char = chr(span_num)
            print(f"Span {span_num:4d} -> '{char}'")
        else:
            print(f"Span {span_num:4d} -> [non-printable]")
    
    print(f"\nFirst 20 spans as string:")
    result = ""
    for span_num in spans[:20]:
        if 32 <= span_num <= 126:
            result += chr(span_num)
        else:
            result += f"[{span_num}]"
    print(result)

def try_modular_arithmetic():
    """Try different modular operations on span numbers"""
    print("\n=== MODULAR ARITHMETIC ATTEMPTS ===")
    
    spans = extract_highlighted_spans()
    
    # Try mod 128 (7-bit ASCII)
    print("Mod 128 (7-bit ASCII):")
    result = ""
    for i, span_num in enumerate(spans[:30]):
        ascii_val = span_num % 128
        if 32 <= ascii_val <= 126:
            char = chr(ascii_val)
            result += char
            print(f"  {span_num} % 128 = {ascii_val} -> '{char}'")
    print(f"Result: {result}")
    
    # Try mod 95 + 32 (printable ASCII range)
    print("\nMod 95 + 32 (printable ASCII):")
    result = ""
    for i, span_num in enumerate(spans[:30]):
        ascii_val = (span_num % 95) + 32
        char = chr(ascii_val)
        result += char
        print(f"  {span_num} % 95 + 32 = {ascii_val} -> '{char}'")
    print(f"Result: {result}")

def analyze_span_differences():
    """Look at differences between consecutive spans"""
    print("\n=== SPAN DIFFERENCES ANALYSIS ===")
    
    spans = extract_highlighted_spans()
    
    print("First 20 spans:", spans[:20])
    
    differences = []
    for i in range(1, min(len(spans), 21)):
        diff = spans[i] - spans[i-1]
        differences.append(diff)
        print(f"  {spans[i]} - {spans[i-1]} = {diff}")
    
    # Try differences as ASCII
    print("\nDifferences as ASCII:")
    result = ""
    for diff in differences:
        if 32 <= diff <= 126:
            char = chr(diff)
            result += char
            print(f"  {diff} -> '{char}'")
    print(f"Differences as string: {result}")

def try_base_conversions():
    """Try different base interpretations"""
    print("\n=== BASE CONVERSION ATTEMPTS ===")
    
    spans = extract_highlighted_spans()
    
    # Try treating first few spans as a big number in different bases
    for base in [8, 10, 16]:
        print(f"\nBase {base} interpretation of first 5 spans:")
        for i in range(min(5, len(spans))):
            span_num = spans[i]
            try:
                # Convert span number to string and interpret in different base
                span_str = str(span_num)
                if all(int(digit) < base for digit in span_str):
                    value = int(span_str, base)
                    if 32 <= value <= 126:
                        print(f"  {span_num} (base {base}) = {value} -> '{chr(value)}'")
            except:
                pass

if __name__ == "__main__":
    spans = extract_highlighted_spans()
    print(f"Total highlighted spans: {len(spans)}")
    print(f"First 10 spans: {spans[:10]}")
    print(f"Last 10 spans: {spans[-10:]}")
    
    try_direct_ascii()
    try_modular_arithmetic()
    analyze_span_differences()
    try_base_conversions()
