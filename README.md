# Distributed Scientific Calculator

A Python-based scientific calculator where the GUI runs on Windows and all math computations (trig, log, sqrt, pi, etc.) are offloaded to a Raspberry Pi 5 server over TCP sockets using sympy.

## Features
- Responsive Tkinter GUI with button press animation
- Scientific functions: sin/cos/tan, sqrt, log/ln, exponents, parentheses
- Degree/Radian mode toggle
- Remote evaluation on Raspberry Pi
- Modular server tasks (system info, primes, matrices + calculator)

## How to Run

### Server (Raspberry Pi)
```bash
cd distributed_pi_system/server
python3 -m venv venv
source venv/bin/activate
pip install sympy numpy psutil
python server.py   # or server_v2.py
