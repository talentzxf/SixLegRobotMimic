import time
import serial


ser = serial.Serial(

    port='/dev/ttyAMA0',
    baudrate = 115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

legs = []

for i in range(6):
    legs.append([])
    legs[i].append(i*3)
    legs[i].append(i * 3+1)
    legs[i].append(i * 3 +2 )


cmd='"#%03dP2500T1000!"'%legs[0][1]
print(cmd)
ser.write(cmd)
ser.close()
