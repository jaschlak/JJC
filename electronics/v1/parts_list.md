# v1 Parts List

| Item | Qty | Description | Suggested Part | Purchase Link | Notes |
|------|-----|-------------|----------------|---------------|-------|
| Microcontroller | 1 | Programmable embedded board | ESP32 dev board, Gold Edition, Type-C | https://www.amazon.com/dp/B0FRXZD6VC | Compatible with Arduino IDE, MicroPython, and ESP-IDF |
| LED strip | 1 roll | Addressable RGB LEDs for prototyping | WS2812B 5m strip, 300 LEDs | https://www.amazon.com/dp/B097BWJGYK | Cut or connect only a short section for initial tests |
| Power | 1 | 5V power source | 5V USB or bench power supply | https://www.amazon.com/s?k=5v+usb+power+supply | Size the supply for the LED count; share ground with ESP32 |
| Bulk capacitor | 1 pack | Power smoothing | ALLECIN 1000 uF 10V electrolytic capacitor pack | https://www.amazon.com/dp/B0CMQCC5D3 | Use one capacitor per LED power input; observe polarity |
| Series resistor | 1 kit | Data line protection | BOJACK 1/4W resistor assortment with 330 ohm values | https://www.amazon.com/dp/B08FD1XVL6 | Use one 330 ohm resistor per LED data line |
| Logic level shifter | 1 | Data signal reliability | 74AHCT125 / SN74AHCT125 3.3V-to-5V level shifter | https://www.adafruit.com/product/1787 | Recommended for WS2812B when using ESP32 3.3V data |
| Data wire | 1 kit | Signal and power wiring | 22 AWG silicone wire, multiple colors | https://www.amazon.com/s?k=22+awg+silicone+wire | Flexible and solderable |
| Connectors | 1 pack | Optional USB 5V/GND power access | Jienk 22 AWG USB-A male 2-pin power pigtail, 5 pack | https://www.amazon.com/dp/B0CRQTYV9H | Optional for bench setup; use only 5V and GND |
| Soldering | 1 kit | Tools | Soldering iron and solder | https://www.amazon.com/s?k=soldering+iron+kit | Required if you do not already have soldering tools |
| Insulation | 1 kit | Wire protection | Ginsco 580-piece 2:1 heat shrink tubing kit | https://www.amazon.com/dp/B01MFA3OFA | Protects solder joints; assorted sizes are useful for wire and connector joints |
| Optional | 1 kit | Button input | 120-piece 12x12x7.3 mm momentary tactile button kit with caps | https://www.amazon.com/dp/B0G2CRKZ4G | Later for manual color change; use one button for the first prototype |
| Optional | 1 pack | Motion sensor | KEAcvise 6-pack GY-521 MPU6050 6-axis accelerometer/gyroscope modules | https://www.amazon.com/dp/B0F9DLNHTB | Future motion detection prototype; uses one I2C module and keeps spares |

## Power Notes

The 5m WS2812B strip has 300 LEDs. At full white and full brightness, that can draw far more current than a computer USB port or small USB wall adapter can safely supply.

For first tests:

- Cut or connect only a short section, such as 8-16 LEDs.
- Keep brightness low in software.
- Power the LEDs from a 5V supply sized for the LED count.
- Always connect ESP32 GND and LED power supply GND together.
