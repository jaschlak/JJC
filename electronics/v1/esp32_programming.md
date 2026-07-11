# ESP32 Programming Guide

This guide assumes you will use the Arduino IDE, Arduino-compatible tooling, or MicroPython to program the ESP32.

## 1. Install ESP32 Arduino Support

1. Open the Arduino IDE.
2. Go to `File > Preferences`.
3. In `Additional Boards Manager URLs`, add:
   - `https://espressif.github.io/arduino-esp32/package_esp32_index.json`
4. Open `Tools > Board > Boards Manager`.
5. Search for `esp32` and install the `esp32` package by Espressif.

## 2. Choose The Board

1. Go to `Tools > Board` and choose your ESP32 model.
2. Set the correct port under `Tools > Port`.
3. Set `Upload Speed` to `921600` or `115200` if needed.

## 3. Install FastLED

1. Open `Sketch > Include Library > Manage Libraries`.
2. Search for `FastLED`.
3. Install the FastLED library by Daniel Garcia and Mark Kriegsman.

## 4. Basic ESP32 Test Sketch

Create a new sketch and paste:

```cpp
#include <FastLED.h>

#define LED_PIN 5
#define NUM_LEDS 12
#define BRIGHTNESS 80
#define LED_TYPE WS2812B
#define COLOR_ORDER GRB

CRGB leds[NUM_LEDS];

void setup() {
  FastLED.addLeds<LED_TYPE, LED_PIN, COLOR_ORDER>(leds, NUM_LEDS).setCorrection(TypicalLEDStrip);
  FastLED.setBrightness(BRIGHTNESS);
}

void loop() {
  fill_rainbow(leds, NUM_LEDS, millis() / 20, 7);
  FastLED.show();
  delay(20);
}
```

- `LED_PIN` should match the GPIO pin wired to the data line.
- `NUM_LEDS` should match the number of LEDs connected.
- Keep `BRIGHTNESS` low for USB-powered tests.

## 5. Uploading The Sketch

1. Connect the ESP32 to your PC with USB.
2. Select the correct board and COM port.
3. Click upload.
4. Watch the output console for `Connecting...` and `Done uploading`.

## 6. Troubleshooting

If the LEDs do not light:

- Verify the strip is powered with 5V.
- Confirm ground is shared with ESP32.
- Confirm `LED_PIN` matches the chosen GPIO.
- Confirm strip data direction is correct.
- Try a lower LED count and lower brightness.
- Add the level shifter, 330 ohm resistor, and 1000 uF capacitor if they are not already installed.

## 7. Color Cycle With Button Support

Use this script after the basic test works. GPIO 14 is used for the button to avoid ESP32 boot strap pins such as GPIO 0.

```cpp
#include <FastLED.h>

#define LED_PIN 5
#define NUM_LEDS 12
#define BRIGHTNESS 80
#define BUTTON_PIN 14
#define LED_TYPE WS2812B
#define COLOR_ORDER GRB

CRGB leds[NUM_LEDS];
int currentMode = 0;

void setup() {
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  FastLED.addLeds<LED_TYPE, LED_PIN, COLOR_ORDER>(leds, NUM_LEDS).setCorrection(TypicalLEDStrip);
  FastLED.setBrightness(BRIGHTNESS);
}

void loop() {
  static bool previousPressed = false;
  bool pressed = digitalRead(BUTTON_PIN) == LOW;

  if (pressed && !previousPressed) {
    currentMode = (currentMode + 1) % 3;
    delay(40);
  }
  previousPressed = pressed;

  switch (currentMode) {
    case 0:
      rainbowCycle();
      break;
    case 1:
      meteorRain(CRGB::Blue);
      break;
    case 2:
      colorWipe(CRGB::Red);
      break;
  }

  FastLED.show();
  delay(20);
}

void rainbowCycle() {
  fill_rainbow(leds, NUM_LEDS, millis() / 20, 7);
}

void meteorRain(const CRGB& color) {
  fadeToBlackBy(leds, NUM_LEDS, 64);
  int index = (millis() / 40) % NUM_LEDS;
  leds[index] = color;
}

void colorWipe(const CRGB& color) {
  static int index = 0;
  fadeToBlackBy(leds, NUM_LEDS, 24);
  leds[index] = color;
  index = (index + 1) % NUM_LEDS;
}
```

## 8. MicroPython Quickstart

If you prefer MicroPython, the ESP32 runs it well.

### Flash MicroPython Firmware

1. Download the current stable MicroPython ESP32 `.bin` from https://micropython.org/download/esp32/.
2. Install `esptool.py`:

```bash
python -m pip install esptool
```

3. Erase the board and write the firmware, replacing the COM port and file name:

```bash
esptool.py --port COM3 erase_flash
esptool.py --chip esp32 --port COM3 write_flash -z 0x1000 esp32-202*.bin
```

### Upload A NeoPixel Test

Install `ampy`:

```bash
python -m pip install adafruit-ampy
```

Create a file named `main.py` with this content:

```python
import machine
import neopixel
import time

NUM_LEDS = 12
DATA_PIN = 5
BRIGHTNESS = 0.25

pin = machine.Pin(DATA_PIN, machine.Pin.OUT)
np = neopixel.NeoPixel(pin, NUM_LEDS)

def scale(color):
    return tuple(int(channel * BRIGHTNESS) for channel in color)

def wheel(pos):
    pos = 255 - pos
    if pos < 85:
        return scale((255 - pos * 3, 0, pos * 3))
    if pos < 170:
        pos -= 85
        return scale((0, pos * 3, 255 - pos * 3))
    pos -= 170
    return scale((pos * 3, 255 - pos * 3, 0))

def rainbow_cycle():
    for j in range(255):
        for i in range(NUM_LEDS):
            pixel_index = (i * 256 // NUM_LEDS) + j
            np[i] = wheel(pixel_index & 255)
        np.write()
        time.sleep_ms(20)

while True:
    rainbow_cycle()
```

Upload it with `ampy`:

```bash
ampy --port COM3 put main.py
```

When the board boots it will run `main.py` and the LEDs should cycle.

## Notes

- Use a common ground between the ESP32 and the LED strip.
- If the strip is powered from 5V, use a logic level shifter for maximum reliability.
- Keep brightness low and use only a short LED section for USB-powered tests.
- For interactive REPL, use PuTTY on Windows or `screen` on Linux/macOS at 115200 baud.
