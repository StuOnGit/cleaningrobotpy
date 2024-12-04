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
        self.assertEqual(robot.heading, robot.N)

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
    def test_manage_cleaning_system_cleaning_system_on(self, mock_ibs: Mock):
        robot = CleaningRobot()
        mock_ibs.return_value = 11
        robot.manage_cleaning_system()
        self.assertTrue(robot.cleaning_system_on)

    @patch.object(IBS, "get_charge_left")
    def test_manage_cleaning_system_cleaning_system_off(self, mock_ibs: Mock):
        robot = CleaningRobot()
        mock_ibs.return_value = 10
        robot.manage_cleaning_system()
        self.assertFalse(robot.cleaning_system_on)

    @patch.object(IBS, "get_charge_left")
    def test_manage_cleaning_recharge_on(self, mock_ibs: Mock):
        robot = CleaningRobot()
        mock_ibs.return_value = 10
        robot.manage_cleaning_system()
        self.assertTrue(robot.recharge_led_on)

    @patch.object(IBS, "get_charge_left")
    def test_manage_cleaning_recharge_off(self, mock_ibs: Mock):
        robot = CleaningRobot()
        mock_ibs.return_value = 11
        robot.manage_cleaning_system()
        self.assertFalse(robot.recharge_led_on)

    def test_execute_command_forward(self):
        robot = CleaningRobot()
        robot.initialize_robot()
        result = robot.execute_command(robot.FORWARD)
        self.assertEqual(result, '(0,1,N)')

    def test_execute_command_left(self):
        robot = CleaningRobot()
        robot.initialize_robot()
        result = robot.execute_command(robot.LEFT)
        self.assertEqual(result, '(0,0,W)')


    def test_execute_command_right(self):
        robot = CleaningRobot()
        robot.initialize_robot()
        result = robot.execute_command(robot.RIGHT)
        self.assertEqual(result, '(0,0,E)')

    @patch.object(GPIO, "input")
    def test_obstacle_found(self, mock_gpio: Mock):
        robot = CleaningRobot()
        robot.initialize_robot()
        mock_gpio.return_value = True
        result = robot.obstacle_found()
        self.assertTrue(result)

    @patch.object(GPIO, "input")
    def test_obstacle_not_found(self, mock_gpio: Mock):
        robot = CleaningRobot()
        robot.initialize_robot()
        mock_gpio.return_value = False
        result = robot.obstacle_found()
        self.assertFalse(result)


    @patch.object(GPIO, "input")
    def test_command_and_obstacle_found(self, mock_gpio: Mock):
        robot = CleaningRobot()
        robot.initialize_robot()
        mock_gpio.return_value = True
        result = robot.execute_command(robot.FORWARD)
        self.assertEqual(result, '(0,0,N)(0,1)')


    @patch.object(IBS, "get_charge_left")
    def test_command_but_not_charged(self, mock_ibs: Mock):
        robot = CleaningRobot()
        robot.initialize_robot()
        mock_ibs.return_value = 10
        result = robot.execute_command(robot.FORWARD)
        self.assertEqual(result, '!(0,0,N)')
