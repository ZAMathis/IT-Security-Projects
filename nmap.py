import socket

TIMEOUT = 5  # Default timeout for socket connections in seconds
PORTS = [22, 80, 443, 8000] # List of ports to scan for now

def scan_port(target, port, timeout=TIMEOUT):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    
    try:
        result = sock.connect_ex((target, port))
        return result == 0  # Port is open
    except socket.gaierror:
        print(f"Hostname {target} could not be resolved.")
        return False
    except socket.timeout:
        print(f"Connection to {target}:{port} timed out.")
        return False
    finally:
        sock.close()

def main():
    target = '127.0.1'  # Localhost for testing, will change to use input later
    print(f"Scanning ports on {target}...")

    for port in PORTS:
        if scan_port(target, port):
            print(f"Port {port} is open on {target}.")
        else:
            print(f"Port {port} is closed on {target}.")
    print("Scan complete.")

if __name__ == "__main__":
    main()