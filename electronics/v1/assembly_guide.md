# ESP32 Electronics Assembly Guide

This guide shows how to assemble the ESP32-based LED prototype once your parts arrive.
It is written for the parts in `electronics/v1/parts_list.md`.

Reference diagram:

```text
electronics/v1/wiring_diagram_basic_led_test.svg
```

## 1. Check Your Parts

- ESP32 dev board
- WS2812B NeoPixel-style strip, starting with 8-16 LEDs
- 5V power supply sized for the number of LEDs connected
- 22 AWG silicone wire or jumper wires
- Logic level shifter, 3.3V to 5V, for the LED data line
- 1000 uF capacitor, 10V or higher
- 330 ohm resistor
- Optional: small tactile button, motion sensor
- Soldering tools, heat shrink tubing, multimeter

## 2. Prepare The LED Strip

- Cut the strip to the number of LEDs you want.
- Tin the +5V, GND, and DIN pads lightly with solder.
- If the strip has a direction arrow, the arrow should point from the controller toward the LEDs.

## 3. Wiring Overview

### Required Connections

- **5V power**
  - Connect the 5V supply to the LED strip +5V pad.
  - Connect the same 5V supply to the ESP32 VIN or 5V pin, not the 3.3V pin.
- **Ground**
  - Connect LED strip GND to ESP32 GND.
  - Use a common ground for all devices.
- **Data**
  - Connect ESP32 GPIO pin to the logic level shifter input.
  - Connect the shifter output to the LED strip DIN pad.

### Recommended Protection

- Put a 1000 uF electrolytic capacitor across 5V and GND at the beginning of the LED strip.
- Add a 330 ohm resistor in series with the LED data line between the level shifter and DIN.
- Use a logic level shifter because ESP32 outputs 3.3V and the strip is powered at 5V.

### Example Pin Choices

- `DATA_PIN = 5` or another safe ESP32 GPIO
- `5V` power to VIN / 5V pin
- `GND` to GND

Confirm the raw GPIO number for your exact board before wiring.

## 4. Assembly Steps

1. Place the ESP32 board and LED strip near each other.
2. Run two power wires: one for 5V and one for GND.
3. Connect the LED strip +5V to the power rail and GND to the common ground.
4. Connect ESP32 VIN/5V to the same 5V supply.
5. Connect ESP32 GND to common ground.
6. Connect ESP32 data pin to the logic shifter input.
7. Connect the logic shifter output to LED strip DIN.
8. Add the 330 ohm resistor in series with the data output.
9. Add the 1000 uF capacitor across 5V and GND at the strip.
10. Double-check all connections before powering up.

Do not power a full 300-LED strip from the ESP32 board or a normal computer USB port. Start with a short LED section and low brightness until the 5V supply is sized for the number of LEDs connected.

## 5. Test Before Final Installation

- Use the Arduino IDE to upload the test script from `esp32_programming.md`.
- After upload, power the board and watch the LED strip.
- If nothing lights, verify:
  - 5V is present at the strip
  - Ground is common
  - Data pin is correct
  - Direction on the strip is correct

## 6. Mounting In The Club

- Keep the ESP32 and wiring away from moving parts.
- Secure the LED strip flat inside the club body where it will be visible.
- Put the board in a location where USB access is possible for later updates.
- Use heat shrink or tape to protect solder joints.

## 7. Next Steps

- Program the ESP32 with the baseline test sketch.
- Confirm the LED strip turns on and cycles colors.
- Once the test works, move to the full lighting behavior script.
