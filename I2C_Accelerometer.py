import smbus
import time

class Accelerometer:
    
    GRAVITY = 9.80665
    
    ADDRESS = 0x68
    ACCEL_CONFIG = 0x1C
    ACCEL_XOUT = 0x3B
    ACCEL_YOUT = 0x3D
    ACCEL_ZOUT = 0x3F
    SMPLRT_DIV = 0x19
    CONFIG = 0x1A
    INT_ENABLE = 0x38
    
    PWR_MGMT_1 = 0x6B
            
    def __init__(self, address, acc,bus=1):
      
        self.bus = smbus.SMBus(bus)
        time.sleep(0.1)
        self.address = address
        self.acc = acc
        
    def accelerometer_range_scalefactor(self):
        
        #Setting the scalefactor for each Force Sensitivity Level
        
        if self.acc == 2:
            self.scalefactor = 16384.0
            self.range = 0x00
            
        elif self.acc == 4:
            self.scalefactor = 8192.0
            self.range = 0x08
            
        elif self.acc == 8:
            self.scalefactor = 4096.0
            self.range = 0x10
            
        elif self.acc == 16:
            self.scalefactor = 2048.0
            self.range = 0x18
            
        else:
            print("Invalid range input")
            
    def accelerometer_setup(self):
        
        #Here the registers in the accelerometer are being enabled for data to be collected
        
        if (self.address == self.ADDRESS): 
            self.accelerometer_range_scalefactor()
            
            self.bus.write_byte_data(self.address, self.SMPLRT_DIV, 0)
            time.sleep(0.5)
            self.bus.write_byte_data(self.address, self.PWR_MGMT_1, 0x00)
            time.sleep(0.5)
            self.bus.write_byte_data(self.address, self.PWR_MGMT_1, 0x01)
            time.sleep(0.5)
            self.bus.write_byte_data(self.address, self.CONFIG, 0)
            time.sleep(0.5)
            
            #Once the ACCEL_CONFIG register is configured, data is being written 
            #Data is being collected in the x,y,z registers 
            
            self.bus.write_byte_data(self.address, self.ACCEL_CONFIG, self.range) 
            time.sleep(0.5)
            self.bus.write_byte_data(self.address,self.INT_ENABLE,1)
            time.sleep(0.5)
            
            print("------------------------------------------------------")
            
            print("ACCELEROMETER SETUP COMPLETE....")
            print("ACCELEROMETER RANGE ENTERED:" + str(self.acc))
            print("ACCELEROMETER SCALEFACTOR:" + str(self.scalefactor))
            
            print("------------------------------------------------------")
            time.sleep(5)
            
        else:
            print("Wrong device address")
        
    def conv_bit(self,register):
        
        #Data is being read from the x,y,z registers as a 16 bit unsigned value
        #For each plane (x,y,z) there are two registers collecting data
        #One registers stores the 8 high-bits of the unsigned value
        #The second one stores 8 low-bits of the unsigned value
        #Together making the unsigned 16 bit value
        
        if (self.address == self.ADDRESS):
            
            #Reads high and low 8 bit values and shifts them into 16 bit
            
            high = self.bus.read_byte_data(self.address, register)
            low = self.bus.read_byte_data(self.address, register +1) #register +1 is to access low-bit value
            
            #Making 16 bit value shifting high by 8 to left 

            value = (high << 8) + low
            
            #Making 16 bit unsigned value to signed value
            #(0 -> 65535) into (-32768 -> +32767)
            
            if (value >= 0x8000): #32768
                return -((65535 - value) + 1)
            else:
                return value
        else:
            print("Wrong device address")
    
    def getAccelerometerData(self):
        
        #Here the data for each acceleration direction (x,y,z) is being read and converted to signed 16 bit value
        
        ax = self.conv_bit(self.ACCEL_XOUT)
        ay = self.conv_bit(self.ACCEL_YOUT)
        az = self.conv_bit(self.ACCEL_ZOUT)
        
        # Signed 16 bit value is converted into G force
        
        x = round((ax/self.scalefactor)*self.GRAVITY,3)
        y = round((ay/self.scalefactor)*self.GRAVITY,3)
        z = round((az/self.scalefactor)*self.GRAVITY,3)
        
        return ax,ay,az

    def Accelerometer_Data(self, t):
        
        self.accelerometer_setup()
        startTime = time.time()
        while(time.time() < (startTime + t)):
            print(self.getAccelerometerData())
        print("\n--------------------------------")
        print("Closing")
        
mpu = Accelerometer(0x68,2 )
mpu.Accelerometer_Data(60)


         