# Distributed Scientific Calculator

A Python-based scientific calculator where the GUI runs on Windows and all math computations (trig, log, sqrt, pi, etc.) are offloaded to a Raspberry Pi 5 server over TCP sockets using sympy.

## Features
- Responsive Tkinter GUI with button press animation
- Scientific functions: sin/cos/tan, sqrt, log/ln, exponents, parentheses
- Degree/Radian mode toggle
- Remote evaluation on Raspberry Pi
- Modular server tasks (system info, primes, matrices + calculator)<img width="1920" height="1020" alt="faw" src="https://github.com/user-attachments/assets/82beb355-b07e-4fb0-a484-83d26631a3cd" />


## How to Run

### Server (Raspberry Pi)
```bash
cd distributed_pi_system/server
python3 -m venv venv
source venv/bin/activate
pip install sympy numpy psutil
python server.py   # or server_v2.py
<img width="1920" height="1020" alt="faw" src="https://github.com/user-attachments/assets/b8a3a734-6613-498e-bcdb-79912c2411af" />
<img width="1920" height="1020" alt="faw" src="https://github.com/user-attachments/assets/e193e2fe-3afd-408a-abb6-43d83e7bd28e" />
