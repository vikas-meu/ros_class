int ledPin = 8;
char command;

void setup() {
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);
  Serial.begin(9600);
}

void loop() {
  if (Serial.available()) {
    command = Serial.read();

    if (command == '1') {   // Thumbs UP
      digitalWrite(ledPin, HIGH);
    }
    else if (command == '0') { // Thumbs DOWN
      digitalWrite(ledPin, LOW);
    }
  }
}
