# CyberBrick V7RC WiFi AP Utility

## What is V7RC?

**V7RC** is a mobile app (available on iOS App Store and Google Play) created by Ameba (嵐奕科技有限公司) that allows users to control RC devices such as cars, tanks, bulldozers, and even quadcopters via Bluetooth, Wi-Fi, or micro:bit integration. It offers two user interface options:

- 2-channel UI for RC cars
- 4-channel UI for tanks, bulldozers, and similar devices

The V7RC App is available for free download on both [iOS](https://apps.apple.com/tw/app/v7rc/id1390983964) and [Android](https://play.google.com/store/apps/details?id=com.v7idea.v7rcliteandroidsdkversion&hl=zh_TW) app stores.

---

## Project Overview

This is a compact MicroPython library tailored for CyberBrick’s V7RC module (ESP32-C3) that simplifies:

- Wi‑Fi AP (Access Point) mode setup with custom SSID and password
- Lightweight UDP server listening on `192.168.4.1:6188`
- Built-in NeoPixel LED feedback (red for no clients, green for presence)
- Optional override for LED behavior and UDP callback
- Asynchronous design using `uasynci`

## Features

- Easy Wi‑Fi AP setup
- UDP callback mechanism with default handler
- Default LED status indicator (can be customized)
- Non-blocking, async-friendly using `uasyncio`
- Minimal dependency footprint for MicroPython on CyberBrick Core

## Installation

Copy the following files into your CyberBrick device:

```shell
/app/main.py
/bbl/v7rc.py
/bbl/dgram.py # UDP support module
/bbl/neopixel.py # RGB LED control
```

The NeoPixel LED will automatically indicate connection status:

- Red — no devices connected
- Green — at least one device connected

## About ESP-NOW

While this library uses UDP over Wi‑Fi, V7RC modules also support ESP-NOW, a low-latency wireless protocol ideal for real‑time control tasks. You can integrate with the CyberBrick_ESPNOW project for hybrid control setups.

## License & Credits

This library uses the CyberBrick Codebase License (refer to LICENSE in the repo).
Special thanks to Mason Chen for contributing valuable design ideas.
