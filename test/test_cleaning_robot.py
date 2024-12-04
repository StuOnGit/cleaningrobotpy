from unittest import TestCase
from unittest.mock import Mock, patch, call

from mock import GPIO
from mock.ibs import IBS
from src.cleaning_robot import CleaningRobot
import re


class TestCleaningRobot(TestCase):


    @patch.object(GPIO, "input")
    def test_something(self, mock_object: Mock):
        # This is an example of test where I want to mock the GPIO.input() function
        pass

    def test_initialize_robot_x(self):
        robot = CleaningRobot()
        robot.initialize_robot()
        self.assertEqual(robot.pos_x, 0)

    def test_initialize_robot_y(self):
        robot = CleaningRobot()
        robot.initialize_robot()
        self.assertEqual(robot.pos_y, 0)

    def test_initialize_robot_heading(self):
        robot = CleaningRobot()
        robot.initialize_robot()
        self.assertEqual(robot.heading, 'N')

    def test_robot_status(self):
        robot = CleaningRobot()
        robot.initialize_robot()
        status = robot.robot_status()
        pattern = r'^\((0|1|2|),(0|1|2|3|4),(N|S|O|W)\)$'
        result =  re.match(pattern, status)
        self.assertTrue(result)