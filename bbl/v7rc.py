import network
import uasyncio
from bbl.dgram import UDPServer

# Default built-in LED function (used when not provided by user)
def _default_set_color(r, g, b):
    try:
        from machine import Pin
        from neopixel import NeoPixel
        np = NeoPixel(Pin(8, Pin.OUT), 1)
        np[0] = (r, g, b)
        np.write()
    except:
        print("[v7rc] LED control failed (NeoPixel not available)")

# Default callback for UDP messages (used if cb is not provided)
def _default_cb(msg, addr):
    print("[v7rc] UDP received:", msg, "from", addr)

# Initialize AP and optionally start LED and UDP server
def init_ap(essid, password, cb=None, use_default_led=True, set_color=None):
    wlan = network.WLAN(network.AP_IF)
    wlan.config(essid=essid, password=password, authmode=network.AUTH_WPA_WPA2_PSK)
    wlan.active(True)
    print("[v7rc] AP started at:", wlan.ifconfig()[0])

    # Decide which set_color function to use
    if set_color is None and use_default_led:
        set_color_fn = _default_set_color
    elif set_color is not None:
        set_color_fn = set_color
    else:
        set_color_fn = None

    # Use default callback if none provided
    if cb is None:
        cb = _default_cb

    # Monitor if any station is connected and change LED color accordingly
    async def monitor_sta():
        while True:
            sta_list = wlan.status('stations')
            if set_color_fn:
                if sta_list:
                    set_color_fn(0, 255, 0)  # Green
                else:
                    set_color_fn(255, 0, 0)  # Red
            await uasyncio.sleep(1)

    # Start all services (UDP + LED monitor)
    async def start():
        tasks = []
        if cb:
            s = UDPServer()
            tasks.append(s.serve(cb, '192.168.4.1', 6188))
        tasks.append(monitor_sta())
        await uasyncio.gather(*tasks)

    return start