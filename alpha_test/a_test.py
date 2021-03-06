#!/usr/bin/env python3

import csv
import datetime
import os.path

class _Debug:

    """
        Class to collect the values from different game module
    """

    def __init__(self):

        """
            create new csv file
        """

        self.toWrite= []
        self.read_time = datetime.datetime.fromtimestamp(1640272000).isoformat()
        self.test_number = 1

    def write_stepper(self, stepper_upper_pos:int, stepper_side_pos:int, stepper_upper_speed:int, stepper_side_speed:int,stepper_side_pos_en:int,):

        """
            Write values from central tower

            Arguments:
                stepper_upper_pos: Position of the upper stepper motor
                stepper_side_pos: Position of the side stepper motor
                stepper_side_pos_en: Position of the side stepper motor from Encoder
                stepper_upper_speed: Velocity of the upper stepper motor
                stepper_side_speed: Velocity of theside stepper motor
        """

        self.fieldnames = ['Time', 'Stepper Up', 'Stepper Side', 'Stepper Upper Speed', 'Stepper Side Speed', 'Stepper Side encoder']
        self.rows=[
            {'Time':self.read_time,'Stepper Up':stepper_upper_pos, 'Stepper Side':stepper_side_pos,
            'Stepper Upper Speed':stepper_upper_speed, 'Stepper Side Speed':stepper_side_speed, 'Stepper Side encoder':stepper_side_pos_en}
        ]
        filename = 'stepper({}).csv'.format(self.test_number)
        file = open(filename, 'a', newline='')

        with file:
            file_is_empty = os.stat(filename).st_size == 0
            writer = csv.writer(file,delimiter=',')
            writer = csv.DictWriter(file,fieldnames=self.fieldnames)

            if file_is_empty:
                writer.writeheader()

            writer.writerows(self.rows)


    def write_turrets(self,seat:int, joystick_pos:int, joystick_pos_calc:int, servo_pos:int):

        """
            Write values from turrets

            Arguments:
                seat: Controller seat
                joystick_pos: position of the joystick
                joystick_pos_calc: Mapped position of the joystick
                servo_pos: Position of the servo motor

        """


        self.fieldnames = ['Time', 'Joystick position', 'Joystick position calculated', 'Servo position']
        self.rows=[
            {'Time':self.read_time,'Joystick position':joystick_pos, 'Joystick position calculated':joystick_pos_calc,
            'Servo position':servo_pos}
        ]
        filename = 'turrets({},{}).csv'.format(self.test_number, seat)
        file = open(filename, 'a', newline='')

        with file:
            file_is_empty = os.stat(filename).st_size == 0
            writer = csv.writer(file,delimiter=',')
            writer = csv.DictWriter(file,fieldnames=self.fieldnames)

            if file_is_empty:
                writer.writeheader()

            writer.writerows(self.rows)

    def write_bluster(self, seat:int, led_points:bool, led_shoot:bool, sensor:bool,score:int, magazine:int):


        """
            Write values from bluster

            Arguments:
                seat: Controller seat
                led_points: state of the points led
                led_shoot: State of the shoot led
                sensor: State of the sensor
                score: Number of points
                magazine: Number of shots left in the magazine

        """


        self.fieldnames = ['Time', 'Points LED', 'Shoot LED', 'Sensor state', 'Score', 'Magazine']
        self.rows=[
            {'Time':self.read_time,'Points LED':led_points, 'Shoot LED':led_shoot,
            'Sensor state':sensor, 'Score':score, 'Magazine':magazine}
        ]
        filename = 'bluster({},{}).csv'.format(self.test_number, seat)
        file = open(filename, 'a', newline='')

        with file:
            file_is_empty = os.stat(filename).st_size == 0
            writer = csv.writer(file,delimiter=',')
            writer = csv.DictWriter(file,fieldnames=self.fieldnames)

            if file_is_empty:
                writer.writeheader()

            writer.writerows(self.rows)

    def write_display(self, score_A:int, score_B:int, state:str):

        """
            Write values from display

            Arguments:
                score_A: Score of Team A
                score_B: Score of Team B
                state: State of the display

        """

        self.fieldnames = ['Time', 'Score Team A', 'Score Team B', 'Display state']
        self.rows=[
            {'Time':self.read_time,'Score Team A':score_A, 'Score Team B':score_B, 'Display state':state}
        ]
        filename = 'display({}).csv'.format(self.test_number)
        file = open(filename, 'a', newline='')

        with file:
            file_is_empty = os.stat(filename).st_size == 0
            writer = csv.writer(file,delimiter=',')
            writer = csv.DictWriter(file,fieldnames=self.fieldnames)

            if file_is_empty:
                writer.writeheader()

            writer.writerows(self.rows)

    def write_state(self,state:str):

        """
            Write values from state machine

            Arguments:
                test_number: Number of the test game
                state: State of the game

        """

        self.fieldnames = ['Time', 'Game state']
        self.rows=[
            {'Time':self.read_time,'Game state':state}
        ]
        filename = 'state({}).csv'.format(self.test_number)
        file = open(filename, 'a', newline='')

        with file:
            file_is_empty = os.stat(filename).st_size == 0
            writer = csv.writer(file,delimiter=',')
            writer = csv.DictWriter(file,fieldnames=self.fieldnames)

            if file_is_empty:
                writer.writeheader()

            writer.writerows(self.rows)


    def clear_file(self, name:str):

        """
            Delete everything on a file and close the file

            Arguments:
                name: Name of file to close
        """
        file = open(name, 'r+')
        file.truncate(0)
        file.close()

debug = _Debug()

if __name__ == "__main__":
    time_test = _Debug()
    #time_test.clear_file('stepper(1).csv')
    time_test.write_stepper(5,2,4,5,6)
    time_test.write_stepper(3,32,34,67,2)
    time_test.write_turrets(5,2,4,5)
    time_test.write_bluster(5,0,0,0,3,54)
    time_test.write_display(5,2,'Start')
    time_test.write_state('Start')
