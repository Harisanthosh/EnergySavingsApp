from labjack import ljm
import math
import time
import paho.mqtt.publish as publish


def retrieve_analogvalues():
    # Open first found LabJack
    handle = ljm.openS("ANY", "ANY", "ANY")

    # Call eReadName to read the serial number from the LabJack.
    name = "SERIAL_NUMBER"
    result = ljm.eReadName(handle, name)

    print("\neReadName result: ")
    print("    %s = %f" % (name, result))
    numFrames = 4
    # names = ["SERIAL_NUMBER", "PRODUCT_ID", "FIRMWARE_VERSION"]
    names = ['AIN0', 'AIN1', 'AIN2', 'AIN3']
    results = ljm.eReadNames(handle, numFrames, names)

    print("\neReadNames results: ")
    for i in range(numFrames):
        print("Measured Power of - %s, value : %f" % (names[i], (abs(results[i]) / 0.1) * 9))

    return results


def get_continuous_values():
    for x in range(10):
        retrieve_analogvalues()
        time.sleep(4)
        #print(x)



# while True:
#     numFrames = 4
#     # names = ["SERIAL_NUMBER", "PRODUCT_ID", "FIRMWARE_VERSION"]
#     names = ['AIN0', 'AIN1', 'AIN2', 'AIN3']
#     results = ljm.eReadNames(handle, numFrames, names)
#
#     print("\neReadNames results: ")
#     for i in range(numFrames):
#         print("Measured Power of - %s, value : %f" % (names[i], (abs(results[i]) / 0.1) * 9))

if __name__ == "__main__":
    get_continuous_values()
    # retrieve_analogvalues()

