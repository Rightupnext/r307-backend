# Fingerprint System README

## Project Overview

This project implements a biometric fingerprint verification system using **Raspberry Pi** as the central server. The Raspberry Pi communicates with multiple client devices over LAN and triggers specific fingerprint sensors connected to USB ports.

### Key Features

* Raspberry Pi acts as a **Fingerprint Server**
* Server IP: **192.168.1.48**
* Multiple client devices send fingerprint scan requests via API

  * Client 1 → 192.168.1.44
  * Client 2 → 192.168.1.45
  * Client 3 → 192.168.1.46
  * Client 4 → 192.168.1.47
* Each Raspberry Pi USB port assigned to a specific client

  * `USB PORT 0` ↔ Client 192.168.1.44
  * `USB PORT 1` ↔ Client 192.168.1.45
  * `USB PORT 2` ↔ Client 192.168.1.46
  * `USB PORT 3` ↔ Client 192.168.1.47
* Each API request triggers corresponding port to capture/verify fingerprint

---

## Architecture

```
Multiple Client Devices ---> Sends API request ---> Raspberry Pi Server
                                       |
                                 USB Fingerprint Sensors
```

### Flow

1. Client device calls API with `port` parameter
2. Raspberry Pi selects corresponding `/dev/ttyUSBx`
3. Fingerprint scanner reads & verifies
4. Response returned to client

---

## Installation Guide (Raspberry Pi)

### 1. Update & Install Dependencies

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install git python3-pip -y
```

### 2. Install Miniconda & Create Environment

```bash
conda create --name Army python=3.10
conda activate Army
```

### 3. Clone Project & Install Requirements

```bash
git clone <your-repo-url>
cd <project-folder>
pip install -r requirements.txt
```

### 4. Run Application

```bash
conda activate Army
python app.py
```

---

## API Usage

### Verify Fingerprint

```
POST http://192.168.1.48:5000/api/finger/verify?port=0
```

### Example

* Device 192.168.1.44 → calls:

```
/api/finger/verify?port=0
```

* Device 192.168.1.45 → calls:

```
/api/finger/verify?port=1
```

---

## Notes

* Ensure all client devices are on same LAN
* Use static IP or DHCP reservation for network stability
* USB mapping must match correct sensor slots

---

## Electronics Connectivity Diagram

Below is the hardware connection diagram for Raspberry Pi to Fingerprint Sensors:

```
<h3>R307S Fingerprint Sensor Image:</h3>
<img src="assets/r307s_scanner.png" alt="R307S Scanner" />

<h3>R307S Pin Diagram:</h3>
<img src="assets/R307s_module.png" alt="R307S Module" />

<h3>USB to TTL CP2102 Module Image:</h3>
<img src="assets/CP2102-Pinout.jpg" alt="CP2102 Module" />

<h3>Raspberry Pi 4 Device Image:</h3>
<img src="assets/rasberryPi.png" alt="Raspberry Pi" />




```
Below is a complete **systemd service setup** for your Flask backend located at:

```
/home/siva/Army-backend/app.py
```

With `.env` file placed in:

```
/home/siva/Army-backend/.env
```

---

## ✅ 1. Create the service file

Run:

```bash
sudo nano /etc/systemd/system/army.service
```

Paste this:

```ini
[Unit]
Description=Army Backend Service
After=network.target

[Service]
User=siva
WorkingDirectory=/home/siva/Army-backend

# Load environment variables from .env file
EnvironmentFile=/home/siva/Army-backend/.env

# Activate your Python environment if you use one (edit the path)
ExecStart=/home/siva/miniconda3/envs/army/bin/python app.py

Restart=always
RestartSec=5

# Logging
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=army-backend

[Install]
WantedBy=multi-user.target
```

> ⚠️ **If not using Conda**, change `ExecStart` to your python path:

Example for system python:

```ini
ExecStart=/usr/bin/python3 app.py
```

---

## ✅ 2. Reload systemd

```bash
sudo systemctl daemon-reload
```

---

## ✅ 3. Start service

```bash
sudo systemctl start army.service
```

---

## ✅ 4. Enable auto-start on boot

```bash
sudo systemctl enable army.service
```

---

## ✅ 5. Stop service

```bash
sudo systemctl stop army.service
```

---

## ✅ 6. Restart service

```bash
sudo systemctl restart army.service
```

---

## ✅ 7. Check status

```bash
sudo systemctl status army.service
```

---

## ✅ 8. View logs

```bash
journalctl -u army.service -f
```

---

## ⚠️ Important Notes

| Thing            | Meaning                          |
| ---------------- | -------------------------------- |
| `.env`           | Auto-loaded into service         |
| WorkingDirectory | must point to backend folder     |
| ExecStart        | must point to Python interpreter |

---

## ✅ Test .env loaded

Add inside `.env`:

```
APP_ENV=production
```

Inside `app.py` print:

```python
import os
print("Loaded ENV:", os.getenv("APP_ENV"))
```

Run:

```bash
sudo systemctl restart army.service
journalctl -u army.service -n 20
```

You should see:

```
Loaded ENV: production
```

---

### Done 🎯

Your service will now auto-start, run with `.env`, and support start/stop/restart.

---

### Want auto-reload when you update code?

Tell me and I will give you **systemd + watchdog** or **gunicorn + flask** setup.

---

## Contact

For setup help or improvement requests, please contact the project maintainer.
