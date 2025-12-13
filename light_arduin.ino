// -------- Pin config --------
const int LED_PIN = 8;

char command;

void setup() {
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);

  Serial.begin(9600);
  Serial.println("Arduino ready");
}

void loop() {
  if (Serial.available() > 0) {
    command = Serial.read();

    if (command == '1') {
      digitalWrite(LED_PIN, HIGH);
      Serial.println("LED ON");
    }
    else if (command == '0') {
      digitalWrite(LED_PIN, LOW);
      Serial.println("LED OFF");
    }
  }
}
