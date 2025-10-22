#!/usr/bin/env python3
import hashlib


HASH = "983e3a1fbb4232fff96282ab9a37f89a"  # target hash (lowercase)
rockyou_path = "rockyou/rockyou.txt"    # <-- set this path

def md5_hex(s: bytes) -> str:
    return hashlib.md5(s).hexdigest()

def main():
    found = False
    with open(rockyou_path, "rb", buffering=16*1024*1024) as fh:
        for i, line in enumerate(fh, 1):
            word = line.strip()
            ctf_word = b"ctf[" + word + b"]"
            # try as-is
            if md5_hex(ctf_word) == HASH:
                print(f"Found (raw): {word.decode('utf-8', errors='replace')}")
                found = True
                break
            # try common variations if you want (uncomment as needed)
            # if md5_hex(word.lower()) == HASH: ...
            if i % 500000 == 0:
                print(f"checked {i} words...", flush=True)

    if not found:
        print("Not found in rockyou (as raw). Consider trying variations or using hashcat/john for speed.")

if __name__ == "__main__":
    main()
