import smbus
import time

class STC3100:
    def __init__(self, i2c_address=0x70, i2c_bus=1):
        self.i2c_address = i2c_address
        self.i2c_bus = smbus.SMBus(i2c_bus)
        self.i2c_bus.write_byte_data(i2c_address,1,0b1) 
        self.i2c_bus.write_byte_data(i2c_address,0,0b00010000) #put in operating mode
        #print("Reg mode is: ", bin(self.i2c_bus.read_byte_data(i2c_address,0)))

    def read_register(self, register):
        return self.i2c_bus.read_word_data(self.i2c_address, register)

    def write_register(self, register, data):
        self.i2c_bus.write_word_data(self.i2c_address, register, data)

    def get_voltage(self):
        # Read battery voltage from the STC3100
        voltage_raw = self.read_register(0x08)
        #print("Raw voltage reading: ", voltage_raw)
        voltage = voltage_raw * 2.44e-3  # V
        return voltage

    def get_current(self):
        # Read battery current from the STC3100
        current_raw = self.read_register(0x06)
        current = current_raw * 2.5e-3  #LSB = 2.5 mA
        return current

    def get_temperature(self):
        # Read battery temperature from the STC3100
        temperature_raw = self.read_register(0x0A)
        temperature = temperature_raw * 0.125  # LSB = 0.125 C
        return temperature

    def get_battery_capacity(self):
        # Read battery capacity (fuel gauge) from the STC3100
        capacity_raw = self.read_register(0x02)
        return capacity_raw *  6.7e-6 / 10e-3 # A h



    def write_to_ram(self, register, data):
        # Write data to the specified RAM register
        self.write_register(register, data)

    def read_from_ram(self, register):
        # Read data from the specified RAM register
        return self.read_register(register)

# Example usage
if __name__ == "__main__":
    stc3100 = STC3100()
    
    try:
        # Choose a RAM register to test (e.g., REG_RAM0)
        ram_register = 0x20  # Replace with the desired RAM register address

        # Value to write to the RAM register for testing
        test_data = 0xBEEF  # Replace with the desired test data

        # Perform the test: Write and read from the selected RAM register
        stc3100.write_to_ram(ram_register, test_data)
        read_data = stc3100.read_from_ram(ram_register)

        # Print the results
        print("Test Data Written: 0x{:04X}".format(test_data))
        print("Data Read from RAM: 0x{:04X}".format(read_data))
        
        print("Device ID: ", stc3100.read_from_ram(24))
    except IOError as e:
        print("Error communicating with STC3100: {}".format(e))
    
    try:
        # Read and print battery information
        print("Battery Voltage: {:.2f} V".format(stc3100.get_voltage()))
        print("Battery Current: {:.2f} mA".format(stc3100.get_current()))
        print("Battery Temperature: {:.2f} °C".format(stc3100.get_temperature()))
        print("Battery Capacity: {}".format(stc3100.get_battery_capacity()))

    except IOError as e:
        print("Error reading from STC3100: {}".format(e))

    finally:
        # Cleanup when done
        stc3100.i2c_bus.close()
