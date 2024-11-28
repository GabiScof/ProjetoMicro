#include <FastLED.h>

#define NUM_LEDS  46
#define LED_PIN   8

// CHSV(hue, saturation, value);

CRGB leds[NUM_LEDS];
float hue_val; 
float brightness_val; 
unsigned long lastMillis = 0;  // Store the last time LEDs changed
bool isOn = true;  // State to check whether LEDs are on or off

void setup() {
  Serial.begin(9600);

  FastLED.addLeds<WS2812B, LED_PIN, GRB>(leds, NUM_LEDS);
  fill_solid(leds, NUM_LEDS, CRGB::Black);
  FastLED.setBrightness(20);
}

void loop() {
  unsigned long currentMillis = millis();

  if (Serial.available() > 0) {
    String texto = Serial.readStringUntil('\n');
    texto.trim(); // remove quebra de linha

    if (texto.startsWith("hue")) {
      texto = texto.substring(4);  // Start from the 5th character (after "hue ")
      hue_val = texto.toInt();
    }
    else if (texto.startsWith("brightness")) {
      texto = texto.substring(11);  // Start from the 12th character (after "brightness ")
      brightness_val = texto.toInt();
      FastLED.setBrightness(brightness_val);
    }
    else if (texto.startsWith("batida")) {
      isOn = !isOn;
    }
  }

  if (isOn) {
    for (int i = 0; i < NUM_LEDS; i++) {
    leds[i] = CHSV(hue_val, 255, 255);
    }
  }
  else {
    fill_solid(leds, NUM_LEDS, CRGB::Black);
  }

  FastLED.show();
}

  // EVERY_N_MILLISECONDS(state_time*1000) {
  //   index = (index + 1)%size;
  //   hue_val = hue[index];
  //   brightness_val = brightness[index];

  //   FastLED.setBrightness(brightness_val);
  // }
  
  // // Check if it's time to change the LED state (blink)
  // if (currentMillis - lastMillis >= blinkInterval) {
  //   Serial.println(blinkInterval);
  //   lastMillis = currentMillis;  // Reset the lastMillis time

  //   // Toggle the LED state
  //   isOn = !isOn;
  // }


  // Individual LEDs
  // leds[0] = CRGB::Red;
  // leds[1] = CRGB::Green;
  // leds[2] = CRGB::Blue;
  // leds[3] = CRGB::Magenta;

  // All LEDs
  // fill_solid(leds, NUM_LEDS, CRGB::Magenta);
  // FastLED.show();
  // delay(500);

  // fill_gradient_RGB(leds, NUM_LEDS, CRGB::Red, CRGB::Yellow, CRGB::Green, CRGB::Blue);
  // FastLED.show();
  // delay(500);

  // for (int i = 0; i < NUM_LEDS; i++) {
  //   leds[i] = CHSV(hue, 255, 255);
  // }