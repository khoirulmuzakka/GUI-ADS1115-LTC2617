"""
Created by : Stefan Rummel

"""




import smbus
import time

#FIRST_MUX_ADD=0x76

#MUX_DISABLE=0b0
#MUX_PORT0=0b00000100
#MUX_PORT1=0b00000101
#MUX_PORT2=0b00000110
#MUX_PORT3=0b00000111

#PORT_PJ2=MUX_PORT3
#PORT_PJ1=MUX_PORT0

# each controller is idenified by its adress an branch position

class CRATE_SYSTEM:
    def __init__(self,I2C_INTER):
        self.INTER=I2C_INTER
        self.CTR_LST=()
    def ADD_CTRL(self,branch,address):
        state=0
        pos=(branch,address,state)
        self.CTR_LST.add(pos)
        
    def CHECK_CTR(self,ID):
        if self.CTR_LST[ID].CHECK()==1:
            print ("crate controller found")
        # set state ok
    def CHECK_SYSTEM(self):
        print ("check sysystem")
        # loop over all controller
        # crosscheck state vs. actual    

# unique id for each controller
# initialize functionality



class CRATE_CONTROLLER:
    def __init__(self,Adress,interface):
        self.SILENT=1
        self.CONTROLLER_ADD=Adress
        self.REF_ADC=1890
        self.FS_ADC=4095
        self.PI2C_INTERFACE=interface
        self.IC_ADD= { "ADC": 0b01001000 , "DAC":0b10011010 , "IO":0x21} #I2C Adress of each IC
        self.Ports={"ADC": 0b00000001, "DAC":0b00000010, "IO":0b00000000} # Mulitplexer output which refers to each IC
        self.MUX_EN=0b00000100
        self.MUX_DIS=0b00000000
        # ADC channel + Ext_REF + ADC ON Bits + Single Ended Measurement
        self.ADC_CH={0:0x84,1:0xC4,2:0x94,3:0xD4,4:0xA4,5:0xE4,6:0xB5,7:0xF4} 
        #Funktional assingment between ADC Channel and Switches / temp input
        self.SW_CH_ASS={"SW1":"CH4","SW2":"CH3","SW3":"CH2","SW4":"CH1","FAN":"CH0","TEMP":"CH5"}
        # callibration data for each channel offset (mA,dev from nominal gain 1.2 means 20% more)
        self.CAL_DAT=((0,1),(0,1),(0,1),(0,1),(0,1)) #(offset,gain corretion factor)
        # GPIO St
        self.GPIO_STATE=0
        self.CONF_GPIO() # configure outputs sets everything to 0
        
    def SET_UREF(self,volt_mv):
        self.REF_ADC=volt_mv
        
    def SET_CAL_DEFAULT(self):
        for entry in self.CAL_DAT:
            entry[0]=0
            entry[1]=1
   
            
    def SET_CAL(self,channel,offset,gain_corr):
        self.CAL_DAT[channel-1][0]=offset
        self.CAL_DAT[channel-1][1]=gain_corr
                
    def SEL(self,IC):        
        # enable I2c mulitplexer and set output
        #print "write byte to: ",self.CONTROLLER_ADD," PORT: ",self.Ports[IC]
        data=self.Ports[IC]|self.MUX_EN
        #print data
        self.PI2C_INTERFACE.write_byte(self.CONTROLLER_ADD,data)
    def DSEL(self,IC):
        # disable i2c multiplexer 
        self.PI2C_INTERFACE.write_byte(self.CONTROLLER_ADD,self.Ports[IC]|self.MUX_DIS)

    def CONF_GPIO(self):
        self.SEL("IO")
        
        # check current state
        port0_conf=self.PI2C_INTERFACE.read_byte_data(self.IC_ADD["IO"],0x06)
        port1_conf=self.PI2C_INTERFACE.read_byte_data(self.IC_ADD["IO"],0x07)
        print ("Current Configuration: ",port0_conf,",",port1_conf)
        
        if (port0_conf==0xFF) & (port1_conf==0xFF):
            print ("POWER UP CONFIGURATION DETECTED")
            self.PI2C_INTERFACE.write_byte_data(self.IC_ADD["IO"],0x02,0x00) # set registers with outputvalues to 0
            self.PI2C_INTERFACE.write_byte_data(self.IC_ADD["IO"],0x03,0x00) # dito
            print (self.PI2C_INTERFACE.write_byte_data(self.IC_ADD["IO"],0x06,0x00)) # set port mode 0 output 1 input aka floating
            print (self.PI2C_INTERFACE.write_byte_data(self.IC_ADD["IO"],0x07,0x00)) # dito

        if (port0_conf==0x00) & (port1_conf==0x00):
            print ("PROPER CONFIGURATION DETECTED")
        
        print ("Outputstate, Port 0: ", self.PI2C_INTERFACE.read_byte_data(self.IC_ADD["IO"],0x00))
        print ("Outputstate, Port 1: ",self.PI2C_INTERFACE.read_byte_data(self.IC_ADD["IO"],0x01))

        time.sleep(.2)
        self.DSEL("IO")
    
    def GET_GPIO(self,port,channel):
        self.SEL("IO")
        state=self.PI2C_INTERFACE.read_byte_data(self.IC_ADD["IO"],port)
        self.DSEL("IO")
        intermed=(state>>(channel))
        state=1&intermed
        #print "GPIO Port: ",port," Channel: ", state
        return state
                
    def GET_SLOT_STATE(self,slot):
        return self.GET_GPIO(0,slot-1)

    def SET_GPIO(self,port,channel,value):
        # set gpio channel on off
        self.SEL("IO")

        status=self.PI2C_INTERFACE.read_byte_data(self.IC_ADD["IO"],0x00+port)
        #print status
        chZero=status&(~(1<<channel))
        #chZero=status & POS
        chValue=(value<<channel)
        newVal=chValue|chZero
        #print newVal
        self.PI2C_INTERFACE.write_byte_data(self.IC_ADD["IO"],0x02+port,newVal)        

        self.DSEL("IO")
    
    def RESET_PS(self,unit):
        # all resets are connected to Port 1
        if self.SILENT==0:
            print( "RESET SLOT: ", unit)
        self.SET_GPIO(1,unit-1,1)
        time.sleep(.05)
        self.SET_GPIO(1,unit-1,0)    
    def SWITCH_PS(self,unit,state):
        plain="ND"
        if state==1: plain="ON"
        if state==0: plain="OFF"
        print ("SET SLOT ",unit," to ",plain)
        self.SET_GPIO(0,unit-1,state)
        

    def SET_DAC(self,value):
        self.SEL("DAC")
        
        self.DSEL("DAC")

    def GET_ADC_RAW(self,channel):
        
        self.SEL("ADC")
        if self.SILENT==0:
            print ("read data from address: ",self.IC_ADD["ADC"]," Channel: ",self.ADC_CH[channel])
        RAW=self.PI2C_INTERFACE.read_word_data(self.IC_ADD["ADC"],self.ADC_CH[channel])    
        first=(RAW&0x00FF)<<8
        last=(RAW&0xFF00)>>8
        
        self.DSEL("ADC")    
        return (first+last)

    def GET_ADC_VOLT(self,channel):
        FS=4095
        return (self.REF_ADC*self.GET_ADC_RAW(channel)/self.FS_ADC)        

    def GET_SLOT_CURRENT(self,slot):
        Rs=1000
        Ratio=2800
        return ((self.GET_ADC_VOLT(5-slot)*Ratio/Rs)*self.CAL_DAT[slot-1][1]-self.CAL_DAT[slot-1][0])    
            
    def GET_CUR(self,channel):
        current=(self.GET_ADC_RAW(channel)*self.CAL_DAT[channel-1][1])-self.CAL_DAT[channel-1][0]
        return current

    

class PI2C_INTERFACE:
    def __init__(self,bus,address):
        self.PORT_PJ1=0b00000111
        self.PORT_PJ2=0b00000100
        self.BRANCH_MUX_ADD=address
        self.bus=smbus.SMBus(bus)
        self.assingment=0
        self.ERROR_CTR=0
    def write_quick(self,adress):
        try:
            self.bus.write_quick(adress)
            return 1
        except:
            return 0

    def write_byte(self,adress,data):
        try:
            self.bus.write_byte(adress,data)
        except:
            print ("I2C ERROR AT ADRESS: ",adress)
            self.ERROR_CTR+=1
            pass

    def write_word_data(self,adress,cmd,data):
        try:
            return self.bus.write_word_data(adress,cmd,data)
        except:
            self.ERROR_CTR+=1
            print ("I2C ERROR AT ADRESS: ",adress)
            return 0
            
    def write_byte_data(self,adress,cmd,data):
        try: 
            return self.bus.write_byte_data(adress,cmd,data)
        except:
            self.ERROR_CTR+=1
            print ("I2C ERROR AT ADRESS: ",adress)
            pass

    def read_byte_data(self,adress,data):
        try:
            return self.bus.read_byte_data(adress,data)
        except:
            print ("I2C ERROR AT ADRESS: ",adress)
            return 0

    def read_word_data(self,adress,cmd):
        try:
            return self.bus.read_word_data(adress,cmd)
        except:    
            self.ERROR_CTR+=1
            print ("I2C ERROR AT ADRESS: ",adress)
            return 0

    def SEL_BRANCH(self,branch):
        if branch=="left":
            print ("SET LEFT BRANCH")
            self.write_byte(self.BRANCH_MUX_ADD,self.PORT_PJ2)
        if branch=="right":
            print ("SET RIGHT BRANCH")
            self.write_byte(self.BRANCH_MUX_ADD,self.PORT_PJ1)    
        
    def DSEL(self):
        print ("DISABLE PI2C MUX")
        self.write_byte(self.BRANCH_MUX_ADD,0)

    def PING(self,address):
        try:
            self.write_quick(adress)
            return 1
        except:
            return 0

    def SCAN(self):
        for i in xrange(0x03,0x78):
            try:
                time.sleep(0.02)
                self.bus.write_quick(i)
                print ("found adress at", i)
            except:
                pass
    



if __name__=='__main__':

    PI2C=PI2C_INTERFACE(1,0x76)

    PI2C.SEL_BRANCH("right")

    PI2C.SCAN()

    CRT=CRATE_CONTROLLER(0x70,PI2C)

    for i in xrange(0,10):

        #val=CRT.GET_ADC_RAW("CH6")
    
        CRT.SET_GPIO(0,1,1) # (PORT, Channel, Value)
        #time.sleep(.01)
        CRT.SET_GPIO(0,1,0) # (PORT, Channel, Value)
    
        #time.sleep(.1)
        #print "Voltage: ",val*REF/FS," RAW: ",val


    CRT.SWITCH_PS(3,1)
    print (CRT.GET_SLOT_STATE(3))
    time.sleep(4)

    CRT.SWITCH_PS(3,0)
    print (CRT.GET_SLOT_STATE(3))


