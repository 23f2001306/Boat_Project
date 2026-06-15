/*
  Water Hyacinth Collection Boat - Phase 6 Arduino Firmware

  Hardware:
  - Arduino Uno
  - HW-130 / L293D Motor Shield
  - AFMotor_R4 Library

  Motor Mapping:
  M1 = Front Left Paddle Wheel
  M2 = Front Right Paddle Wheel
  M3 = Rear Left Paddle Wheel
  M4 = Rear Right Paddle Wheel

  Serial Commands:
  F = Forward
  B = Backward
  L = Left turn using differential thrust
  R = Right turn using differential thrust
  S = Stop

  Important:
  The motor orientations below match the verified hardware direction tests.
  Do not change run directions unless the physical wiring or motor mounting changes.
*/

#include <AFMotor_R4.h>

AF_DCMotor motor1(1);
AF_DCMotor motor2(2);
AF_DCMotor motor3(3);
AF_DCMotor motor4(4);

const uint8_t DRIVE_SPEED = 200;
const uint8_t TURN_SLOW_SPEED = 100;
const uint8_t TURN_FAST_SPEED = 220;
const unsigned long SAFETY_TIMEOUT_MS = 1000;

unsigned long lastCommandTime = 0;

void setup() {
  Serial.begin(9600);
  stopAll();
  lastCommandTime = millis();
}

void loop() {
  readSerialCommands();
  runFailsafe();
}

void readSerialCommands() {
  while (Serial.available() > 0) {
    char command = Serial.read();

    switch (command) {
      case 'F':
        forward();
        lastCommandTime = millis();
        break;

      case 'B':
        backward();
        lastCommandTime = millis();
        break;

      case 'L':
        leftTurn();
        lastCommandTime = millis();
        break;

      case 'R':
        rightTurn();
        lastCommandTime = millis();
        break;

      case 'S':
        stopAll();
        lastCommandTime = millis();
        break;

      default:
        // Invalid commands are ignored by design.
        break;
    }
  }
}

void runFailsafe() {
  if (millis() - lastCommandTime > SAFETY_TIMEOUT_MS) {
    stopAll();
  }
}

void forward() {
  setAllMotorSpeeds(DRIVE_SPEED);

  motor1.run(BACKWARD);
  motor2.run(BACKWARD);
  motor3.run(FORWARD);
  motor4.run(BACKWARD);
}

void backward() {
  setAllMotorSpeeds(DRIVE_SPEED);

  motor1.run(FORWARD);
  motor2.run(FORWARD);
  motor3.run(BACKWARD);
  motor4.run(FORWARD);
}

void leftTurn() {
  /*
    Differential thrust left turn:
    - Left side paddles run slower.
    - Right side paddles run faster.
    - No motor direction is reversed.
    - All motors keep the verified forward movement directions.
  */
  motor1.setSpeed(TURN_SLOW_SPEED);
  motor3.setSpeed(TURN_SLOW_SPEED);
  motor2.setSpeed(TURN_FAST_SPEED);
  motor4.setSpeed(TURN_FAST_SPEED);

  motor1.run(BACKWARD);
  motor2.run(BACKWARD);
  motor3.run(FORWARD);
  motor4.run(BACKWARD);
}

void rightTurn() {
  /*
    Differential thrust right turn:
    - Left side paddles run faster.
    - Right side paddles run slower.
    - No motor direction is reversed.
    - All motors keep the verified forward movement directions.
  */
  motor1.setSpeed(TURN_FAST_SPEED);
  motor3.setSpeed(TURN_FAST_SPEED);
  motor2.setSpeed(TURN_SLOW_SPEED);
  motor4.setSpeed(TURN_SLOW_SPEED);

  motor1.run(BACKWARD);
  motor2.run(BACKWARD);
  motor3.run(FORWARD);
  motor4.run(BACKWARD);
}

void stopAll() {
  motor1.run(RELEASE);
  motor2.run(RELEASE);
  motor3.run(RELEASE);
  motor4.run(RELEASE);
}

void setAllMotorSpeeds(uint8_t speedValue) {
  motor1.setSpeed(speedValue);
  motor2.setSpeed(speedValue);
  motor3.setSpeed(speedValue);
  motor4.setSpeed(speedValue);
}
