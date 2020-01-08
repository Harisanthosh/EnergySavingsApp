from labjack import ljm
import math

# Open first found LabJack
handle = ljm.openS("ANY", "ANY", "ANY")

# Call eReadName to read the serial number from the LabJack.
name = "SERIAL_NUMBER"
result = ljm.eReadName(handle, name)

print("\neReadName result: ")
print("    %s = %f" % (name, result))

numFrames = 4
#names = ["SERIAL_NUMBER", "PRODUCT_ID", "FIRMWARE_VERSION"]
names = ['AIN0','AIN1','AIN2','AIN3']
results = ljm.eReadNames(handle, numFrames, names)

print("\neReadNames results: ")
for i in range(numFrames):
    print("Measured Power of - %s, value : %f" % (names[i], (results[i]/0.1) * 9))
    # print("Voltage of - %s, value : %f" % (names[i], results[i]))

# regx = ['AIN0','AIN1','AIN2','AIN3']
#
# for trx in regx:
#     rxx = ljm.eReadName(handle, trx)
#     print("%s Voltage is %f" % (trx, rxx))

