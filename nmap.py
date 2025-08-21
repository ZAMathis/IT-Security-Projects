import socket
import time

TIMEOUT = 5  # Default timeout for socket connections in seconds
# PORTS = [22, 80, 443, 8000] # List of ports to scan for now

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

# Let's build a function to parse the ports specified by the user
def parse_ports(port_string):
    ports = []

    for part in port_string.split(','):
        # Handle ranges of ports first
        if '-' in part:
            start, end = part.split('-')
            start, end = int(start), int(end)
            ports.extend(range(start, end + 1))
        else:
            ports.append(int(part))
    return ports

def main():
    target = input("Enter the target IP address or hostname: ")
    ports = parse_ports(input("Enter ports to scan (comma-separated or ranges, e.g., 22,80,443 or 8000-8005): "))
    print(f"Scanning ports on {target}...")

    # Starting a timer
    start_time = time.perf_counter()

    for port in ports:
        if scan_port(target, port):
            print(f"Port {port} is open on {target}.")
        else:
            print(f"Port {port} is closed on {target}.")
    
    # Ending the timer
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print(f"Scan completed in {elapsed_time:.2f} seconds.")

if __name__ == "__main__":
    main()