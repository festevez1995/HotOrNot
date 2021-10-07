## @file mcp9808.py
#  Brief doc for mcp9808.py
#
#  Detailed doc for mcp9808.py
#  This is the program for the temperature sensor
#
#  @author Kevin Andrew Lee and Fernando Estevez
#
#  @copyright License Info
#
#  @date Febuary 6, 2021
import utime
from pyb import I2C

## A temperature Sensor Object
#
#  Details
#  @author Kevin Andrew Lee and Fernando Estevez
#  @copyright License Info
#  @date Febuary 6, 2021
class mcp9808:
    i2cInt = None
    address = 0
    temp_reg = 0
    
    ## Constructor
    #
    #  An initializer which is given a reference to an already created I2C 
    #  object and the address of the MCP9808 on the I2C bus.
    #  @param i2cInt, address, temp_reg
    def __init__(self, i2cInt, address, temp_reg):
        self.i2cInt = i2cInt
        self.address = address
        self.temp_reg = temp_reg
        
    ## Check function
    #
    #  verifies that the sensor is attached at the given bus address
    #  by checking that the value in the manufacturer ID register.
    #    
    def check(self):
        # Check if an I2C device responds to the given address.
        self.i2cInt.is_ready(self.address)
        self.i2cInt.recv(1,self.address)
    
    ## Set Data function
    #
    #  Sets up a buffer to read the data into.
    #  @return data. Returns the read data.
    def setData(self):
        # Sets up a data buffer
        # Reads 4 bytes at a given address. Stores it into a temp reg with in
        # the i2c device. sets timeout at 5000 and sets addr size to 8 bits.
        data = self.i2cInt.mem_read(4, self.address, self.temp_reg, 
                                         timeout=5000, addr_size=8)
        return data
    
    ## Temperature in Celsius function
    #
    #  Gets the data and returns the temperature in celsius.
    #  @param data. Read data 
    #  @return temp. Returns the temperature in Celsius.   
    def celsius(self, data):
        value = data[0] << 8 | data[1]
        temp = (value & 0xFFF) / 16.0
        if value & 0x1000:
            temp -= 256.0
        return temp
    
    ## Temperature in Fahrenheit function
    #
    #  Gets the data and returns the temperature in Fahrenheit.
    #  @param data. Read data
    #  @return temp. Returns the temperature in Fahrenheit.
    def fahrenheit(self, data):
        return (self.celsius(data) * 9/5) + 32

if __name__ == "__main__":
    """
    temp_reg = 5
    res_reg = 8
    
    i2c = I2C(1, I2C.MASTER)
    addr = i2c.scan()
    
    tempSensor = mcp9808(i2c, addr[0], temp_reg)
    tempSensor.check()
    
    while True:
        myData = tempSensor.setData()
        print(tempSensor.fahrenheit(myData))
        utime.sleep_ms(500)
        

    print(i2c.scan())
    print(i2c.is_ready(24))
    print(i2c.recv(1,24))
    """
    
