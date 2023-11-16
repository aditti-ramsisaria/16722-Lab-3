#include <Adafruit_VEML7700.h>

const int referenceSquareWavePin = 10;     // Digital pin for reference square wave output

Adafruit_VEML7700 veml = Adafruit_VEML7700();

int count = 0;

void setup() {
  Serial.begin(9600);

  if (!veml.begin()) {
    Serial.println("Sensor not found");
    while (1);
  }
}

void loop() {
  // Generate Dataset 2: Modulated square wave signal T = 4s
  // if (count == 0) {
  //   analogWrite(referenceSquareWavePin, 255);
  // }
  // else if (count == 10) {
  //   analogWrite(referenceSquareWavePin, 0);
  // }

  Serial.print(millis() / 1000.0);
  Serial.print(",");
  Serial.println(veml.readLux());

  count = (count + 1) % 20;
  // sensor reading every 100ms
  delay(100);
}
