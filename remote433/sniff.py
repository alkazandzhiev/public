from datetime import datetime
import RPi.GPIO as GPIO
import json

RECEIVED_SIGNAL = [[], []]  #[[time of reading], [signal reading]]
MAX_DURATION = 1
RECEIVE_PIN = 2

if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RECEIVE_PIN, GPIO.IN)
    cumulative_time = 0
    #print("**Started recording**")
    beginning_time = datetime.now()
    while cumulative_time < MAX_DURATION:
        time_delta = datetime.now() - beginning_time
        RECEIVED_SIGNAL[0].append(time_delta)
        RECEIVED_SIGNAL[1].append(GPIO.input(RECEIVE_PIN))
        cumulative_time = time_delta.seconds
    #print("**Ended recording**")
    #print(len(RECEIVED_SIGNAL[0]))
    GPIO.cleanup()
    
    #print("**Processing results**")
    for i in range(len(RECEIVED_SIGNAL[0])):
        RECEIVED_SIGNAL[0][i] = RECEIVED_SIGNAL[0][i].seconds + RECEIVED_SIGNAL[0][i].microseconds/1000000.0

    #print("**Plotting results**")
    with open("output.txt", "w") as f:
        json.dump(RECEIVED_SIGNAL, f)

