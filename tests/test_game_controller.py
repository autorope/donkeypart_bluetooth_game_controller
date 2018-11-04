import pytest
# -*- coding: utf-8 -*-
import unittest
from donkeyblue import BluetoothGameController



@pytest.fixture()
def get_input_device():
    yield 'test'


class TestMovingSquareTelemetry(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def setUp(self, ):
        self.ctlr = BluetoothGameController(input_path='/test/')




    def test_update_speed(self):
        self.ctlr.update_angle(3)
        assert self.ctlr.angle == 3


