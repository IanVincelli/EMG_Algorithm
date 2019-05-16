
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

def data_processing():

    while True:
        print("Collect new data from arduino? (y/n)")
        i = input()
        if (i == "y"):
            import data_import
            data = data_import.data
            np.save('EMG_data.npy',data)
            break
        elif (i == "n"):
            data  = np.load('EMG_data.npy')
            break
        else:
            print("Input not supported")
    print("Data collection complete")

    print("Commence Data Processing? (y/n)")
    while True:
        i = input()
        if (i == "y"):
            data = data_smooth(data)
            print("Save Processed Data? (y/n)")
            print("Data#.npy standard save format")
            x = input()
            np.save(x,data)
            break
        elif (i == "n"):
            break
        else:
            print("Input not supported")
 
    print("Load new data? Default is Data1 (y/n)")
    while True:
        i = input()
        if (i == "y"):
            files = [f for f in os.listdir('.') if os.path.isfile(f)]
            print(files)
            print("Choose a file")
            x= input()
            data = np.load(x)
            break
        elif (i == "n"):
            data = np.load('Data1.npy')
            break
        else:
            print("Input not supported")

    print("Plot Data? (y/n)")
    while True:
        i = input()
        if (i == "y"):
            data_plot(data)
            break
        elif (i == "n"):
            break
        else:
            print("Input not supported")
    
def data_plot(data):
    titles = ["Sensor1", "Sensor2","rawValue","reference", "endMuscle", "midMuscle"]
    plt.figure(0)
    for n in range(0,6):

        length = sum([np.size(data[n][0]),np.size(data[n][1]),np.size(data[n][2]),np.size(data[n][3])])
        plt.subplot(321 + n)
        plt.title(titles[n])
        plt.plot(range(0,np.size(data[n][0])),data[n][0],'r:',
                 range(np.size(data[n][0]),length-np.size(data[n][2])-np.size(data[n][3])), data[n][1],'b:',
                       range(np.size(data[n][0])+np.size(data[n][1]),length-np.size(data[n][3])),data[n][2],'g:',
                       range(length-np.size(data[n][3]),length), data[n][3],'c:',lw=0.4)
    for n in range(0,6):
        f = plt.figure(n+1)
        plt.title(titles[n])
        for i in range(0,4):
            N = np.size(data[n][i])
            mean = np.mean(data[n][i])
            sd = np.std(data[n][i])
            plt.subplot(411 + i)
            plt.plot(data[n][i],'r:', [mean for x in range(0,N)],'b',
                    [(mean-sd) for x in range(0,N)],'k', [(mean+sd) for x in range(0,N)],'k',
                    [(mean-2*sd) for x in range(0,N)],'k', [(mean+2*sd) for x in range(0,N)],'k',lw=0.4)
    plt.show()

def data_smooth(data):
    titles = ["sen1", "sen2","raw","ref", "end", "mid"]
    processed = []
    std_filt=[False, False, False, False, False, False]
    runavg_filt=[False, False, False, False, False, False,5]

    print("Use 2 standard deviation filter? (y/n)")
    while True:
        i = input()
        if (i == "y"):
            print("To which data sets should this filter be applied")
            print("(sen1,sen2,raw,ref,end,mid), basic(sen1,sen2,raw), all")
            x = input()
            if ',' in x:
                x = x.split(',')
                for n in range(0,np.size(titles)):
                    if titles[n] in x:
                        std_filt[n] = True
            else:
                if x in titles:
                    n = titles.index(x)
                    std_filt[n] = True
                elif x == "basic":
                    for index in range(0,3):
                        std_filt[index] = True      
                elif x == "all":
                    for index in range(0,np.size(titles)):
                        std_filt[index] = True      
            break
        elif (i == "n"):
            break
        else:
            print("Input not supported")
    print("Use running average smoothin? (y,n)")
    while True:
        i = input()
        if (i == "y"):
            print("To which data sets should this smoothing be applied")
            print("(sen1,sen2,raw,ref,end,mid), basic(sen2,raw,ref,end,mid), all")
            x = input()
            if "," in x:
                x = x.split(',')
                for n in range(0,np.size(titles)):
                    if titles[n] in x:
                        runavg_filt[n] = True
            else:
                if x in titles:
                    n = titles.index(x)
                    runavg_filt[n] = True
                elif x == "basic":
                    for index in range(1,np.size(titles)):
                        runavg_filt[index] = True  
                elif x == "all":
                    for index in range(0,np.size(titles)-1):
                        runavg_filt[index] = True
                    
            print("How many points should be used in the averaging? (default = 5)")
            runavg_filt[-1]= int(input())
            break
        elif (i == "n"):
            break
        else:
            print("Input not supported")
    print(std_filt)
    print(runavg_filt)
    for n in range(0,6):
        plot = [[],[],[],[]]
        for i in range(0,np.size(data[n,:,0])):
            if data[0,i,1] == "Extension":
                plot[0].append(float(data[n,i,0]))
            elif data[0,i,1] == "Palm":
                plot[1].append(float(data[n,i,0]))
            elif data[0,i,1] == "Flexion":
                plot[2].append(float(data[n,i,0]))
            elif data[0,i,1] == "Fist":
                plot[3].append(float(data[n,i,0]))

        if std_filt[n] == True:
            sfilter_data = std_filter(plot)
            plot = sfilter_data
        if runavg_filt[n] == True:
            plot = runavg_filter(plot,runavg_filt[-1])

        processed.append(plot)
    return processed
    
def runavg_filter(data,num):
    for n in range(0,4):
        d_avg = []
        for i in range(num, np.size(data[n])-num):
            d_avg.append(np.mean(data[n][i-num:i+num]))
        data[n] = d_avg
        #del data[n][np.size(data[n])-num:np.size(data[n])]
    return data
        
def std_filter(data):

    for i in range(0,4):
        count = []
        N = np.size(data[i])
        mean = np.mean(data[i])
        sd = np.std(data[i])
        for x in range(0,N):
            if (data[i][x]> (2*sd +mean)):
                count.append(x)
        for y in range(0,np.size(count)):
            del data[i][count[y]-y]
    return data

def main():
    print("run data_processing?")
    while True:
        i = input()
        if (i == "y"):
            data_processing()
            break
        elif (i == "n"):
            break
        else:
            print("Input not supported")
    data = np.load("data1.npy")
    print(np.shape(data))
    print(np.shape(data[0,0]))

    #import ML_brain
    #ML_brain


#main()

import ML_brain
ML_brain


