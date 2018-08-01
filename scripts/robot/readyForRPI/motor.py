from wiringpi import *

# Motor class
class Motor:

    # Initialises motor class
    def __init__(self, enpin, togglepinA, togglepinB):
        wiringPiSetupGpio()
        self.togglepinA = togglepinA
        self.togglepinB = togglepinB
        self.enpin = enpin
        pinMode(togglepinA, 1)
        pinMode(togglepinB, 1)
        pinMode(enpin, 1)
        digitalWrite(enpin, 1)

    # Makes the motor turn one way
    def forward(self):
        print("forward")
        digitalWrite(self.togglepinA, 1)
        digitalWrite(self.togglepinB, 0)

    # Makes the motor turn the opposite way
    def reverse(self):
        digitalWrite(self.togglepinA, 0)
        digitalWrite(self.togglepinB, 1)
   
    def stop(self):
        print("stop")
        digitalWrite(self.togglepinA, 0)
        digitalWrite(self.togglepinB, 0)
