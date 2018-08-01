from motor import Motor
import time


#Connect Ultrasonic to 5V, line detection to 3,3V!
class IO_controller():

    # Ultrasonic sensors pins
    motor1 = Motor(1,1,1)
    motor2 = Motor(1,1,1)
    motor3 = Motor(1,1,1)
    motor4 = Motor(1,1,1)
    trigPinPin = Pin(15, Pin.OUT)
    echoPin = Pin(13, Pin.IN)

    # Analog pin used for line detection sensor (PIN VP ON ESP32!)
    adc = machine.ADC(machine.Pin(36))

    def __init__(self):
        print("IO controller initialised")

    # Measure distance using ultrasonic sensor
    def measure_distance(self):
        self.trigPin.off()
        time.sleep_us(2)
        self.trigPin.on()
        time.sleep_us(10)
        self.trigPin.off()
        while self.echoPin.value() == 0:
            pass
        t1 = time.ticks_us()
        while self.echoPin.value() == 1:
            pass
        t2 = time.ticks_us()
        cm = (t2 - t1) / 58.0
        print(cm)
        time.sleep(0.5)
        return cm

    # Check for obstacles
    def check_obstacles(self):
        # if there is an obstacle
        if self.measure_distance() < 20:
            self.control_motors()
        else:
            return

    # Detect lines and nodes
    def detect_node(self):
        value = self.adc.read()
        print(value)
        if(value == 1000):
            return "line"
        elif(value == 2000):
            return "node"
        # If value is between somethings its a line

    # Control the motors to make the robot turn/move forwards
    def control_motors(self, angle):
        if angle == 0:
            print('forward')
        elif angle == 90:
            print('right')
        elif angle == -90:
            print('left')

        # TODO DAARNA RECHTDOOR
