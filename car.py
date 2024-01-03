import pigpio
import time
from fourwheeldrivecontroller import FourWheelDriveController
from stc3100 import STC3100

START_SPEED = 0.4
MAX_SPEED = 0.5
SPEED_INCREMENT = 0.01
			
class HeadlightsController:
    def __init__(self, headlights_pin=26):
        self.pi = pigpio.pi()
        self.headlights_pin = headlights_pin
        self.status = 1 #1 for on 0 for off

        # Setup GPIO pin for headlights
        self.pi.set_mode(self.headlights_pin, pigpio.OUTPUT)

    def turn_on(self):
        # Turn on the headlights
        self.pi.write(self.headlights_pin, 1)
        self.status = 1

    def turn_off(self):
        # Turn off the headlights
        self.pi.write(self.headlights_pin, 0)
        self.status = 0

    def toggle(self):
        if self.status:
            self.turn_off()
        else:
            self.turn_on()

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

        self.speed = 0
        self.turn = 0

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

    def handle_arrow_key_action(self, action):
        if action == "up_pressed":
            print("Up arrow key pressed")
            if self.speed <= 0:
                self.speed = START_SPEED
            else:
                self.speed += SPEED_INCREMENT

            if self.speed > MAX_SPEED:
                self.speed = MAX_SPEED

        elif action == "up_released":
            print("Up arrow key released")
            self.speed = 0

        elif action == "down_pressed":
            if self.speed >= 0:
                self.speed = -START_SPEED
            else:
                self.speed -= SPEED_INCREMENT

            if self.speed < -MAX_SPEED:
                self.speed = -MAX_SPEED

        elif action == "down_released":
            self.speed = 0


        elif action == "left_pressed":
            if self.turn >= 0:
                self.turn = -START_SPEED
            else:
                self.turn -= SPEED_INCREMENT

            if self.turn < -MAX_SPEED:
                self.turn = -MAX_SPEED

        elif action == "left_released":
            self.turn = 0

        elif action == "right_pressed":
            if self.turn <= 0:
                self.turn = START_SPEED
            else:
                self.turn = SPEED_INCREMENT

            if self.turn > MAX_SPEED:
                self.turn = MAX_SPEED

        elif action == "right_released":
            self.turn = 0

        if action == "space_pressed":
            if action == "space_pressed":
                self.headlights_controller.toggle()
                
        self.drive(self.speed,self.turn) #I just like turning to be slower

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
        #car.cleanup()
