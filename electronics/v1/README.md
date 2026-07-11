# Electronics Prototype v1

**Compatibility:** ESP32 dev board, 5V WS2812B-style addressable LEDs, and bench power testing.

## Focus

- Learn how to solder and wire NeoPixel-style LEDs
- Control LED colors from code using a small embedded board
- Prototype basic light behavior before designing final club integration
- Start with electronics similar to what the final product may use

## Suggested Parts

1. **Microcontroller**
   - Preferred: ESP32 dev board with USB-C if possible
   - Reason: built-in Wi-Fi/Bluetooth, more memory, and a stronger path to future app control or sync features
2. **LED strip**
   - WS2812B NeoPixel-style strip, individually addressable RGB LEDs
   - Choose a short section for prototyping, such as 8-16 LEDs
3. **Power**
   - 5V USB power supply or 5V bench supply
   - For ESP32, power the board from 5V VIN or a regulated 5V source and share ground with the LEDs
4. **Reliability parts**
   - 1000 uF electrolytic capacitor across LED 5V and GND
   - 330 ohm resistor in series with the LED data line
   - 3.3V-to-5V logic level shifter for the WS2812B data line
5. **Assembly supplies**
   - Soldering iron and solder
   - Heat shrink tubing
   - Silicone wire or jumper wires

## Purchase Links

- Microcontroller: https://www.amazon.com/dp/B0FRXZD6VC
- LED strip: https://www.amazon.com/dp/B097BWJGYK
- 5V power: https://www.amazon.com/s?k=5v+usb+power+supply

## Power Safety

Do not power a full 300-LED strip at high brightness from the ESP32 or a normal computer USB port.

For first tests:

- Use only a short LED section.
- Keep brightness low in software.
- Use a 5V supply sized for the number of LEDs connected.
- Always connect ESP32 GND and LED power supply GND together.

## Notes

- Keep the first prototype simple: code-driven colors only.
- The controller should be small enough to fit inside a club later.
- Later versions can add motion sensing, timing, sync, and button control.
