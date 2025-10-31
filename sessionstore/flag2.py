import json

# Read the formatted JSON file
with open("sessionstore.json", "r") as f:
    data = json.load(f)

print("=== FIREFOX SESSION ANALYSIS ===\n")

# Extract all URLs from all tabs
urls = []
for window in data["windows"]:
    for tab in window["tabs"]:
        for entry in tab["entries"]:
            urls.append({
                "url": entry["url"],
                "title": entry["title"],
                "timestamp": tab.get("lastAccessed", "unknown")
            })

print("All URLs visited:")
print("-" * 50)
for i, item in enumerate(urls, 1):
    print(f"{i}. {item['url']}")
    print(f"   Title: {item['title']}")
    print()

# Extract just the CERT-SE URLs with fragments
cert_urls = [item for item in urls if "cert.se/#" in item["url"]]

print("-" * 60)
fragments = []
for item in cert_urls:
    fragment = item["url"].split("#")[1]
    fragments.append(fragment)
    print(f"URL: {item['url']}")
    print(f"Fragment: {fragment}")
    print()

print("=== EXTRACTED FRAGMENTS ===")
print("-" * 30)
print("Fragments in order:")
for i, frag in enumerate(fragments, 1):
    print(f"{i}. {frag}")

possible_flag = ''.join(fragments)
print(f"\nAll fragments combined: {possible_flag}")
print(len(possible_flag))

import re


def decode_positional(possible_flag):
    # find all occurrences of number followed by one-or-more non-digit chars
    tokens = re.findall(r'(\d+)([^0-9])', possible_flag)
    # build mapping {position: char}
    mapping = {int(pos): ch for pos, ch in tokens}
    # reconstruct from 1..max_pos
    maxpos = max(mapping)
    return ''.join(mapping.get(i, '?') for i in range(1, maxpos + 1))
decoded_flag = decode_positional(possible_flag)
print(f"\nDecoded flag from positional encoding: {decoded_flag}")