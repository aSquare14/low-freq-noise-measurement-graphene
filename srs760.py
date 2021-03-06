import visa
import csv
import re

rm = visa.ResourceManager()
inst = rm.open_resource('GPIB0::10::INSTR')

def identify_instrument():
    inst_details = inst.query('*IDN?\n')
    print(inst_details)

def start_srs():
    inst.write("*RST\n")
    inst.write("MEAS 0,0\n")

def daq():
    f = open("yaxis.txt","w+")
    f.write(inst.query('SPEC?0\n'))
    f.close()

    f = open('yaxis.txt', 'r+')
    n = f.read().replace(',','\n')
    f.truncate(0)
    f.close()

    f = open('yaxis.txt','w+')
    f.write(n)
    f.close()

    f2 = open("xaxis.txt","w+")
    for i in range(399):
        f2.write(inst.query('BVAL?0,'+str(i)+'\n'))
    f2.close()
    convert_to_csv()

def convert_to_csv():
    f = open('yaxis.txt', 'r+')
    n = f.read().replace(',','')
    f.truncate(0)
    f.close()

    f = open('yaxis.txt','w+')
    f.write(n)
    f.close()

    myData = []
    fy = open("yaxis.txt","r")
    fx = open("xaxis.txt","r")
    y = fy.read().splitlines()
    x = fx.read().splitlines()

    for i in range(len(x)) :
        l = [x[i],y[i]]
        myData.append(l)
    myFile = open('Values.csv','w')
    with myFile:
        writer = csv.writer(myFile)
        writer.writerows(myData)
    print("Measurement is done ! Check your CSV file.\nLeft column is x-axis and right is y-axis !")

def set_frequency(span,start_freq):
     inst.write('SPAN '+ str(span) + '\n')
     inst.write('STRF '+ str(start_freq) + '\n')
     inst.write("STRT?\n")
     inst.write("STCO?\n")

def show_frequency():
    print("Start Fr, Centre Fr, Span is:\n")
    print(inst.write('STRF?\n'))
    print(inst.write('CTRF?\n'))
    print(inst.write('SPAN?\n'))
