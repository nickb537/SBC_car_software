from pwmmotorcontroller import PWMMotorController
import time

class FourWheelDriveController:
    def __init__(self):
        # Create motor instances
        self.fl_motor = PWMMotorController(positive_pin=17, negative_pin=27)
        self.fr_motor = PWMMotorController(positive_pin=22, negative_pin=10)
        self.rl_motor = PWMMotorController(positive_pin=5, negative_pin=0)
        self.rr_motor = PWMMotorController(positive_pin=13, negative_pin=6)

    def set_speeds(self, front_back_speed, left_right_speed):
        # Calculate motor speeds based on front/back and left/right speeds
        fl_speed = front_back_speed + left_right_speed
        fr_speed = front_back_speed - left_right_speed
        rl_speed = front_back_speed + left_right_speed
        rr_speed = front_back_speed - left_right_speed

        # Set speeds for each motor
        self.fl_motor.set_speed(fl_speed)
        self.fr_motor.set_speed(fr_speed)
        self.rl_motor.set_speed(rl_speed)
        self.rr_motor.set_speed(rr_speed)

    def stop_motors(self):
        # Stop all motors
        self.fl_motor.set_speed(0)
        self.fr_motor.set_speed(0)
        self.rl_motor.set_speed(0)
        self.rr_motor.set_speed(0)

    def cleanup(self):
        # Cleanup all motors
        print("stupid cleanup")
        self.fl_motor.cleanup()
        self.fr_motor.cleanup()
        self.rl_motor.cleanup()
        self.rr_motor.cleanup()

# Example usage
if __name__ == "__main__":
    car = FourWheelDriveController()

    # Move forward
    car.set_speeds(front_back_speed=0.5, left_right_speed=0)

    # Wait for some time
    time.sleep(2)

    #Turn right
    car.set_speeds(0,0.5)
    time.sleep(2)

    # Stop the motors
    car.stop_motors()

