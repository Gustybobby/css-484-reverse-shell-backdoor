# Backdoor

> **NOTICE - AUTHORIZED USE ONLY:** This repository is intended **only** for authorized security research, defensive testing, or academic study within a controlled, consented environment. Do **not** deploy or use these materials on systems you do not own or have explicit permission to test. The authors are not responsible for misuse.

## Overview
This repository contains proof-of-concept components developed for academic/security-research purposes. The components demonstrate a set of features commonly discussed in defensive/security analysis:

- Key capture (research/demo only)
- Privilege escalation demonstration (non-exploitative, educational)
- Screen recording (instrumentation for UI testing / analysis)
- Persistence behavior modeling (for defensive study of persistence mechanisms)

> All components are included for analysis, detection testing, and defensive tool development. They are **not** intended for unauthorized use.

## Pre-conditions / Required Environment
These materials assume you will run them in a controlled lab environment (for example: isolated virtual machines, air-gapped or host-only networks) and only with explicit authorization.

Recommended environment characteristics:
- Use disposable or snapshot-capable virtual machines (VMs).
- Use separate host and target VMs (e.g., attacker / victim) inside an isolated network.
- Ensure network isolation and no connectivity to production or the public internet.
- Maintain clear consent and written authorization for any testing.

## Setup Guide

This guide shows how to prepare two lab VMs and start the server component. It assumes both VMs are under your control and on an isolated/test network.

### Requirements

- Two VMs: `kali` and `windows-10`
- `git` installed on both VMs (Windows need Git for Windows)
- Python 3 and `pip` on the Kali VM
- VM (VirtualBox, VMware, etc.) with ability to create an isolated subnet

### Network / Connectivity

1. Place both VMs on the same isolated subnet so they can reach each other.

- Example network used in this repository: `192.168.100.0/24`
- If using VirtualBox, create a NAT or host-only network with that subnet (or choose another subnet and update `/lib/config.py` accordingly).

2. Example addressing used in tests:

- `kali` (analysis/host) → `192.168.100.4`
- `windows-10` (target/server) → `192.168.100.5`

3. Test connectivity by pinging each machine from the other:

From Kali:
```bash
ping 192.168.100.5
```

From Windows (PowerShell / cmd):
```bash
ping 192.168.100.4
```

If both pings succeed, network connectivity is OK.

### Repository

Clone this repository into both VMs for ease of reproduction:

```bash
git clone https://github.com/Gustybobby/css-484-reverse-shell-backdoor.git
cd css-484-reverse-shell-backdoor
```
> On Windows, install Git if it is not already present.

### Kali - Python environment & dependencies

From the repository root on the Kali VM:

1. Create and activate a virtual environment:
```bash
pip install virtualenv          # only if virtualenv isn't installed
virtualenv .venv
source .venv/bin/activate
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Install gnome-terminal
```bash
sudo apt update
sudo apt install gnome-terminal
```

4. Setup EOP payload

Put `/dist/itr_client.exe` into `ITR_CLIENT_FILEPATH`. The default filepath is `/home/kali/files/itr_client.exe`.

### Configure IPs (if needed)

Update the configuration file to reflect the lab IP addresses you chose:
```
/lib/config.py
```
Change the host/peer addresses as appropriate for your isolated network.

### Start the server

Make the server script executable and run it:
```bash
chmod +x ./server.sh
./server.sh
```
The script open 4 terminal windows.

### Windows 10 - Backdoor payload and vulnerable installer

From the repository, put `all_client.exe`, `npp.exe` into some directory then run `all_client.exe`.

## Keylogger

1. After running `all_client.exe`, the executable set reverse shell back to the terminal. Run the following command to start the keylogger:
```bash
keylogger [start]
```

![keylogger step 1](https://github.com/Gustybobby/css-484-reverse-shell-backdoor/blob/bd12c64e083e6e1d8ddaeef938736a0294d684a0/assets/keylogger/step1.jpg)

2. Try typing something on windows 10, run the following command to get the keylogs
```bash
keylogger [get]
```

![keylogger step 2](https://github.com/Gustybobby/css-484-reverse-shell-backdoor/blob/bd12c64e083e6e1d8ddaeef938736a0294d684a0/assets/keylogger/step2.jpg)

## Escalation of Privilege

1. After running `all_client.exe`, the executable set reverse shell back to the terminal.

![eop step 1](https://github.com/Gustybobby/css-484-reverse-shell-backdoor/blob/bd12c64e083e6e1d8ddaeef938736a0294d684a0/assets/eop/step1.jpg)

2. The server will keep polling `tasklist` command and search for process with substring `npp`

![eop step 2](https://github.com/Gustybobby/css-484-reverse-shell-backdoor/blob/bd12c64e083e6e1d8ddaeef938736a0294d684a0/assets/eop/step2.jpg)

3. Open `npp.exe`, the server will find the process and send `itr_client.exe` renamed as `regsvr32.exe` into the same directory as `npp.exe`

![eop step 3](https://github.com/Gustybobby/css-484-reverse-shell-backdoor/blob/bd12c64e083e6e1d8ddaeef938736a0294d684a0/assets/eop/step3.jpg)

4. Complete the installation process, `regsvr32.exe` will run with elevated permission, setting up an escalated reverse shell back to another server.

![eop step 4](https://github.com/Gustybobby/css-484-reverse-shell-backdoor/blob/bd12c64e083e6e1d8ddaeef938736a0294d684a0/assets/eop/step4.jpg)

## Persistence

1. Following escalation of privilege from the last section `itr_client.exe` setup an admin reverse shell back to the server.

2. The server then executes `sc create <service_name> binPath= <exe_path> start= auto`. This persists the executable into a service that runs on startup.

![persist step 1](https://github.com/Gustybobby/css-484-reverse-shell-backdoor/blob/bd12c64e083e6e1d8ddaeef938736a0294d684a0/assets/persist/step1.jpg)

3. Try restarting the kali server and restart your windows machine. You should see reverse shell connection to the server with `nt authority/system`.

![persist step 2](https://github.com/Gustybobby/css-484-reverse-shell-backdoor/blob/bd12c64e083e6e1d8ddaeef938736a0294d684a0/assets/persist/step2.jpg)

## Recording

1. Nothing to explain much here. You will see the screen recording right away.

![recording step 1](https://github.com/Gustybobby/css-484-reverse-shell-backdoor/blob/bd12c64e083e6e1d8ddaeef938736a0294d684a0/assets/vca/recording.png)




