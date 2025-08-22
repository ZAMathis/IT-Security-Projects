import socket
import argparse
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

TIMEOUT = 1.0  # Default timeout for socket connections in seconds

# Core function to scan a single port
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
        part = part.strip() # strip any whitespace, in case of errors
        # Handle ranges of ports first
        if '-' in part:
            start, end = part.split('-')
            start, end = int(start), int(end)
            ports.extend(range(start, end + 1))
        else:
            ports.append(int(part))

    return ports

# Let's add a function for grabbing banners of specific ports
def grab_banner(target, port, timeout=TIMEOUT):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((target, port))

        banner = None

        # We're going to redo the banner grabbing tailoring it to each service
        if port in [80, 8080, 8000, 8888]: # common http ports
            sock.sendall(b'HEAD / HTTP/1.0\r\n\r\n')
            banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
        elif port == 443:  # HTTPS
            banner = "Possible HTTPS service"
        elif port in [21, 22, 23, 25, 110, 143]:
            # guys like these usually greet first
            banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
        else:
            # if all else fails, we'll just try to grab SOMETHING
            try:
                banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
            except Exception:
                pass

        """
        # Try HTTP request first, since I'm having issues with getting 80 and 8080 banners
        try:
            sock.sendall(b'HEAD / HTTP/1.0\r\n\r\n')
            banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
        except Exception:
            pass

        # If we didn't get a banner from the HTTP request, we can try a regular banner grab
        if not banner:
            try:
                banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
            except Exception:
                pass
        """
        return banner if banner else None
    except Exception:
        return None
    finally:
        sock.close()

def main():
    
    # Now let's make this more like a command line tool with arguements -help, etc
    parser = argparse.ArgumentParser(description="Simple python port scanner")

    parser.add_argument("target", help="Target IP address or hostname to scan")

    parser.add_argument("-p", "--ports",
                        default="20, 21, 22, 23, 25, 53, 80, 110, 143, 443, 8080",
                        help="Comma-separated list of ports to scan (e.g., 22,80,443 or 8000-8005)")
    
    parser.add_argument("-t", "--timeout", type=float, default=TIMEOUT,
                        help="Timeout for each port scan in seconds (default: 1 second)")
    
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Enable verbose output")
    
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

            if args.verbose:
                print(f'Scanning port {port}')

            try:
                is_open = future.result()
                
                if is_open:
                    banner = grab_banner(target, port)
                    results.append((port, is_open, banner))
                else:
                    results.append((port, is_open, None))

            except Exception as e:
                print(f"Error scanning port {port}: {e}")
        
    # Print the results, sorted by port number
    results.sort(key=lambda x: x[0])

    for port, is_open, banner in results:
        status = "open" if is_open else "closed"
        line = f"{port}/TCP {status}"
        if is_open and banner:
            line += f" | {banner}"
        print(line)

    # Ending the timer
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print(f"Scan completed in {elapsed_time:.2f} seconds.")

if __name__ == "__main__":
    main()