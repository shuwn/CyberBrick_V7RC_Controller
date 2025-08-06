# CyberBrick V7RC WiFi AP Utility

A lightweight MicroPython library for CyberBrick and ESP32-C3-based V7RC modules, enabling:

- WiFi AP (Access Point) mode setup
- UDP server communication
- Built-in LED status logic (optional and overridable)

This library simplifies the process of networking and feedback LED handling, allowing users to focus on interaction logic.

---

## Features

- Simple Access Point setup with password
- UDP message handling via callback
- Built-in LED behavior:
  - Red: No device connected
  - Green: connected
- Optional: Define your own LED behavior and UDP message callback

---

## Requirements

- Cyberbrick Core
- `neopixel` module (for LED control)
- `uasyncio` for async task handling
