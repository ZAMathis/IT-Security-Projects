"""
Yeah, I didn't write this part lol. But it was too complex for me to think about.
However it was necessary to have a way to decode responses from various protocols.
Thanks, ChatGPT!
"""

import struct

def decode_dns(data: bytes) -> str:
    """Decode a minimal DNS response header."""
    if len(data) < 12:
        return "Invalid DNS response"
    # First 12 bytes are header
    (tid, flags, qdcount, ancount, nscount, arcount) = struct.unpack(">HHHHHH", data[:12])
    rcode = flags & 0x000F
    return f"DNS response | answers={ancount}, rcode={rcode}"

def decode_ntp(data: bytes) -> str:
    """Decode an NTP response (very basic)."""
    if len(data) < 48:
        return "Invalid NTP response"
    first_byte = data[0]
    li = (first_byte >> 6) & 0x3
    vn = (first_byte >> 3) & 0x7
    mode = first_byte & 0x7
    return f"NTP response | version={vn}, mode={mode}, LI={li}"

def decode_snmp(data: bytes) -> str:
    """Very rough SNMP decoder."""
    if not data.startswith(b"\x30"):
        return "Invalid SNMP response"
    return f"SNMP response | length={len(data)} bytes"

def decode_tftp(data: bytes) -> str:
    """Parse TFTP opcode (first 2 bytes)."""
    if len(data) < 2:
        return "Invalid TFTP response"
    opcode = struct.unpack(">H", data[:2])[0]
    opcodes = {3: "DATA", 4: "ACK", 5: "ERROR"}
    return f"TFTP response | opcode={opcodes.get(opcode, opcode)}"
