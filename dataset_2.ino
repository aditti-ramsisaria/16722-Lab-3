#include <Adafruit_VEML7700.h>

Adafruit_VEML7700 veml = Adafruit_VEML7700();

const int squareWavePin = 9;               // Digital pin for modulated square wave output
const int referenceSquareWavePin = 10;     // Digital pin for reference square wave output
const int flickerLED1 = 6;
const int flickerLED2 = 7;
int count = 0;

void setup() {
  pinMode(squareWavePin, OUTPUT);
  pinMode(referenceSquareWavePin, OUTPUT);
  pinMode(flickerLED1, OUTPUT);
  pinMode(flickerLED2, OUTPUT);
  Serial.begin(9600);

  if (!veml.begin()) {
    Serial.println("Sensor not found");
    while (1);
  }
}

void loop() {
  // Generate Noise Signal at random counts
   simulateFlickeringNoise();
  
  // Generate Dataset 2: Modulated square wave signal T = 4s
  if (count == 0) {
    analogWrite(referenceSquareWavePin, 255);
  }
  else if (count == 10) {
    analogWrite(referenceSquareWavePin, 0);
  }

  Serial.print(millis() / 1000.0);
  Serial.print(",");
  Serial.println(veml.readLux());

  count = (count + 1) % 20;
  // sensor reading every 100ms
  delay(100);
}

void simulateFlickeringNoise() {
  // Randomly toggle flickering LEDs for noise
  if (random(100) < 5) {  // Adjust the threshold for flickering frequency
    digitalWrite(flickerLED1, HIGH);
  } else {
    digitalWrite(flickerLED1, LOW);
  }

  if (random(100) < 5) {  // Adjust the threshold for flickering frequency
    digitalWrite(flickerLED2, HIGH);
  } else {
    digitalWrite(flickerLED2, LOW);
  }
}
