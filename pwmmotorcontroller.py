import pigpio
import time

class PWMMotorController:
    def __init__(self, positive_pin, negative_pin):
        self.pi = pigpio.pi()
        self.positive_pin = positive_pin
        self.negative_pin = negative_pin
        
        # Setup GPIO pins
        self.pi.set_mode(self.positive_pin, pigpio.OUTPUT)
        self.pi.set_mode(self.negative_pin, pigpio.OUTPUT)
        self.pi.set_PWM_frequency(self.positive_pin, 1000)
        self.pi.set_PWM_frequency(self.negative_pin, 1000)
        
        # Initially set speed to 0
        self.set_speed(0)

    def set_speed(self, speed):
        if speed > 1:
            speed = 1
        elif speed < -1:
            speed = -1
        
        if speed == 0:
            self.pi.set_PWM_dutycycle(self.positive_pin, 0)
            self.pi.set_PWM_dutycycle(self.negative_pin, 0)
        elif speed > 0:
            self.pi.set_PWM_dutycycle(self.positive_pin, int(speed * 255))
            self.pi.set_PWM_dutycycle(self.negative_pin, 0)
        else:
            self.pi.set_PWM_dutycycle(self.positive_pin, 0)
            self.pi.set_PWM_dutycycle(self.negative_pin, int(abs(speed) * 255))


    def cleanup(self):
        # Cleanup GPIO before exiting
        self.pi.set_PWM_dutycycle(self.positive_pin, 0)
        self.pi.set_PWM_dutycycle(self.negative_pin, 0)
        self.pi.stop()
        return

    #def __del__(self):
        #self.cleanup()

# Example usage
if __name__ == "__main__":
    motor = PWMMotorController(positive_pin=17, negative_pin=27)

    try:
        print("Moving forward...")
        motor.set_speed(0.5)  # Move forward at half speed
        time.sleep(1)        # Keep moving forward for 1 second

        print("Moving backward...")
        motor.set_speed(-0.5)  # Move backward at half speed
        time.sleep(1)         # Keep moving backward for 1 second

        print("Stopping...")
        motor.set_speed(0)    # Stop the motor

    finally:
        # Cleanup when done
        del motor
