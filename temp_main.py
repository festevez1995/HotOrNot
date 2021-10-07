'''
@file temp_main.py
@brief A file that runs on the Nucleo L476
@details A file that records temperature values using a MCP9808 sensor using the TempSensor Class
@author Kevin Lee and Fernando Estevez
@date February 9, 2021
'''


from Lab_4_mcp9808 import TempSensor
from pyb import I2C

##I2C address
address = 24
##I2C object
i2c = I2C(1, I2C.MASTER)   
##TempSensor Object
t = TempSensor(i2c,address)
t.loop()