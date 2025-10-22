import pyshark
import base64

# Path to your pcap file
pcap_file = "cert-se_ctf2025.pcap"

# Load the capture
capture_udp = pyshark.FileCapture(pcap_file, display_filter="udp")


def decode_udp_payload(capture):
    for i, packet in enumerate(capture):
        try:
            # Skip DNS packets (UDP port 53)
            src_port = int(packet.udp.srcport)
            dst_port = int(packet.udp.dstport)
            if src_port == 53 or dst_port == 53:
                continue

            # Extract UDP payload (if it exists)
            data = packet.udp.payload.replace(":", "")
            raw_bytes = bytes.fromhex(data)

            # Try Base64 decode
            decoded = base64.b64decode(raw_bytes).decode(errors="ignore")
            print(decoded, end="")
        except Exception as e:
            # Skip packets that fail decoding
            continue



decode_udp_payload(capture_udp)
