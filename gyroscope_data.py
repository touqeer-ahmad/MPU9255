#Library
import smbus

#Initiliazation of I2C bus
bus = smbus.SMBus(1)
address = 0x68       # Sensor I2C address

# Register address from MPU 9255 register map
power_mgmt_1 = 0x6b
gyro_config = 0x1b
gyro_xout_h = 0x43
gyro_yout_h = 0x45
gyro_zout_h = 0x47

# Setting power register to start getting sesnor data
bus.write_byte_data(address, power_mgmt_1, 0)

# Setting gyroscope register to set the sensitivity
# 0,8,16 and 24 for 131,65.5,32.8 and 16.4 sensitivity respectively
bus.write_byte_data(address, gyro_config, 24)

#Function to read byte and word and then convert 2's compliment data to integer
def read_byte(adr):
    return bus.read_byte_data(address, adr)

def read_word(adr):
    high = bus.read_byte_data(address, adr)
    low = bus.read_byte_data(address, adr+1)
    val = (high << 8) + low
    return val

def read_word_2c(adr):
    val = read_word(adr)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val

print "Raw and Scaled Acelerometer data\n"

gyro_xout = read_word_2c(gyro_xout_h) #We just need to put H byte address
gyro_yout = read_word_2c(gyro_yout_h) #as we are reading the word data
gyro_zout = read_word_2c(gyro_zout_h)

gyro_xout_scaled = gyro_xout / 16.4 #According to the sensitivity you set
gyro_yout_scaled = gyro_yout / 16.4
gyro_zout_scaled = gyro_zout / 16.4

print "X>\t Raw: ", gyro_xout, "\t Scaled: ", gyro_xout_scaled
print "Y>\t Raw: ", gyro_yout, "\t Scaled: ", gyro_yout_scaled
print "Z>\t Raw: ", gyro_zout, "\t Scaled: ", gyro_zout_scaled
