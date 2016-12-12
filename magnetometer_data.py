#Libraries and functions needed
import smbus
import math

#Initiliazation of I2C bus
bus = smbus.SMBus(1)
address = 0x68       # Sensor I2C address
address_mag = 0x0c  #Sensor address for magnetometer

# Register address from MPU 9255 register map
power_mgmt_1 = 0x6b
usr_cntrl = 0x6a
int_pin_conf = 0x37
cntrl = 0x0a
mag_xout_h = 0x03
mag_yout_h = 0x05
mag_zout_h = 0x07

#initialize the smbus for i2c communication
bus = smbus.SMBus(1)
#initialize the power registers to wake up sensor
bus.write_byte_data(address, power_mgmt_1, 0)
#disable master i2c mode of sensor
bus.write_byte_data(address, usr_cntrl, 0)
# enable bypass mode to read directly from magnetometer
bus.write_byte_data(address, int_pin_conf, 2)
# setup magnetic sensors for contiuously reading data
bus.write_byte_data(address_mag, 0x0a, 18)

def read_byte(address, adr):
    return bus.read_byte_data(address, adr)

def read_word_mag(address, adr):
    low = read_byte(address, adr)
    high = read_byte(address, adr+1)
    val = (high << 8) + low
    return val

def read_word_2c_mag(address, adr):
    val = read_word_mag(address, adr)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val

print "Raw and Scaled Magnetometer Data"

#Raw Magnetometer data
mag_xout = read_word_2c_mag(address_mag, mag_xout_h)
mag_yout = read_word_2c_mag(address_mag, mag_yout_h)
mag_zout = read_word_2c_mag(address_mag, mag_zout_h)

mag_xout_scaled = mag_xout / 0.6 #From data sheet, there is only
mag_yout_scaled = mag_yout / 0.6 #one sensitivity level for 
mag_zout_scaled = mag_zout / 0.6 #Magnetometer in MPU 9255

#Raw Magnetometer data scaling by 0.6 due to default sensitivity
print "X>\t Raw: ", mag_xout, "\tscaled: ", (mag_xout_scaled)
print "Y>\t Raw: ", mag_yout, "\tscaled: ", (mag_yout_scaled)
print "Z>\t Raw: ", mag_zout, "\tscaled: ", (mag_zout_scaled)
