# IT-Security-Projects

A collection of small tools and scripts in Python for common information-security tasks: port scanning, directory discovery, fuzzing, hash cracking, and eventually more.

---

## Table of Contents

- [About](#about)  
- [Project Structure](#project-structure)  
- [Requirements](#requirements)  
- [Installation](#installation)  
- [Usage](#usage)  
- [Important Legal Notice](#important-legal-notice)  

---

## About

This repository serves as a learning playground and reference for security tooling and techniques. Each subfolder contains a focused project intended to demonstrate a specific security concept or practice.

---

## Project Structure
(As of September 2025)

```
.
├── Port Scanner/           # Tools for scanning open ports on hosts
├── dirdiscover/            # Directory discovery / web directory brute-forcing
├── fuzzer/                 # Simple fuzzing scripts (input injection testing)
├── hash_crack/             # Hash cracking tools or dictionary attacks
└── README.md
```

---

## Requirements

- Python 3.8+ (or your preferred Python 3.x)  

Install dependencies (if provided):

```bash
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/ZAMathis/IT-Security-Projects.git
cd IT-Security-Projects
```

Optionally create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate   # macOS / Linux
.venv\Scripts\activate      # Windows (PowerShell)
```

---

## Usage

Each script has different flags and inputs. Typical workflow:

1. Change into the tool folder you want to run, for example:

   ```bash
   cd "Port Scanner"
   ```

2. Inspect the script header or run `--help`:

   ```bash
   python3 port_scanner.py --help
   ```

3. Example usage (replace with actual script names and flags in the repo):

   ```bash
   # Port scanner example
   python3 port_scanner.py --target 192.168.1.10 --ports 1-1024

   # Directory discovery example
   python3 dirdiscover.py --url https://example.com --wordlist wordlist.txt

   # Fuzzer example
   WIP

   # Hash cracker (dictionary attack)
   python3 hash_crack.py --file hashes.txt OR --target verylonghash1234 --wordlist passwords.txt --hashtype md5
   ```

---

## Important Legal Notice

**Do not** use these tools on networks, systems, or services you do not own or do not have explicit written permission to test. Unauthorized scanning, fuzzing, or cracking can be illegal and may result in civil or criminal penalties. Use these projects responsibly and for educational / authorized testing only.

---
