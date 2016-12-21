import wiringpi
import os
import struct
import json
from time import sleep

class Hdc1000:

    def __init__(self):
        wiringpi.wiringPiSetup()
        self.i2c = wiringpi.I2C()

    def getHumidity(self):
        self.dev = self.i2c.setup(0x40)
        self.i2c.writeReg16(self.dev, 0x02, 0x10) # Temp + Hidi 32-bit transfer mode, LSB-MSB inverted why?
        self.i2c.writeReg8(self.dev, 0x00, 0x00) # Start conversion
        sleep((6350.0 + 6500.0 + 500.0)/1000000.0) # Wait for conversion
        #LSB-MSB inverted, again...
        self.temp = ((struct.unpack('4B', os.read(self.dev, 4)))[0] << 8 | (struct.unpack('4B', os.read(self.dev, 4)))[1])
        self.hudi = ((struct.unpack('4B', os.read(self.dev, 4)))[2] << 8 | (struct.unpack('4B', os.read(self.dev, 4)))[3])
        os.close(self.dev) # Don't leave the door open.
        return ((self.hudi / 65535.0) * 100)

    def getTemperature(self):
        self.dev = self.i2c.setup(0x40)
        self.i2c.writeReg16(self.dev, 0x02, 0x10) # Temp + Hidi 32-bit transfer mode, LSB-MSB inverted why?
        self.i2c.writeReg8(self.dev, 0x00, 0x00) # Start conversion
        sleep((6350.0 + 6500.0 + 500.0)/1000000.0) # Wait for conversion
        #LSB-MSB inverted, again...
        self.temp = ((struct.unpack('4B', os.read(self.dev, 4)))[0] << 8 | (struct.unpack('4B', os.read(self.dev, 4)))[1])
        self.hudi = ((struct.unpack('4B', os.read(self.dev, 4)))[2] << 8 | (struct.unpack('4B', os.read(self.dev, 4)))[3])
        os.close(self.dev) # Don't leave the door open.
        return ((self.temp / 65535.0) * 165 - 40)

oHdc1000=Hdc1000()

dict = {}
dict["Humidity"] = "%.2f" % oHdc1000.getHumidity()
dict["Temperature"] = "%.2f" % oHdc1000.getTemperature()
enc = json.dumps(dict)
print enc

