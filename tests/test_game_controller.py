import pytest
# -*- coding: utf-8 -*-
import unittest
import evdev
from evdev import ecodes

from ..donkeypart_bluetooth_controller import BluetoothGameController

from select import select
from pytest import raises, fixture


class FakeDevice:
    def read_loop(self):
        return 'test'

@pytest.fixture
def input_device():
    return FakeDevice()


def test_device_read_loop(input_device):
    print('reading loop')
    ctlr = BluetoothGameController(event_input_device=input_device)
    ctlr.device.read_loop()

