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

# conventions
sensor_1 = [TRIGGER_PIN_1, ECHO_PIN_1]
sensor_2 = [TRIGGER_PIN_2, ECHO_PIN_2]

# get distance from sensor
def trigger(sensor):

    print("getting distance...")

    #......SENSOR 1....................
    print("1. sending trigger pulse")
    # Send a trigger pulse.
    GPIO.output(sensor[0], GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(sensor[0], GPIO.LOW)
    # Start a timer.
    start_time = time.time()
    end_time = time.time()

    #........ECHO 1................................
    print("1. Wait for the echo pulse to return...")
    # Wait for the echo pulse to return.
    while GPIO.input(sensor[1]) == GPIO.LOW:
        start_time = time.time()

    while GPIO.input(sensor[1]) == GPIO.HIGH:
        # Stop the timer.
        end_time = time.time()

    # Calculate the distance.
    print("calculating distance")
    speed_of_sound = 343 #m/s
    pulse_duration = end_time - start_time #sec
    distance = (speed_of_sound * pulse_duration * 100) /2 #cm
    #pulse_duration_2 = end_time_2 - start_time_2 #sec
    #distance_2 = (speed_of_sound * pulse_duration_2 * 100) /2 #cm 

    return distance

def loop_on():
    #keep the sensor_1 0n in while loop until the distance is less than 100
    while distance_1 > 150:
        print("inside while loop, within the time\n\n")
        # trigger the ultrasonic sensor.
        distance_1 = trigger(sensor_1)
        print("distance 1 : ", distance_1)
        time.sleep(0.1) # sleep for 0.1 sec


# get current time
now = time.localtime()
print("got the current time")
print(now)

# check if it is night time
if now.tm_hour >= 18 and now.tm_hour <= 23:
#if now.tm_hour >= 12 and now.tm_hour <= 18:

    while True:
        print("it is night time")
        distance_1 = 200
        count = 0 # person in the room counter

        #keep the sensor_1 0n in while loop until the distance is less than 100
        #keep the sensor_1 0n in while loop until the distance is less than 100
        while distance_1 > 150:
            print("inside while loop, within the time\n\n")
            # trigger the ultrasonic sensor.
            distance_1 = trigger(sensor_1)
            print("distance 1 : ", distance_1)
            time.sleep(0.1) # sleep for 0.1 sec

        # If the distance_1 is less than 100, check the distance_2 from the sensor_2.
        if distance_1 < 150:
            print("DETECTED PERSON IN SENSOR 1")
            print("switching to sensor 2")
            # keep a list of distances from sensor 2
            dist_list = []  
            #trigger sensor 5 times
            for i in range(5):
                distance_2 = trigger(sensor_2)
                dist_list.append(distance_2)
                print("distance 2 : ", distance_2)
                time.sleep(0.001) # sleep for 1ms

            # if any value in the dist_list is less than 100, turn on the lights
            for i in dist_list:
                if i < 150 and count == 0:
                    # detection in sensor_2 also, turn on the lights
                    print("DETECTED PERSON IN SENSOR 2")
                    print("ENTERED ROOM")
                    print("Turning on the lights.")
                    GPIO.output(light_2, GPIO.LOW)
                    GPIO.output(light_3, GPIO.LOW)
                    count += 1
                    break # break the loop if any value is less than 150 
                
                elif i > 150 and count > 1: #nothing detected in sensor_2, but count is more than 1
                    print("SOMEONE LEFT THE ROOM")
                    count -= 1
                    print("now, count = ", count )
                    pass 

                elif i > 150 and count == 1: 
                    # no detection in sensor_2, but count WAS only 1,  turn off the lights
                    print("NO ONE IN THE ROOM")
                    print("LEFT ROOM")
                    print("Turning off the lights.")
                    GPIO.output(light_2, GPIO.HIGH)
                    GPIO.output(light_3, GPIO.HIGH)
                    count -= 1
            
        # Otherwise, turn off the lights.
        else:
            print("ERROR")
            print("Turning off the lights.")
            GPIO.output(light_2, GPIO.HIGH)
            GPIO.output(light_3, GPIO.HIGH)
            

