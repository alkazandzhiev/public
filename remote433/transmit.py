from array import array
import time, sys
import RPi.GPIO as GPIO

NUM_ATTEMPTS = 4
TRANSMIT_PIN = 2

# Transmit pulse times
tPulseTotal =   0.00166 # Should equal tPulseZeroOn + tPulseZeroOff and tPulseOneOn + tPulseOneOff
tPulseZeroOn =  0.00126
tPulseZeroOff = 0.00040
tPulseOneOn =   0.00044
tPulseOneOff =  0.00122

# Transmit batch times
tBatchTotal =   0.05333 # Should be tBatchOn + tBatchOff
tBatchOn =      0.04150 # Should be 25*tPulseTotal
tBatchOff =     0.01183 # The silence between the batches

# Pre-initialized commands sequences
pulseOn = [[], [], [], []]
pulseOff = [[], [], [], []]
pulseOn[0].append(array('l', [1, 1,1,0,1,0,1,0,1, 1,1,0,1,0,1,0,1, 0,1,0,1,0,1,0,1]))
pulseOn[0].append(array('l', [1, 1,1,0,1,0,1,0,1, 0,1,1,1,0,1,0,1, 0,1,0,1,0,1,0,1]))
pulseOn[0].append(array('l', [1, 1,1,0,1,0,1,0,1, 0,1,0,1,1,1,0,1, 0,1,0,1,0,1,0,1]))
pulseOn[0].append(array('l', [1, 1,1,0,1,0,1,0,1, 0,1,0,1,0,1,1,1, 0,1,0,1,0,1,0,1]))
pulseOn[1].append(array('l', [1, 0,1,1,1,0,1,0,1, 1,1,0,1,0,1,0,1, 0,1,0,1,0,1,0,1]))
pulseOn[1].append(array('l', [1, 0,1,1,1,0,1,0,1, 0,1,1,1,0,1,0,1, 0,1,0,1,0,1,0,1]))
pulseOn[1].append(array('l', [1, 0,1,1,1,0,1,0,1, 0,1,0,1,1,1,0,1, 0,1,0,1,0,1,0,1]))
pulseOn[1].append(array('l', [1, 0,1,1,1,0,1,0,1, 0,1,0,1,0,1,1,1, 0,1,0,1,0,1,0,1]))
pulseOn[2].append(array('l', [1, 0,1,0,1,1,1,0,1, 1,1,0,1,0,1,0,1, 0,1,0,1,0,1,0,1]))
pulseOn[2].append(array('l', [1, 0,1,0,1,1,1,0,1, 0,1,1,1,0,1,0,1, 0,1,0,1,0,1,0,1]))
pulseOn[2].append(array('l', [1, 0,1,0,1,1,1,0,1, 0,1,0,1,1,1,0,1, 0,1,0,1,0,1,0,1]))
pulseOn[2].append(array('l', [1, 0,1,0,1,1,1,0,1, 0,1,0,1,0,1,1,1, 0,1,0,1,0,1,0,1]))
pulseOn[3].append(array('l', [1, 0,1,0,1,0,1,1,1, 1,1,0,1,0,1,0,1, 0,1,0,1,0,1,0,1]))
pulseOn[3].append(array('l', [1, 0,1,0,1,0,1,1,1, 0,1,1,1,0,1,0,1, 0,1,0,1,0,1,0,1]))
pulseOn[3].append(array('l', [1, 0,1,0,1,0,1,1,1, 0,1,0,1,1,1,0,1, 0,1,0,1,0,1,0,1]))
pulseOn[3].append(array('l', [1, 0,1,0,1,0,1,1,1, 0,1,0,1,0,1,1,1, 0,1,0,1,0,1,0,1]))
pulseOff[0].append(array('l', [1, 1,1,0,1,0,1,0,1, 1,1,0,1,0,1,0,1, 0,1,0,1,0,1,1,1]))
pulseOff[0].append(array('l', [1, 1,1,0,1,0,1,0,1, 0,1,1,1,0,1,0,1, 0,1,0,1,0,1,1,1]))
pulseOff[0].append(array('l', [1, 1,1,0,1,0,1,0,1, 0,1,0,1,1,1,0,1, 0,1,0,1,0,1,1,1]))
pulseOff[0].append(array('l', [1, 1,1,0,1,0,1,0,1, 0,1,0,1,0,1,1,1, 0,1,0,1,0,1,1,1]))
pulseOff[1].append(array('l', [1, 0,1,1,1,0,1,0,1, 1,1,0,1,0,1,0,1, 0,1,0,1,0,1,1,1]))
pulseOff[1].append(array('l', [1, 0,1,1,1,0,1,0,1, 0,1,1,1,0,1,0,1, 0,1,0,1,0,1,1,1]))
pulseOff[1].append(array('l', [1, 0,1,1,1,0,1,0,1, 0,1,0,1,1,1,0,1, 0,1,0,1,0,1,1,1]))
pulseOff[1].append(array('l', [1, 0,1,1,1,0,1,0,1, 0,1,0,1,0,1,1,1, 0,1,0,1,0,1,1,1]))
pulseOff[2].append(array('l', [1, 0,1,0,1,1,1,0,1, 1,1,0,1,0,1,0,1, 0,1,0,1,0,1,1,1]))
pulseOff[2].append(array('l', [1, 0,1,0,1,1,1,0,1, 0,1,1,1,0,1,0,1, 0,1,0,1,0,1,1,1]))
pulseOff[2].append(array('l', [1, 0,1,0,1,1,1,0,1, 0,1,0,1,1,1,0,1, 0,1,0,1,0,1,1,1]))
pulseOff[2].append(array('l', [1, 0,1,0,1,1,1,0,1, 0,1,0,1,0,1,1,1, 0,1,0,1,0,1,1,1]))
pulseOff[3].append(array('l', [1, 0,1,0,1,0,1,1,1, 1,1,0,1,0,1,0,1, 0,1,0,1,0,1,1,1]))
pulseOff[3].append(array('l', [1, 0,1,0,1,0,1,1,1, 0,1,1,1,0,1,0,1, 0,1,0,1,0,1,1,1]))
pulseOff[3].append(array('l', [1, 0,1,0,1,0,1,1,1, 0,1,0,1,1,1,0,1, 0,1,0,1,0,1,1,1]))
pulseOff[3].append(array('l', [1, 0,1,0,1,0,1,1,1, 0,1,0,1,0,1,1,1, 0,1,0,1,0,1,1,1]))

def transmit_code(group, channel, state):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRANSMIT_PIN, GPIO.OUT)
    code = 0
    if (state != 0):
        code = pulseOn[group][channel]
    else:
        code = pulseOff[group][channel]

    for i in range(NUM_ATTEMPTS):
        for signal in code:
            if signal != 0:
                GPIO.output(TRANSMIT_PIN, 1)
                time.sleep(tPulseOneOn)
                GPIO.output(TRANSMIT_PIN, 0)
                time.sleep(tPulseOneOff)
            else:
                GPIO.output(TRANSMIT_PIN, 1)
                time.sleep(tPulseZeroOn)
                GPIO.output(TRANSMIT_PIN, 0)
                time.sleep(tPulseZeroOff)

        GPIO.output(TRANSMIT_PIN, 0)
        time.sleep(tBatchOff)
    GPIO.cleanup()

if __name__ == '__main__':
    if (len(sys.argv) >= 4):
        transmit_code(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))

