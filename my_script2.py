'''
start date: 28.05.23
end date: in progress

my practical project on room automation
requirements:
1. relay board
2. lights(2)
3. ultrasonic sensor(2)

concept:
when it is the night time and the sensor detects any object near the door
the lights turn on

'''


import RPi.GPIO as GPIO
import time

GPIO.cleanup()
# ultrasonic sensor pins
TRIGGER_PIN_1 = 12
ECHO_PIN_1 = 5

TRIGGER_PIN_2 = 8
ECHO_PIN_2 = 26

# light pins with respect to relay board
light_2 = 38
light_3 = 36

# GPIO BCM– The BCM option refers to the pin by “Broadcom SOC Channel. They signify the Broadcom SOC channel designation.
GPIO.setmode(GPIO.BOARD)

# set input and output pins in sensor
GPIO.setup(TRIGGER_PIN_1, GPIO.OUT)
GPIO.setup(ECHO_PIN_1, GPIO.IN)
GPIO.setup(TRIGGER_PIN_2, GPIO.OUT)
GPIO.setup(ECHO_PIN_2, GPIO.IN)

# setup output pins for lights
GPIO.setup(light_2, GPIO.OUT)
GPIO.setup(light_3, GPIO.OUT)

# turn off lights first
GPIO.output(light_2, GPIO.HIGH)
GPIO.output(light_3, GPIO.HIGH)
print("Everything set up")

# get distance from sensor
def get_distance():

    print("getting distance...")

    #......SENSOR 1....................
    print("1. sending trigger pulse")
    # Send a trigger pulse.
    GPIO.output(TRIGGER_PIN_1, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(TRIGGER_PIN_1, GPIO.LOW)
    # Start a timer.
    start_time_1 = time.time()
    end_time_1 = time.time()

    #........ECHO 1................................
    print("1. Wait for the echo pulse to return...")
    # Wait for the echo pulse to return.
    while GPIO.input(ECHO_PIN_1) == GPIO.LOW:
        start_time_1 = time.time()

    while GPIO.input(ECHO_PIN_1) == GPIO.HIGH:
        # Stop the timer.
        end_time_1 = time.time()


    #.......SENSOR 2...................
    print("2. sending trigger pulse")
    # Send a trigger pulse.
    GPIO.output(TRIGGER_PIN_2, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(TRIGGER_PIN_2, GPIO.LOW)
    # Start a timer.
    start_time_2 = time.time()
    end_time_2 = time.time()

    #........ECHO 2.................................
    print("2. Wait for the echo pulse to return...")
    # Wait for the echo pulse to return.
    while GPIO.input(ECHO_PIN_2) == GPIO.LOW:
        start_time_2 = time.time()

    while GPIO.input(ECHO_PIN_2) == GPIO.HIGH:
        # Stop the timer.
        end_time_2 = time.time()


    # Calculate the distance.
    print("calculating distance")
    speed_of_sound = 343 #m/s
    pulse_duration_1 = end_time_1 - start_time_1 #sec
    distance_1 = (speed_of_sound * pulse_duration_1 * 100) /2 #cm
    pulse_duration_2 = end_time_2 - start_time_2 #sec
    distance_2 = (speed_of_sound * pulse_duration_2 * 100) /2 #cm 
 

    return end_time_1, end_time_2, distance_1, distance_2

# get current time
now = time.localtime()
print("got the current time")
print(now)

# check if it is night time
#if now.tm_hour >= 18 or now.tm_hour <= 22:
if now.tm_hour >= 12 and now.tm_hour <= 18:

    print("inside if condition, within the time\n\n")
    # Get the distance from the ultrasonic sensor.
    end_time_1,end_time_2, distance_1, distance_2 = get_distance()
    print("end time 1 : ", end_time_1)
    print("end time 2 : ", end_time_2,"\n")
    print("distance 1 : ", distance_1)
    print("distance 2 : ", distance_2)


    print("CHECKING CONDITION\n\n")
    # If the endtime_2 is greater than endtime_2, turn on the lights.
    if end_time_2 > end_time_1+0.00001 and (distance_1 < 100 and distance_2 < 100):

        print("ENTERED ROOM")
        print("Turning on the lights.")
        GPIO.output(light_2, GPIO.LOW)
        GPIO.output(light_3, GPIO.LOW)

    # Otherwise, turn off the lights.
    elif end_time_1+0.00001 > end_time_2 and (distance_1 < 100 and distance_2 < 100):

        print("LEFT ROOM")
        print("Turning off the lights.")
        GPIO.output(light_2, GPIO.HIGH)
        GPIO.output(light_3, GPIO.HIGH)
'''
    #else if distance is not within 100 cm
    else :

	GPIO.output(light_2, GPIO.HIGH)
	GPIO.output(light_3, GPIO.HIGH)
'''
print("THE END")
'''
    # If the distance is less than 100 cm, turn on the lights.
    if distance < 100:

        print("distance within 10")
        print("Turning on the lights.")
        GPIO.output(light_2, GPIO.LOW)
        GPIO.output(light_3, GPIO.LOW)

    # Otherwise, turn off the lights.
    else:
        print("Turning off the lights.")
        GPIO.output(light_2, GPIO.HIGH)

print("exited from if block")

'''
# Close the GPIO pins.
#GPIO.cleanup()
#print("closed the GPIO pins")
