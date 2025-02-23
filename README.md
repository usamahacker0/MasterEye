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
# Dependencies
The application requires the following Python libraries:

1.tkinter (GUI)
2.socket (Network communication)
3.ipaddress (IP range handling)
4.threading (Multi-threading support)
5.requests (HTTP requests for login attempts)
6.csv & json (Exporting results)
7.You can install them all using:
