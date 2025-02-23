# MasterEye - IP Scanner

![MasterEye Screenshot](./MasterEye.png)  
*A powerful multi-threaded IP scanner with port scanning, credential testing, and a user-friendly GUI.*

## Features
- Scan an IP range for active hosts
- Check for open ports (default: 80, 443, 8080)
- Attempt login with default credentials
- Multi-threaded scanning for speed
- Export results in CSV & JSON formats
- Dark theme support

## Installation
### Prerequisites
Ensure you have Python 3 installed. You can check by running:
```sh
python --version
```
# Install Dependencies
```sh
pip install -r requirements.txt
```
# Running the Application
```sh
python mastereye.py
```
# To install all the required dependencies for your project, run the following command in your terminal:
```sh
pip install -r requirements.txt
```
## Usage
1. Enter an IP range (e.g., `192.168.1.1-192.168.1.255`).
2. Click **Start Scan** to begin scanning.
3. View live scan results in the table.
4. Export results to **CSV** or **JSON**.
5. Toggle **dark mode** in the settings menu.

