import smbus
import time

class test:
    
    def __init__(self, address_STM32, acc, bus=1):
        
        self.bus = smbus.SMBus(bus)
        self.address = address_STM32 
        self.acc = acc
        
    def get_scalefactor(self):
        
        #Setting the scalefactor for each Force Sensitivity Level
        
        if self.acc == 2:
            self.scalefactor = 16384.0
            
        elif self.acc == 4:
            self.scalefactor = 8192.0
            
        elif self.acc == 8:
            self.scalefactor = 4096.0
            
        elif self.acc == 16:
            self.scalefactor = 2048.0

        else:
            print("Invalid range input")
            
    def write_number(self,value):
        self.get_scalefactor()
        
        #Enter values between given ranges as this will allows us to enter signed values from -32768 to +32767
        #Then turn this into an unisigned 16 bit number that will be sent to the STM32 with the 8 bit high and 8 bit low
        
        
        Bvalue = (float(value)/9.8)*self.scalefactor
        
        if(Bvalue < 0):
            
            # e.g. This equation is being solved -8359 = -((65535-value)+1)
            #Getting the unsigned 16-bit number
        
            Nvalue = int(65535 - ((Bvalue/-1)+1))
            
            #The 16-bit number is being split up into two 8-bit numbers holding the high 8-bits and the low 8-bits 
            
            BHvalue = Nvalue >> 8
            BLvalue = Nvalue & 0xff
            
        else:
            BHvalue = int(Bvalue) >> 8 
            BLvalue = int(Bvalue) & 0xff   
        
        #Writing the high and low 8-bits values to the microcontroller
            
        self.bus.write_byte_data(self.address, BHvalue,BLvalue)
        print(BHvalue,BLvalue)
        time.sleep(0.5)

    def write_bytes(self):
        
        #Defining input values based on sensitivitiy ranges 
        
        print("--------------------------------------------")
        print("Enter values based on the following ranges; ")
        print("Enter values -19 -> 19 for 2g range")
        print("Enter values -38 -> 38 for 4g range")
        print("Enter values -76 -> 76 for 8g range")
        print("Enter values -152 -> 152 for 16g range")
        print("--------------------------------------------")
    
        x = (input("Enter x acceleration: "))
        y = (input("Enter y acceleration: "))
        z = (input("Enter z acceleration: "))
        
        #Writing the 16 bit unsigned numbers to the microcontroller for each x,y,z acceleration 
        
        self.write_number(x)
        self.write_number(y)
        self.write_number(z)
        
        return -1

obj = test(0x04,2)
obj.write_bytes()




            
            
            
        
    




    
    
    

