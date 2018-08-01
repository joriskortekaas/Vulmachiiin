from wiringpi import *
from motor import Motor
import time

#Connect Ultrasonic to 5V, line detection to 3,3V!
class IO_controller():

    def __init__ (self, trigPin, echoPin):
    # Ultrasonic sensors pins
        self.motor1 = Motor(12,2,3) #rechtsachter
        self.motor2 = Motor(20,4,14) #rechtsvoor
        self.motor3 = Motor(26,15,18) #linksachter
        self.motor4 = Motor(16,27,17) #linksvoor

        wiringPiSetupGpio()
        print("IO controller initialised")
        pinMode(trigPin, 1)
        pinMode(echoPin, 1)
        self.trigPin = trigPin
        self.echoPin = echoPin
        
        self.blackPin = 21
        self.greyPin = 19
        self.whitePin = 6
        pinMode(self.blackPin,0)
        pinMode(self.greyPin, 0)
        pinMode(self.whitePin, 0)

    # Measure distance using ultrasonic sensor
    def measure_distance(self):
        # set Trigger to HIGH
        digitalWrite(self.trigPin, 1)
        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        digitalWrite(self.trigPin, 0)
        StartTime = time.time()
        StopTime = time.time()
        # save StartTime
        while digitalRead(self.echoPin) == 0:
            StartTime = time.time()
        # save time of arrival
        while digitalRead(self.echoPin) == 1:
            StopTime = time.time()
        # time difference between start and arrival
        TimeElapsed = StopTime - StartTime
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distance = (TimeElapsed * 34300) / 2
        #print("distance: " + distance + " cm")
        return distance

    # Detect lines and nodes
    def detect_node(self):
        print(digitalRead(self.whitePin)) 
      
        if digitalRead(self.greyPin):
            print("grey") 
            return "ground"
        elif digitalRead(self.blackPin):
            print("black")
            return "line"            
        elif digitalRead(self.whitePin):
            print("white")
            return "node"

    def forward(self, secs):
        self.stop()        
        self.motor1.forward()
        self.motor2.forward()
        self.motor3.forward()
        self.motor4.forward()
        time.sleep(secs)
        self.stop()
                       
    def reverse(self,secs):
        self.stop()
        self.motor1.reverse()
        self.motor2.reverse()
        self.motor3.reverse()
        self.motor4.reverse()
        time.sleep(secs)
        self.stop()

    def right(self):
        self.stop()
        self.motor1.reverse()
        self.motor2.reverse()
        self.motor3.forward()
        self.motor4.forward()
        time.sleep(2)
        self.stop()

    def left(self):
        self.stop()
        self.motor1.forward()
        self.motor2.forward()
        self.motor3.reverse()
        self.motor4.reverse()   
        time.sleep(1.4)
        self.stop()

    def stop(self):
        self.motor1.stop()
        self.motor2.stop()
        self.motor3.stop()
        self.motor4.stop()
        time.sleep(0.5)

io = IO_controller(23,24)
io.forward(3.6)
io.right()

