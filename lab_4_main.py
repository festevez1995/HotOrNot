## @file lab_4_main.py
#  Brief doc for lab_4_main.py
#
#  Detailed doc for lab_4_main.py
#  This is the program for the temperature sensor
#
#  @author Kevin Andrew Lee and Fernando Estevez
#
#  @copyright License Info
#
#  @date Febuary 6, 2021
import mcp9808 
import utime
import pyb
from pyb import I2C

MAX_TIME = 28800000 # 8hrs in ms
ONE_MINUTE = 60000 # 1 minute in ms

def dataToCSV(time, tempS, tempN):
    i = 0
    size = len(tempS)
    with open("temp.csv", "w") as a_file:
        a_file.write('SensorTemp,NucleoTemp,Time\n')
        while i < size:
            a_file.write('{:},{:},{:}\n'.format(tempS[i], tempN[i], time[i]))
            i += 1
        
    

def main():
    global MAX_TIME, ONE_MINUTE
    # Holds time elapsed    
    tot_time = []
    # Holds the temperature from the sensor
    temp_list = []
    # holds the temperature from Nucleo
    nucleo_temp_list = []
    temp_reg = 5
    # Sets up an ADC object
    adc = pyb.ADCAll(12, 0x70000)
    # Sets up an i2c object
    i2c = I2C(1, I2C.MASTER)
    # Gets an array of addresses
    addr = i2c.scan()
    # Creates a temperature sensor object 
    sensor = mcp9808.mcp9808(i2c, addr[0], temp_reg)
    # Checks for the sensor
    sensor.check()
    # Will keep track of total elapsed time
    timeElapsed = 0
    lastTime = 0
    while True:
        try:
            if timeElapsed >= MAX_TIME:
                dataToCSV(tot_time, temp_list, nucleo_temp_list)
                break
            
            tempData = sensor.setData()
            # Reads the temp sensor in Fahrenheit
            tempSensor = sensor.fahrenheit(tempData)
            # Reads the Nucleo temperature
            tempNucleo = adc.read_core_temp()
            # Keeps track of the time elapsed
            start = utime.ticks_ms()
            # appends the sensors temp to our temp list
            temp_list.append(tempSensor)
            # appends the nucleos temp to out temp list
            nucleo_temp_list.append(tempNucleo)
            
            print("Temp: ", tempSensor)
            print("Temp of Nucleo: ", tempNucleo)
            # wait for a minute before reading again
            utime.sleep_ms(ONE_MINUTE)
            end = utime.ticks_ms()
            mytime = end - start
            # Appends the total elapsed time to our time list
            tot_time.append((mytime + lastTime) / ONE_MINUTE)
            lastTime = mytime + lastTime
            timeElapsed += ONE_MINUTE
        except KeyboardInterrupt:
            break
    

if __name__ == "__main__":
    main()
