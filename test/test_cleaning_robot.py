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

    def test_robot_status_initial_position(self):
        robot = CleaningRobot()
        robot.initialize_robot()
        status = robot.robot_status()
        pattern = r'^\((0|1|2|),(0|1|2|3|4),(N|S|O|W)\)$'
        result =  re.match(pattern, status)
        self.assertTrue(result)

    def test_robot_status_position(self):
        robot = CleaningRobot()
        robot.heading = robot.S
        robot.pos_x = 2
        robot.pos_y = 2
        status = robot.robot_status()
        pattern = r'^\((0|1|2|),(0|1|2|3|4),(N|S|O|W)\)$'
        result = re.match(pattern, status)
        self.assertTrue(result)

    @patch.object(IBS, "get_charge_left")
    def test_manage_cleaning_system_cleaning_system_on_recharging_off(self, mock_ibs: Mock):
        robot = CleaningRobot()
        mock_ibs.return_value = 11
        robot.manage_cleaning_system()
        self.assertTrue(robot.cleaning_system_on)
