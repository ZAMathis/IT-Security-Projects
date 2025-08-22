import socket
import argparse
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

TIMEOUT = 1  # Default timeout for socket connections in seconds

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
    
    # Now let's make this more like a command line tool with arguements -help, etc
    parser = argparse.ArgumentParser(description="Simple python port scanner")
    parser.add_argument("target", help="Target IP address or hostname to scan")
    parser.add_argument("-p", "--ports",
                        default="20, 21, 22, 23, 25, 53, 80, 110, 143, 443, 8080",
                        help="Comma-separated list of ports to scan (e.g., 22,80,443 or 8000-8005)")
    
    args = parser.parse_args()
    target = args.target
    ports = parse_ports(args.ports)
    print(f"Scanning ports on {target}...")

    # Starting a timer
    start_time = time.perf_counter()

    # Using ThreadPoolExecutor for concurrent scanning, storing in a result array
    results = []

    with ThreadPoolExecutor(max_workers=100) as executor:
        future_to_port = {executor.submit(scan_port, target, port): port for port in ports}

        # As each thread finishes, try to collect the result
        for future in as_completed(future_to_port):
            port = future_to_port[future]
            try:
                is_open = future.result()
                results.append((port, is_open))
            except Exception as e:
                print(f"Error scanning port {port}: {e}")
        
    # Print the results, sorted by port number
    results.sort(key=lambda x: x[0])
    for port, is_open in results:
        status = "open" if is_open else "closed"
        print(f"{port}/TCP {status}.")

    # Ending the timer
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print(f"Scan completed in {elapsed_time:.2f} seconds.")

if __name__ == "__main__":
    main()