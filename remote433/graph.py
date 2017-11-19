from datetime import datetime
import matplotlib.pyplot as pyplot
import json

if __name__ == '__main__':
    with open("output.txt", "r") as f:
        RECEIVED_SIGNAL = json.load(f)

    #print '**Plotting results**'
    pyplot.plot(RECEIVED_SIGNAL[0], RECEIVED_SIGNAL[1])
    pyplot.axis([0.011, 0.5976, -0.2, 1.2])
    pyplot.minorticks_on()
    pyplot.grid(True)
    pyplot.grid(which='minor', linestyle=':', linewidth='0.5', color='black')
    pyplot.show()
