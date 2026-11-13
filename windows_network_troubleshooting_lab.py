"""
Windows Network & Troubleshooting Lab
A beginner-friendly, read-only network diagnostics toolkit.

Python: 3.10+
Platform: Windows 10/11
Dependencies: Python standard library only
"""

import platform
import socket
import subprocess
from datetime import datetime
from pathlib import Path


def run_command(command, timeout=20):
    """Run a system command safely and return its output."""
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            errors="replace",
            timeout=timeout,
            shell=False,
        )
        output = result.stdout.strip()
        if result.stderr.strip():
            output += "\n" + result.stderr.strip()
        return output or "(No output returned.)"
    except subprocess.TimeoutExpired:
        return "The command timed out. The network may be slow or unreachable."
    except FileNotFoundError:
        return f"Required command was not found: {command[0]}"
    except Exception as error:
        return f"An error occurred: {error}"


def show_network_configuration():
    """Display detailed Windows network configuration."""
    print("\n=== NETWORK CONFIGURATION ===")
    if platform.system() != "Windows":
        print("This feature is designed for Windows 10/11.")
        return
    print(run_command(["ipconfig", "/all"]))


def test_connectivity():
    """Ping a host to test basic network connectivity."""
    print("\n=== CONNECTIVITY TEST ===")
    host = input("Enter a hostname or IP address (e.g. google.com): ").strip()
    if not host or any(char.isspace() for char in host):
        print("Please enter one valid hostname or IP address.")
        return

    if platform.system() == "Windows":
        command = ["ping", "-n", "4", host]
    else:
        command = ["ping", "-c", "4", host]

    print(run_command(command, timeout=25))


def dns_lookup():
    """Resolve a hostname and display its IP addresses."""
    print("\n=== DNS LOOKUP ===")
    hostname = input("Enter a hostname (e.g. google.com): ").strip()
    if not hostname or any(char.isspace() for char in hostname):
        print("Please enter one valid hostname.")
        return

    try:
        results = socket.getaddrinfo(hostname, None)
        addresses = sorted({item[4][0] for item in results})
        print(f"Hostname : {hostname}")
        print("IP address(es):")
        for address in addresses:
            print(f"  - {address}")
        print("Status   : DNS resolution successful")
    except socket.gaierror as error:
        print(f"DNS lookup failed: {error}")
        print("Status   : Name resolution unsuccessful")


def trace_route():
    """Trace the network route to a destination."""
    print("\n=== TRACEROUTE ===")
    host = input("Enter a hostname or IP address: ").strip()
    if not host or any(char.isspace() for char in host):
        print("Please enter one valid hostname or IP address.")
        return

    if platform.system() == "Windows":
        command = ["tracert", "-d", "-h", "12", "-w", "1000", host]
    else:
        print("This starter project currently supports tracert on Windows.")
        return

    print(run_command(command, timeout=35))


def check_tcp_port():
    """Check whether a TCP port on a host accepts a connection."""
    print("\n=== TCP PORT CHECK ===")
    host = input("Enter hostname or IP address (e.g. example.com): ").strip()
    if not host or any(char.isspace() for char in host):
        print("Please enter one valid hostname or IP address.")
        return

    port_text = input("Enter TCP port (e.g. 443 for HTTPS): ").strip()
    try:
        port = int(port_text)
        if not 1 <= port <= 65535:
            raise ValueError
    except ValueError:
        print("Port must be a number from 1 to 65535.")
        return

    try:
        with socket.create_connection((host, port), timeout=5):
            print(f"Result : {host}:{port} is reachable.")
            print("Status : TCP connection successful")
    except socket.timeout:
        print(f"Result : Connection to {host}:{port} timed out.")
    except OSError as error:
        print(f"Result : Could not connect to {host}:{port}.")
        print(f"Details: {error}")


def generate_diagnostic_report():
    """Save a basic diagnostic report without changing network settings."""
    print("\n=== GENERATE NETWORK REPORT ===")
    report_dir = Path("reports")
    report_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = report_dir / f"network_report_{timestamp}.txt"

    lines = [
        "WINDOWS NETWORK DIAGNOSTIC REPORT",
        "=" * 40,
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"Computer : {socket.gethostname()}",
        f"OS       : {platform.platform()}",
        "",
        "NETWORK CONFIGURATION",
        "-" * 40,
    ]

    if platform.system() == "Windows":
        lines.append(run_command(["ipconfig", "/all"]))
        lines.extend(["", "DNS CACHE (summary command)", "-" * 40])
        lines.append(run_command(["ipconfig", "/displaydns"], timeout=20))
    else:
        lines.append("Detailed configuration is available only on Windows.")

    try:
        local_ip = socket.gethostbyname(socket.gethostname())
    except socket.gaierror:
        local_ip = "Could not determine local IP address."

    lines.extend(["", f"Hostname : {socket.gethostname()}", f"Local IP : {local_ip}"])
    report_path.write_text("\n".join(lines), encoding="utf-8")

    print(f"Report created: {report_path.resolve()}")
    print("Status        : Report generation completed")


def show_menu():
    """Display the main menu."""
    print("\n" + "=" * 48)
    print(" WINDOWS NETWORK & TROUBLESHOOTING LAB")
    print("=" * 48)
    print("1. View network configuration")
    print("2. Test network connectivity (Ping)")
    print("3. DNS lookup")
    print("4. Trace network route (Tracert)")
    print("5. Check TCP port")
    print("6. Generate network diagnostic report")
    print("0. Exit")
    print("=" * 48)


def main():
    """Run the interactive network troubleshooting toolkit."""
    while True:
        show_menu()
        choice = input("Select an option: ").strip()

        actions = {
            "1": show_network_configuration,
            "2": test_connectivity,
            "3": dns_lookup,
            "4": trace_route,
            "5": check_tcp_port,
            "6": generate_diagnostic_report,
        }

        if choice == "0":
            print("Exiting Network & Troubleshooting Lab. Goodbye!")
            break
        elif choice in actions:
            actions[choice]()
        else:
            print("Invalid option. Please select 0–6.")


if __name__ == "__main__":
    main()
