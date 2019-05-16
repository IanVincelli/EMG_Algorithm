import serial
import time 
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd



ser = serial.Serial("COM3")
ser.flushInput()
#plot_window = 20
#y_var = np.array(np.zeros([plot_window]))

#plt.ion()
#fig, ax = plt.subplots()
#line, = ax.plot(y_var)
loop = True
count = 0
end = 0
s= -1
state = ["Extension", "Palm","Flexion","Fist"]
print("Initialized")
input("Press Enter When Ready")
print("Collecting Data")
print("Type Stop to end data collection")
while loop == True:
    s = s+1
    if (s>3):
        s = 0

    label = state[s]
    i = input("press enter to continue " + label )
    if (i == "Stop"):
        t = 1   
        loop = False
    else:
        t = 0

    if (t ==0):
        start = time.time()
        t = 1
    while (end - start < 1.5):
        ser_bytes = ser.readline()
        decoded_bytes = (ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
        parsed_data = decoded_bytes.split(',')

        if (np.size(parsed_data) == 6):
            if (count == 0):
                sensor1 =  [[float(parsed_data[0]),label]]
                sensor2 =  [[float(parsed_data[1]),label]]
                rawValue =  [[float(parsed_data[2]),label]]
                reference =  [[float(parsed_data[3]),label]]
                endMuscle =  [[float(parsed_data[4]),label]]
                midMuscle =  [[float(parsed_data[5]),label]]
                count = count +1
            else:
                sensor1.append([float(parsed_data[0]),label])
                sensor2.append([float(parsed_data[1]),label])
                rawValue.append([float(parsed_data[2]),label])
                reference.append([float(parsed_data[3]),label])
                endMuscle.append([float(parsed_data[4]),label])
                midMuscle.append([float(parsed_data[5]),label])

        end = time.time()

data = np.array([sensor1,sensor2,rawValue, reference,endMuscle,midMuscle])

    #print(end - start)

    


