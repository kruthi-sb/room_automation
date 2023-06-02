# ROOM AUTOMATION
*EMERGENCY CODE TO STOP SERVICE:*
`sudo systemctl stop room_lights`

## DESCRIPTION
This project aims to build an automatic light control system for a room. The system will be able to detect and entry and exit of a person and control the light in the room likewise.

## COMPONENTS
1. Raspberry Pi 3B+
2. Ultrasonic Sensor HC-SR04 (x2)
3. Relay Module (x1)
4. Jumper Wires
5. Power Supply for Raspberry Pi (5V, 2.5A recommended)

## WIRING DIAGRAM
Refer the wiring diagram in the files

## WORKING
The [ultrasonic sensors](https://lastminuteengineers.com/arduino-sr04-ultrasonic-sensor-tutorial/) are used to detect the entry and exit of a person. The 2 sensors are placed beside each other. Let's say the one near to the door is SENSOR 1 and the other one is SENSOR 2. The SENSOR 1 is always kept ON. 
- *ENTRY:*
When a person enters the room, SENSOR 1 detects the person and inturn triggers SENSOR 2. The SENSOR 2 verifies the entry of the person and turns on the light.
- *EXIT:*
When the person exits the room, SENSOR 1 detects the person and inturn triggers SENSOR 2. But, the SENSOR 2 doesn't catch the person as he/she has already exited the room. So, the light turn off.
- *COUNT:*
This count is used to determine the number of people in the room.
    At each trigger of SENSOR 2, the count is incremented by 1.
    At each trigger of SENSOR 1, but NO trigger of SENSOR 2, the count is decremented by 1. 

## GPIO PINS

NOTE: 'my_plan2.py' code uses **GPIO BOARD mode** for pin numbering. Refer [this for pin diagram](https://www.raspberrypi.com/documentation/computers/os.html#gpio-and-the-40-pin-header) and [this for modes](https://iot4beginners.com/difference-between-bcm-and-board-pin-numbering-in-raspberry-pi/).

- *SENSOR 1:*          
GND 1 - 14         
ECHO 1 - 5          
TRIG 1 - 12         
VCC - 4    

- *SENSOR 2:*                    
GND 2 - 9          
ECHO 2 - 19          
TRIG 2 - 10         
VCC - 4   

- *RELAY:*          
GND OUT - 6     
VCC 5V - 2            
IN2 - 38      
GND IN1 - 34             

## CODE GUIDE
- Refer 'my_plan2.py' file for the final working code. 
- 'my_start.py' file runs the 'my_plan2.py' file when time conditions are met. It checks the current time every 5 mins and runs the code if the time is between 18:00 PM and 23:00 PM.
- 'turn_on.py' file is used to turn on the light manually. It includes setting up the GPIO pins and turning on the light.
- 'turn_off.py' file is used to turn off the light manually. It includes setting up the GPIO pins and turning off the light.
- Rest of the files are previous versions of the code.

## Rasbian OS Commands

### To setup the Raspberry Pi for the project, follow the below steps:
1. `sudo apt-get update`: To update the OS
2. `sudo apt-get upgrade`: To upgrade the OS (to be done after update always)
3. `sudo apt-get install python3-pip`: To install pip3 (python3 package manager)
4. `sudo pip3 install RPi.GPIO`: To install GPIO library for python3

### To set up 'my_plan2.py' code:
1. `sudo nano my_plan2.py`: To create a new file named 'my_plan2.py' and open it in nano editor
2. Copy the code from 'my_plan2.py' file and paste it in the nano editor
3. `Ctrl + O` and `Enter`: To save the file
4. `Ctrl + X`: To exit the nano editor
5. `sudo python3 my_plan2.py`: To run the code
6. `Ctrl + C`: To stop the code

### To set up 'my_start.py' code:
1. `sudo nano my_start.py`: To create a new file named 'my_start.py' and open it in nano editor
2. Copy the code from 'my_start.py' file and paste it in the nano editor
3. `Ctrl + O` and `Enter`: To save the file
4. `Ctrl + X`: To exit the nano editor
5. `sudo python3 my_start.py`: To run the code
6. `Ctrl + C`: To stop the code

### To set up 'my_start.py' code to run at startup:
Some already explored-but-failed methods are rc.local and crontab. The best method is to use systemd service. 

Using Systemd service: You can create a systemd service unit to run your Python script at startup. Systemd is a modern init system used in many Linux distributions, including Raspberry Pi OS.

1. Create a systemd service unit file:
`sudo nano /etc/systemd/system/room_lights.service`

2. In the text editor, enter the following content for the service unit file:

```
[Unit]
Description=Your Service Description
After=network.target

[Service]
ExecStart=/usr/bin/python3 /home/iron-man42/my_start.py
WorkingDirectory=/home/iron-man42
StandardOutput=inherit
StandardError=inherit
Restart=always
User=iron-man42

[Install]
WantedBy=multi-user.target
```

3. Save the file by pressing Ctrl+O, then exit the text editor by pressing Ctrl+X.

4. Set the correct permissions for the service unit file:
`sudo chmod 644 /etc/systemd/system/room_lights.service`

5. Enable the service to start at boot:
`sudo systemctl enable room_lights.service`

6. Start the service manually to test:
`sudo systemctl start room_lights`

7. Check the status of the service to verify it's running without errors:
`sudo systemctl status room_lights`

8. Reboot the Raspberry Pi and check the status of the service again to verify it starts automatically:
`sudo reboot`
`sudo systemctl status room_lights`

9. To stop the service:
`sudo systemctl stop room_lights`

### Output from systemd service:
By default, the output of the service is directed to the system journal. To view the output, use
`sudo journalctl -u room_lights`
The logs will include both standard output and standard error messages.

## REFERENCES
About Ultrasonic sensor HC-SR04 physics:

Ultrasonic sensors work based on the principle of echolocation. 
Here's a high-level overview of how ultrasonic sensors typically work:

- The sensor emits a short burst of ultrasonic sound waves, usually in the range of **40 kHz** to 200 kHz. This burst is often referred to as a "ping."

- The sound waves propagate through the air in a cone-shaped pattern from the sensor. When the sound waves encounter an object in their path, they bounce back (reflect) off the object.

- The sensor detects the reflected sound waves (echo) using a receiver element.

- By measuring the time between the transmission of the sound wave and the reception of the echo, the sensor can determine the time of flight (TOF) of the sound waves.

- Knowing the speed of sound in the medium (usually air), the sensor can calculate the distance to the object using the formula: Distance = (Speed of Sound × Time of Flight) / 2.

- The frequency range of ultrasonic sensors typically used in consumer electronics is **40 kHz** (human range is upto 20 kHz).

## TROUBLESHOOTING
- Use `turn_on.py` and `turn_off.py` files to check if the relay is working properly.
- Use `sudo python3 my_plan2.py` to check if the code is working properly.
- Use `sudo python3 my_start.py` to check if the code is working properly.
- Use `sudo systemctl status room_lights` to check if the service is running properly.
- Use `sudo journalctl -u room_lights` to check the logs of the service.
- Use `sudo systemctl stop room_lights` to stop the service.
- Use `sudo systemctl disable room_lights` to disable the service.
- Use `sudo systemctl enable room_lights` to enable the service.
- Use `sudo systemctl start room_lights` to start the service.

## CREDITS
- Thanks to ChatGPT for helping with linux commands and troubleshooting.
- Thanks to Me for finding out the logic for the system.
- Thanks to Github Copilot for helping with the README.md file.
