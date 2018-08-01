

# Motor class
class Motor:

    # Initialises motor class
    def __init__(self, PWMpin, togglepinA, togglepinB):
        self.togglepinA = Pin(togglepinA, Pin.OUT)
        self.togglepinB = Pin(togglepinB, Pin.OUT)
        self.PWMpin = PWM(Pin(PWMpin))

    # Changes frequency (2000 recommended for DC motor)
    def setFrequency(self, frequency):
        self.PWMpin.freq(frequency)

    # Sets duty cycle
    def setDuty(self, dutycycle):
        self.PWMpin.duty(dutycycle)

    # Makes the motor turn one way
    def forward(self):
        self.togglepinA.value(1)
        self.togglepinB.value(0)

    # Makes the motor turn the opposite way
    def reverse(self):
        self.togglepinA.value(0)
        self.togglepinB.value(1)
