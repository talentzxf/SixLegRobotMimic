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

for i in range(17):
    cmd='"#%03dP1500T0150!"'%i
    print cmd
    ser.write(cmd)

#cmd='"#001P1500T0150!"'
#print cmd
#ser.write(cmd)

	
ser.close()
