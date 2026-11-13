# Windows Network & Troubleshooting Lab

A beginner-friendly Python project for practicing Windows network diagnostics. It is designed for an IT Support / IT Helpdesk portfolio.

## Features

1. View detailed network configuration with `ipconfig /all`.
2. Test basic connectivity with `ping`.
3. Resolve hostnames using Python DNS lookup (`socket.getaddrinfo`).
4. Trace a route with Windows `tracert`.
5. Test whether a TCP port is reachable.
6. Generate a timestamped network diagnostic report in a local `reports` folder.

## Requirements

- Python 3.10 or newer
- Windows 10 or Windows 11 for all menu features
- No third-party Python packages

## Run the project

Open PowerShell in this folder and run:

```powershell
python windows_network_troubleshooting_lab.py
```

## Safety and privacy

- The project performs diagnostic/read-only checks. It does not change IP settings, renew DHCP leases, modify DNS settings, or configure a router.
- Use only hosts and ports you are authorized to test.
- Network reports may contain private information such as local IP addresses, MAC addresses, DNS servers, and adapter details. Review reports before sharing them publicly. Do not upload real diagnostic reports to GitHub.

## Learning outcomes

- Understand IP configuration, DNS resolution, ping, traceroute, and TCP ports.
- Practice Python's `socket`, `subprocess`, `pathlib`, and `datetime` modules.
- Create a simple network troubleshooting workflow and diagnostic report.
