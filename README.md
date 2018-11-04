# Bluetooth Game Controller
This is a library to connect a Wii-U (and possibly others) bluetooth game controller to your donkeycar.


### Install
Install the library.
```bash
git clone https://github.com/autorope/donkeypart_bluetooth_game_controller.git
pip install -e ./donkeypart_bluetooth_game_controller
```


### Connect your bluetooth controller to the raspberry pi.
1. Start the bluetooth bash tool on your raspberry pi.
```bash
sudo bluetoothctl
power on
scan on
```

2. Turn on your controller in scan mode and look for your controllers name in the bluetoothctl 
scan results. 
3. Connect to your controller using its id (my controller id is `8C:CD:E8:AB:32:DE`) once you've found it's id. You may have to run these commands several times.
```bash
pair 8C:CD:E8:AB:32:DE
connect 8C:CD:E8:AB:32:DE
trust 8C:CD:E8:AB:32:DE
```
4. Now your controller should show that your connected (ie. blinking light turns solid.)

5. Run the part script to see if it works. You should see all the button values printed as you press them. Like this.
```bash
LEFT_STICK_Y 0.00234375
LEFT_STICK_Y 0.0015625
LEFT_STICK_Y 0.00078125
A 1
A 0
Y 1
Y 0
X 1
X 0
```