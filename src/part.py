
import time
from itertools import cycle

import evdev
from evdev import ecodes
import yaml


class BluetoothDevice:

    def get_input_device(self, path):
        return evdev.InputDevice(path)

    def find_input_device(self, search_term):
        all_devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
        likely_devices = []
        for device in all_devices:
            if self.search_term in device.name.lower():
                likely_devices.append(device)

        if len(likely_devices) == 1:
            # correct device was likely found
            return likely_devices[0]
        elif len(likely_devices) >= 2:
            raise ValueError("found several possible devices. Please specify your input stream.")
        else:
            raise ValueError("no input event streams found")
        return None


class BluetoothGameController(BluetoothDevice):
    """
    Generator of cordinates of a bouncing moving square for simulations.
    """

    def __init__(self, input_path=None):
        # used to find the event stream input (/dev/input/...)
        self.search_term = "nintendo"

        self.running = False

        self.state = {}
        self.angle = 0.0
        self.throttle = 0.0

        self.throttle_scale = 1.0
        self.throttle_scale_increment = .05
        self.y_axis_direction = -1  # pushing stick forward gives negative values

        self.drive_mode_toggle = cycle(['user', 'local_angle', 'local'])
        self.drive_mode = next(self.drive_mode_toggle)

        self.recording_toggle = cycle([True, False])
        self.recording = next(self.recording_toggle)

        if input_path is None:
            self.device = self.find_input_device(self.search_term)
        else:
            self.device = self.get_input_device(input_path)

        self.btn_map = {305: 'A',
                        304: 'B',
                        307: 'X',
                        308: 'Y',
                        312: 'LEFT_BOTTOM_TRIGGER',
                        310: 'LEFT_TOP_TRIGGER',
                        313: 'RIGHT_BOTTOM_TRIGGER',
                        311: 'RIGHT_TOP_TRIGGER',
                        317: 'LEFT_STICK_PRESS',
                        318: 'RIGHT_STICK_PRESS',
                        314: 'SELECT',
                        315: 'START',
                        0: 'LEFT_STICK_X',
                        1: 'LEFT_STICK_Y',
                        3: 'RIGHT_STICK_X',
                        4: 'RIGHT_STICK_Y',
                        547: 'PAD_RIGHT',
                        546: 'PAD_LEFT',
                        544: 'PAD_UP',
                        548: 'PAD_DOWN',
                        }

        self.func_map = {
            'LEFT_STICK_X': self.update_angle,
            'LEFT_STICK_Y': self.update_throttle,
            'B': self.toggle_recording,
            'A': self.toggle_drive_mode,
            'PAD_UP': self.increment_throttle_scale,
            'PAD_DOWN': self.decrement_throttle_scale,
        }
        self.joystic_max_value = 1280

    def update_angle(self, val):
        self.angle = val
        return

    def update_throttle(self, val):
        self.throttle = val * self.throttle_scale * self.y_axis_direction
        return

    def toggle_recording(self, val):
        if val == 1:
            self.recording = next(self.recording_toggle)
        return

    def toggle_drive_mode(self, val):
        if val == 1:
            self.drive_mode = next(self.drive_mode_toggle)
        return

    def increment_throttle_scale(self, val):
        if val == 1:
            self.throttle_scale += self.throttle_scale_increment
        return

    def decrement_throttle_scale(self, val):
        if val == 1:
            self.throttle_scale -= self.throttle_scale_increment
        return

    def read_loop(self):
        """
        Read input, map events to button names and scale joystic values to between 1 and 0.
        """
        event = next(self.device.read_loop())
        btn = self.btn_map.get(event.code)
        val = event.value
        if event.type == ecodes.EV_ABS:
            val = val / self.joystic_max_value
        return btn, val

    def update(self):
        while True:
            btn, val = self.read_loop()

            # update state
            self.state[btn] = val

            # run_functions
            func = self.func_map.get(btn)
            if func is not None:
                func(val)

    def run_threaded(self, img_arr=None):
        return self.angle, self.throttle, self.drive_mode, self.recording

    def shutdown(self):
        self.running = False
        time.sleep(0.1)