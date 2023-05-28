import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(38, GPIO.OUT)
GPIO.setup(36, GPIO.OUT)

GPIO.output(38, GPIO.HIGH)
GPIO.output(36, GPIO.HIGH)

print("DONE")
#GPIO.cleanup()
