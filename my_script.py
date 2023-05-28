'''
start date: 29.05.23
end date: in progress

my practical project on room automation
requirements:
1. relay board
2. lights(2)
3. ultrasonic sensor(1)

concept:
when it is the night time and the sensor detects any object near the door
the lights turn on

'''


import RPi.GPIO as GPIO
import time

GPIO.cleanup()
# ultrasonic sensor pins
TRIGGER_PIN = 12
ECHO_PIN = 5

# light pins with respect to relay board
light_2 = 38
light_3 = 36

# GPIO BCM– The BCM option refers to the pin by “Broadcom SOC Channel. They signify the Broadcom SOC channel designation.
GPIO.setmode(GPIO.BOARD)

# set input and output pins in sensor
GPIO.setup(TRIGGER_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

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
    print("sending trigger pulse")
    # Send a trigger pulse.
    GPIO.output(TRIGGER_PIN, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(TRIGGER_PIN, GPIO.LOW)

    # Start a timer.
    start_time = time.time()
    end_time = time.time()

    print("Wait for the echo pulse to return...")
    # Wait for the echo pulse to return.
    while GPIO.input(ECHO_PIN) == GPIO.LOW:
        strat_time = time.time()

    while GPIO.input(ECHO_PIN) == GPIO.HIGH:
    	# Stop the timer.
    	end_time = time.time()

    # Calculate the distance.
    print("calculating distance")
    speed_of_sound = 343 #m/s
    pulse_duration = end_time - start_time #sec
    distance = (speed_of_sound * pulse_duration * 100) /2 #cm 

    return distance

# get current time
now = time.localtime()
print("got the current time")
print(now)

# check if it is night time
#if now.tm_hour >= 18 or now.tm_hour <= 22:
if now.tm_hour >= 12 and now.tm_hour <= 18:

    print("inside if condition, within the time")
    # Get the distance from the ultrasonic sensor.
    distance = get_distance()
    print("distance: ", distance)
    GPIO.setup(light_2, GPIO.OUT)
    GPIO.setup(light_3, GPIO.OUT)


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


# Close the GPIO pins.
#GPIO.cleanup()
#print("closed the GPIO pins")

