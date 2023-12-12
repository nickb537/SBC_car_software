import pigpio

import FourWheelDriveController from FourWheelDriveController
			
class HeadlightsController:
    def __init__(self, headlights_pin=26):
        self.pi = pigpio.pi()
        self.headlights_pin = headlights_pin

        # Setup GPIO pin for headlights
        self.pi.set_mode(self.headlights_pin, pigpio.OUTPUT)

    def turn_on(self):
        # Turn on the headlights
        self.pi.write(self.headlights_pin, 1)

    def turn_off(self):
        # Turn off the headlights
        self.pi.write(self.headlights_pin, 0)

    def cleanup(self):
        # Cleanup GPIO before exiting
        self.turn_off()
        self.pi.stop()


class Car:
    def __init__(self):
        # Instantiate components
        self.drive_controller = FourWheelDriveController()
        self.headlights_controller = HeadlightsController()
        self.battery_monitor = STC3100()

    def drive(self, front_back_speed, left_right_speed):
        # Control the car's movement
        self.drive_controller.set_speeds(front_back_speed, left_right_speed)

    def turn_on_headlights(self):
        # Turn on the headlights
        self.headlights_controller.turn_on()

    def turn_off_headlights(self):
        # Turn off the headlights
        self.headlights_controller.turn_off()

    def read_battery_info(self):
        # Read and print battery information
        print("Battery Voltage: {:.2f} V".format(self.battery_monitor.get_voltage()))
        print("Battery Current: {:.2f} mA".format(self.battery_monitor.get_current()))
        print("Battery Temperature: {:.2f} °C".format(self.battery_monitor.get_temperature()))
        print("Battery Capacity: {}".format(self.battery_monitor.get_battery_capacity()))

    def stop(self):
        # Stop the car's movement
        self.drive_controller.stop_motors()

    def cleanup(self):
        # Cleanup all components
        self.drive_controller.cleanup()
        self.headlights_controller.cleanup()
        self.battery_monitor.i2c_bus.close()

# Example usage
if __name__ == "__main__":
    car = Car()

    try:
        # Drive forward with headlights on
        car.turn_on_headlights()
        car.drive(front_back_speed=0.5, left_right_speed=0)
        time.sleep(2)  # Keep moving forward for 2 seconds

        # Drive backward with headlights off
        car.turn_off_headlights()
        car.drive(front_back_speed=-0.5, left_right_speed=0)
        time.sleep(2)  # Keep moving backward for 2 seconds

        # Read battery information
        car.read_battery_info()

    finally:
        # Stop the car and perform cleanup
        car.stop()
        car.cleanup()