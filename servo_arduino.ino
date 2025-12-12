#include <Servo.h>

Servo myServo;
int angle = 90;

void setup() {
  Serial.begin(9600);
  myServo.attach(9);    
  myServo.write(angle);
}

void loop() {
  if (Serial.available()) {
    angle = Serial.parseInt();
    angle = constrain(angle, 0, 180);
    myServo.write(angle);
  }
}
