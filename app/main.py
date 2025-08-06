import uasyncio
import bbl.v7rc as v7rc

# V7rc initialization with custom ESSID and password
# You can also provide a custom callback function for UDP messages
start = v7rc.init_ap(
    essid='cyber_car',
    password='12341234',
    use_default_led=True
)

uasyncio.run(start())