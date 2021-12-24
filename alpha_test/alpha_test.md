# Alpha Test

## Abstract

In the present test concept, the test procedure for acceptance and, if necessary, adaptations for the use of the Game are described and concrete test cases for checking the functionalities are formulated.

## Test team

The test teams are made up of all 6 Team Member. Their tasks are as follows:

- Carrying out the test cases and

- Documentation of errors in the error list.

## Test preparation

The following points need to be prepared before testing can begin:

- Provision and configuration of the hardware (Playing field to be completed, Sensors and actuators calibrated)

- Preparation of the software for correct data collection (see "Parameters to collect and analyse")

- Provision of the test documents for test documentation

### Parameters to collect and analyse

*Turrets control*
1. seat
2. joystick_position from game console
3. joystick_position calculated
4. servo_position (in degree)

*Blaster control*
1. seat
2. shoot_led state
3. points_led state
4. score
5. magazine
6. sensor state

*Central tower*
1. upper stepper position set (in degree)
2. side stepper position set  (in degree)
3. side stepper position from encoder
4. speed upper stepper  (in RPM)
5. speed side stepper  (in RPM)

*Display*
1. score Team A
2. score Team B
3. state of display

*State mashine*
1. current state of game


## Procedure and test sequence

By playing 5 rounds of the game, possible errors in software are to be discovered. If one of the players notices an error, he will write it down in an error list. The data of game modules is automatically written to .csv files.

## Test Evaluation

