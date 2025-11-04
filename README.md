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
R307S Fingerprint Sensor Image:
assets/images/r307s_scanner.png

R307S Pin Diagram:
assets/images/r307s_pin_diagram.png

USB to TTL CP2102 Module Image:
assets/images/cp2102_module.png

Raspberry Pi 4 Device Image:
assets/images/raspberrypi4_device.png

Complete Fingerprint Connectivity Diagram:
assets/images/fingerprint_connection_diagram.png
```

---

## Contact

For setup help or improvement requests, please contact the project maintainer.
